from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Application
from app.forms import ApplicationForm

producer = Blueprint('producer', __name__)

@producer.before_request
@login_required
def require_producer():
    if current_user.role != 'producer':
        abort(403)

@producer.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            producer_id=current_user.id,
            project_name=form.project_name.data,
            capacity=form.capacity.data,
            documents=form.documents.data,
            status='pending'
        )
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('producer.my_applications'))
    
    return render_template('apply_form.html', form=form)

@producer.route('/my_applications')
def my_applications():
    applications = Application.query.filter_by(producer_id=current_user.id).all()
    return render_template('my_applications.html', applications=applications)
