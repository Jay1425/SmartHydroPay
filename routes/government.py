from flask import Blueprint, render_template, redirect, url_for, flash, abort
government = Blueprint('government', __name__)
from flask_login import login_required, current_user
from app import db
from app.models import Application, Audit
from app.forms import GovernmentReviewForm

government = Blueprint('government', __name__)

@government.route('/review/<int:application_id>', methods=['GET', 'POST'])
def review_application(application_id):
    application = Application.query.get_or_404(application_id)
    form = GovernmentReviewForm()
    if form.validate_on_submit():
        application.status = 'govt_approved' if form.approved.data else 'rejected'
        application.govt_comments = form.comments.data
        db.session.commit()
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('government.applications'))
    return render_template('govt_review.html', application=application, form=form)

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
