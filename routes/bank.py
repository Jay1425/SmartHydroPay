from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import Application, Transaction
from app.forms import TransactionForm

bank = Blueprint('bank', __name__)

@bank.before_request
@login_required
def require_bank():
    if current_user.role != 'bank':
        abort(403)

@bank.route('/transactions')
def transactions():
    transactions = Transaction.query.filter_by(bank_id=current_user.id).all()
    pending_applications = Application.query.filter_by(status='govt_approved').all()
    return render_template('transactions.html', 
                         transactions=transactions, 
                         pending_applications=pending_applications)

@bank.route('/release/<int:application_id>', methods=['GET', 'POST'])
def release(application_id):
    application = Application.query.get_or_404(application_id)
    
    if application.status != 'govt_approved':
        flash('Funds can only be released for government approved applications.', 'warning')
        return redirect(url_for('bank.transactions'))
    
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            bank_id=current_user.id,
            application_id=application_id,
            amount=form.amount.data,
            comments=form.comments.data
        )
        
        # Update application status
        application.status = 'fund_released'
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Funds of ${form.amount.data:,.2f} released for "{application.project_name}"!', 'success')
        return redirect(url_for('bank.transactions'))
    
    # Calculate recommended amount
    print(f"Application capacity: {application.capacity} (type: {type(application.capacity)})")
    recommended_amount = float(application.capacity) * 100000
    print(f"Recommended amount: {recommended_amount}")
    
    return render_template('release_funds.html', 
                         form=form, 
                         application=application, 
                         recommended_amount=recommended_amount)

@bank.route('/pending')
def pending_releases():
    applications = Application.query.filter_by(status='govt_approved').all()
    return render_template('pending_releases.html', applications=applications)
