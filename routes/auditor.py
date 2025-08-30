from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import Application, Audit, Milestone
from app.forms import AuditForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime

auditor = Blueprint('auditor', __name__)

@auditor.before_request
@login_required
def require_auditor():
    if current_user.role != 'auditor':
        abort(403)

@auditor.route('/applications')
def applications():
    # Show applications pending audit and completed audits
    pending_audits = Application.query.filter_by(status='pending').all()
    completed_audits = Audit.query.filter_by(auditor_id=current_user.id).all()
    
    return render_template('auditor_applications.html', 
                         pending_audits=pending_audits,
                         completed_audits=completed_audits)

@auditor.route('/verify/<int:application_id>', methods=['GET', 'POST'])
def verify(application_id):
    application = Application.query.get_or_404(application_id)
    milestones = Milestone.query.filter_by(application_id=application_id).all()
    
    # Check if this application is already audited
    existing_audit = Audit.query.filter_by(
        application_id=application_id,
        auditor_id=current_user.id
    ).first()
    
    form = AuditForm()
    
    if form.validate_on_submit():
        # Handle audit report file upload
        audit_report_path = None
        if form.audit_report_file.data:
            file = form.audit_report_file.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'audit_reports', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            audit_report_path = f'uploads/audit_reports/{filename}'
        
        if existing_audit:
            # Update existing audit
            existing_audit.audit_comments = form.audit_comments.data
            existing_audit.technical_compliance = form.technical_compliance.data
            existing_audit.financial_compliance = form.financial_compliance.data
            existing_audit.environmental_compliance = form.environmental_compliance.data
            existing_audit.overall_compliance_score = form.overall_compliance_score.data
            existing_audit.compliance_status = form.compliance_status.data
            existing_audit.recommendations = form.recommendations.data
            existing_audit.verified = form.verified.data
            if audit_report_path:
                existing_audit.audit_report_path = audit_report_path
            existing_audit.audit_date = datetime.utcnow()
        else:
            # Create new comprehensive audit
            audit = Audit(
                application_id=application_id,
                auditor_id=current_user.id,
                audit_comments=form.audit_comments.data,
                technical_compliance=form.technical_compliance.data,
                financial_compliance=form.financial_compliance.data,
                environmental_compliance=form.environmental_compliance.data,
                overall_compliance_score=form.overall_compliance_score.data,
                compliance_status=form.compliance_status.data,
                recommendations=form.recommendations.data,
                verified=form.verified.data,
                audit_report_path=audit_report_path,
                audit_date=datetime.utcnow(),
                # Legacy field for backward compatibility
                comments=form.audit_comments.data
            )
            db.session.add(audit)
        
        # Update application status based on audit outcome
        if form.verified.data and form.compliance_status.data == 'compliant':
            application.status = 'auditor_verified'
        elif form.compliance_status.data == 'non_compliant':
            application.status = 'rejected'
        else:
            application.status = 'requires_revision'
        
        db.session.commit()
        flash('Comprehensive audit completed successfully!', 'success')
        return redirect(url_for('auditor.applications'))
    
    # Pre-populate form if audit exists
    if existing_audit:
        form.audit_comments.data = existing_audit.audit_comments
        form.verified.data = existing_audit.verified
        form.technical_compliance.data = existing_audit.technical_compliance
        form.financial_compliance.data = existing_audit.financial_compliance
        form.environmental_compliance.data = existing_audit.environmental_compliance
        form.overall_compliance_score.data = existing_audit.overall_compliance_score
        form.compliance_status.data = existing_audit.compliance_status
        form.recommendations.data = existing_audit.recommendations
    
    return render_template('verify.html', 
                         form=form, 
                         application=application,
                         milestones=milestones,
                         existing_audit=existing_audit)

@auditor.route('/milestone/<int:milestone_id>/verify', methods=['POST'])
def verify_milestone(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    
    verification_status = request.form.get('verification_status')
    verification_comments = request.form.get('verification_comments')
    
    if verification_status == 'verified':
        milestone.auditor_verification_status = 'verified'
        milestone.auditor_verification_date = datetime.utcnow()
        milestone.auditor_verification_comments = verification_comments
        flash('Milestone verified successfully!', 'success')
    elif verification_status == 'rejected':
        milestone.auditor_verification_status = 'rejected'
        milestone.auditor_verification_comments = verification_comments
        flash('Milestone verification rejected.', 'warning')
    
    db.session.commit()
    return redirect(url_for('auditor.verify', application_id=milestone.application_id))

@auditor.route('/audit/<int:audit_id>/view')
def view_audit(audit_id):
    audit = Audit.query.get_or_404(audit_id)
    
    # Ensure the audit belongs to the current auditor
    if audit.auditor_id != current_user.id:
        abort(403)
    
    return render_template('view_audit.html', audit=audit)

@auditor.route('/profile/update', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        # Update auditor-specific information
        current_user.auditor_id_number = request.form.get('auditor_id_number', current_user.auditor_id_number)
        current_user.certification = request.form.get('certification', current_user.certification)
        
        # Update contact details
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.bio = request.form.get('bio', current_user.bio)
        current_user.organization = request.form.get('organization', current_user.organization)
        
        db.session.commit()
        flash('Auditor profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('edit_profile.html', user=current_user)
