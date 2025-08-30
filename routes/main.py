from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Application, Audit, Transaction

main = Blueprint('main', __name__)
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from app.forms import EditProfileForm
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.organization = form.organization.data
        current_user.bio = form.bio.data
        if form.password.data:
            current_user.set_password(form.password.data)
        from app import db
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'producer':
        applications = Application.query.filter_by(producer_id=current_user.id).all()
        return render_template('dashboard.html', applications=applications)
    
    elif current_user.role == 'auditor':
        applications = Application.query.filter_by(status='pending').all()
        return render_template('dashboard.html', applications=applications)
    
    elif current_user.role == 'government':
        applications = Application.query.filter_by(status='auditor_verified').all()
        return render_template('dashboard.html', applications=applications)
    
    elif current_user.role == 'bank':
        applications = Application.query.filter_by(status='govt_approved').all()
        transactions = Transaction.query.filter_by(bank_id=current_user.id).all()
        return render_template('dashboard.html', applications=applications, transactions=transactions)
    
    return render_template('dashboard.html')

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404