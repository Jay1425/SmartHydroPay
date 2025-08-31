from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Application, Audit
from app.forms import AuditForm

auditor = Blueprint('auditor', __name__)

@auditor.before_request
@login_required
def require_auditor():
    if current_user.role != 'auditor':
        abort(403)

@auditor.route('/verify/<int:application_id>', methods=['GET', 'POST'])
def verify(application_id):
    application = Application.query.get_or_404(application_id)
    
    # Check if this application is already audited
    existing_audit = Audit.query.filter_by(
        application_id=application_id,
        auditor_id=current_user.id
    ).first()
    
    form = AuditForm()
    if form.validate_on_submit():
        if existing_audit:
            # Update existing audit
            existing_audit.comments = form.comments.data
            existing_audit.verified = form.verified.data
        else:
            # Create new audit
            audit = Audit(
                application_id=application_id,
                auditor_id=current_user.id,
                comments=form.comments.data,
                verified=form.verified.data
            )
            db.session.add(audit)
        
        # Update application status
        if form.verified.data:
            application.status = 'auditor_verified'
        else:
            application.status = 'rejected'
        
        db.session.commit()
        flash('Audit completed successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Pre-populate form if audit exists
    if existing_audit:
        form.comments.data = existing_audit.comments
        form.verified.data = existing_audit.verified
    
    return render_template('verify.html', form=form, application=application)

@auditor.route('/applications')
def applications():
    applications = Application.query.filter_by(status='pending').all()
    return render_template('auditor_applications.html', applications=applications)
