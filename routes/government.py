from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Application, Audit

government = Blueprint('government', __name__)

@government.before_request
@login_required
def require_government():
    if current_user.role != 'government':
        abort(403)

@government.route('/applications')
def applications():
    applications = Application.query.filter_by(status='auditor_verified').all()
    return render_template('govt_applications.html', applications=applications)

@government.route('/approve/<int:application_id>')
def approve(application_id):
    application = Application.query.get_or_404(application_id)
    
    if application.status != 'auditor_verified':
        flash('Application cannot be approved. It must be auditor verified first.', 'warning')
        return redirect(url_for('government.applications'))
    
    application.status = 'govt_approved'
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
    return render_template('approve.html', application=application, audit=audit)
