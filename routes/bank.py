from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import Application, Transaction, Milestone, SubsidyPolicy
from app.forms import TransactionForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime

bank = Blueprint('bank', __name__)

@bank.before_request
@login_required
def require_bank():
    if current_user.role != 'bank':
        abort(403)

@bank.route('/transactions')
def transactions():
    # Show different categories of transactions and applications
    all_transactions = Transaction.query.filter_by(bank_id=current_user.id).order_by(Transaction.transaction_date.desc()).all()
    pending_releases = Application.query.filter_by(status='govt_approved').all()
    milestone_requests = Milestone.query.join(Application).filter(
        Milestone.status == 'completed',
        Milestone.auditor_verification_status == 'verified',
        Milestone.payment_status == 'pending'
    ).all()
    
    return render_template('transactions.html', 
                         transactions=all_transactions, 
                         pending_releases=pending_releases,
                         milestone_requests=milestone_requests)

@bank.route('/release/<int:application_id>', methods=['GET', 'POST'])
def release(application_id):
    application = Application.query.get_or_404(application_id)
    milestones = Milestone.query.filter_by(application_id=application_id).all()
    
    if application.status != 'govt_approved':
        flash('Funds can only be released for government approved applications.', 'warning')
        return redirect(url_for('bank.transactions'))
    
    form = TransactionForm()
    
    # Calculate subsidy amounts based on policy
    policy = SubsidyPolicy.query.filter_by(technology_type=application.technology_type).first()
    recommended_amount = 0
    
    if policy:
        if policy.rate_per_ton and application.capacity_tons:
            recommended_amount += policy.rate_per_ton * application.capacity_tons
        if policy.rate_per_mw and application.capacity_mw:
            recommended_amount += policy.rate_per_mw * application.capacity_mw
        if policy.rate_percentage_capex and application.capex_estimate:
            recommended_amount += (policy.rate_percentage_capex / 100) * application.capex_estimate * 1000000  # Convert crores to rupees
    
    if form.validate_on_submit():
        # Handle transaction document upload
        transaction_doc = None
        if form.transaction_document.data:
            file = form.transaction_document.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'transactions', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            transaction_doc = f'uploads/transactions/{filename}'
        
        transaction = Transaction(
            bank_id=current_user.id,
            application_id=application_id,
            transaction_amount=form.transaction_amount.data,
            transaction_type=form.transaction_type.data,
            transaction_reference=form.transaction_reference.data,
            beneficiary_account_number=form.beneficiary_account_number.data,
            beneficiary_bank_name=form.beneficiary_bank_name.data,
            beneficiary_ifsc_code=form.beneficiary_ifsc_code.data,
            transaction_comments=form.transaction_comments.data,
            transaction_document_path=transaction_doc,
            transaction_date=datetime.utcnow(),
            disbursement_status='completed',
            # Legacy fields for backward compatibility
            amount=form.transaction_amount.data,
            comments=form.transaction_comments.data
        )
        
        # Update application status
        application.status = 'fund_released'
        application.disbursement_amount = form.transaction_amount.data
        application.disbursement_date = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Funds of ₹{form.transaction_amount.data:,.2f} released for "{application.project_name}"!', 'success')
        return redirect(url_for('bank.transactions'))
    
    return render_template('release_funds.html', 
                         form=form, 
                         application=application, 
                         milestones=milestones,
                         recommended_amount=recommended_amount,
                         policy=policy)

@bank.route('/milestone/<int:milestone_id>/pay', methods=['POST'])
def pay_milestone(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    
    if milestone.auditor_verification_status != 'verified':
        flash('Milestone must be auditor verified before payment.', 'warning')
        return redirect(url_for('bank.transactions'))
    
    # Handle milestone payment document upload
    payment_doc = None
    if 'payment_document' in request.files:
        file = request.files['payment_document']
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'milestone_payments', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            payment_doc = f'uploads/milestone_payments/{filename}'
    
    # Create milestone payment transaction
    transaction = Transaction(
        bank_id=current_user.id,
        application_id=milestone.application_id,
        milestone_id=milestone_id,
        transaction_amount=milestone.milestone_amount,
        transaction_type='milestone_payment',
        transaction_reference=request.form.get('transaction_reference'),
        beneficiary_account_number=milestone.application.producer.bank_account_number,
        beneficiary_bank_name=milestone.application.producer.bank_name,
        beneficiary_ifsc_code=milestone.application.producer.ifsc_code,
        transaction_comments=f'Milestone payment for: {milestone.milestone_name}',
        transaction_document_path=payment_doc,
        transaction_date=datetime.utcnow(),
        disbursement_status='completed',
        # Legacy fields
        amount=milestone.milestone_amount,
        comments=f'Milestone payment for: {milestone.milestone_name}'
    )
    
    # Update milestone payment status
    milestone.payment_status = 'paid'
    milestone.payment_date = datetime.utcnow()
    
    db.session.add(transaction)
    db.session.commit()
    
    flash(f'Milestone payment of ₹{milestone.milestone_amount:,.2f} processed successfully!', 'success')
    return redirect(url_for('bank.transactions'))

@bank.route('/pending')
def pending_releases():
    applications = Application.query.filter_by(status='govt_approved').all()
    return render_template('pending_releases.html', applications=applications)

@bank.route('/transaction/<int:transaction_id>/view')
def view_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Ensure the transaction belongs to the current bank
    if transaction.bank_id != current_user.id:
        abort(403)
    
    return render_template('view_transaction.html', transaction=transaction)

@bank.route('/reconciliation')
def reconciliation():
    # Show transaction reconciliation and reports
    total_disbursed = db.session.query(db.func.sum(Transaction.transaction_amount)).filter_by(bank_id=current_user.id).scalar() or 0
    transaction_count = Transaction.query.filter_by(bank_id=current_user.id).count()
    
    recent_transactions = Transaction.query.filter_by(bank_id=current_user.id).order_by(Transaction.transaction_date.desc()).limit(10).all()
    
    return render_template('bank_reconciliation.html',
                         total_disbursed=total_disbursed,
                         transaction_count=transaction_count,
                         recent_transactions=recent_transactions)
