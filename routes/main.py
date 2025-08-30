from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Application, Audit, Transaction

main = Blueprint('main', __name__)

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
