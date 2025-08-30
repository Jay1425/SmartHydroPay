from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import Application, Audit, SubsidyPolicy, Milestone
from app.forms import GovernmentReviewForm, SubsidyPolicyForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime

government = Blueprint('government', __name__)

@government.before_request
@login_required
def require_government():
    if current_user.role != 'government':
        abort(403)

@government.route('/applications')
def applications():
    # Show applications at different stages
    pending_audit = Application.query.filter_by(status='pending').all()
    auditor_verified = Application.query.filter_by(status='auditor_verified').all()
    under_review = Application.query.filter_by(status='under_government_review').all()
    
    return render_template('govt_applications.html', 
                         pending_audit=pending_audit,
                         auditor_verified=auditor_verified,
                         under_review=under_review)

@government.route('/review/<int:application_id>', methods=['GET', 'POST'])
def review_application(application_id):
    application = Application.query.get_or_404(application_id)
    audit = Audit.query.filter_by(application_id=application_id).first()
    milestones = Milestone.query.filter_by(application_id=application_id).all()
    
    form = GovernmentReviewForm()
    
    if form.validate_on_submit():
        # Handle approval document upload
        approval_doc = None
        if form.approval_document.data:
            file = form.approval_document.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'approvals', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            approval_doc = f'uploads/approvals/{filename}'
        
        # Update application status and details
        if form.approved.data:
            application.status = 'govt_approved'
            application.govt_approval_date = datetime.utcnow()
            application.approval_reference_number = form.approval_reference_number.data
            application.approval_conditions = form.approval_conditions.data
            application.subsidy_amount_approved = form.subsidy_amount_approved.data
            flash(f'Application "{application.project_name}" approved successfully!', 'success')
        else:
            application.status = 'rejected'
            application.rejection_reason = form.rejection_reason.data
            flash(f'Application "{application.project_name}" rejected.', 'info')
        
        application.govt_comments = form.govt_comments.data
        application.govt_reviewer_id = current_user.id
        application.approval_document_path = approval_doc
        
        db.session.commit()
        return redirect(url_for('government.applications'))
    
    return render_template('govt_review.html', 
                         application=application, 
                         audit=audit, 
                         milestones=milestones,
                         form=form)

@government.route('/policies', methods=['GET', 'POST'])
def manage_policies():
    form = SubsidyPolicyForm()
    
    if form.validate_on_submit():
        policy = SubsidyPolicy(
            policy_name=form.policy_name.data,
            technology_type=form.technology_type.data,
            rate_per_ton=form.rate_per_ton.data,
            rate_per_mw=form.rate_per_mw.data,
            rate_percentage_capex=form.rate_percentage_capex.data,
            min_capacity_threshold=form.min_capacity_threshold.data,
            max_capacity_threshold=form.max_capacity_threshold.data,
            policy_start_date=form.policy_start_date.data,
            policy_end_date=form.policy_end_date.data,
            eligibility_criteria=form.eligibility_criteria.data,
            created_by_id=current_user.id
        )
        
        db.session.add(policy)
        db.session.commit()
        flash('Subsidy policy created successfully!', 'success')
        return redirect(url_for('government.manage_policies'))
    
    policies = SubsidyPolicy.query.all()
    return render_template('manage_policies.html', policies=policies, form=form)

@government.route('/policy/<int:policy_id>/update', methods=['POST'])
def update_policy(policy_id):
    policy = SubsidyPolicy.query.get_or_404(policy_id)
    
    if request.form.get('action') == 'activate':
        policy.is_active = True
        flash('Policy activated successfully!', 'success')
    elif request.form.get('action') == 'deactivate':
        policy.is_active = False
        flash('Policy deactivated successfully!', 'info')
    
    db.session.commit()
    return redirect(url_for('government.manage_policies'))

@government.route('/approve/<int:application_id>')
def approve(application_id):
    application = Application.query.get_or_404(application_id)
    
    if application.status != 'auditor_verified':
        flash('Application cannot be approved. It must be auditor verified first.', 'warning')
        return redirect(url_for('government.applications'))
    
    application.status = 'govt_approved'
    application.govt_approval_date = datetime.utcnow()
    db.session.commit()
    flash(f'Application "{application.project_name}" approved successfully!', 'success')
    return redirect(url_for('government.applications'))

@government.route('/reject/<int:application_id>')
def reject(application_id):
    application = Application.query.get_or_404(application_id)
    
    application.status = 'rejected'
    db.session.commit()
    flash(f'Application "{application.project_name}" rejected.', 'info')
    return redirect(url_for('government.applications'))

@government.route('/view/<int:application_id>')
def view_application(application_id):
    application = Application.query.get_or_404(application_id)
    audit = Audit.query.filter_by(application_id=application_id).first()
    milestones = Milestone.query.filter_by(application_id=application_id).all()
    return render_template('approve.html', 
                         application=application, 
                         audit=audit, 
                         milestones=milestones)
