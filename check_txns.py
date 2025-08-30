#!/usr/bin/env python3
"""
Test script to check and create sample transaction data
"""

from app import create_app, db
from app.models import User, Application, Transaction

def check_transactions():
    app = create_app()
    
    with app.app_context():
        # Check existing transactions
        transactions = Transaction.query.all()
        print(f"Found {len(transactions)} transactions")
        
        for txn in transactions:
            print(f"Transaction {txn.id}: Amount ${txn.amount}, Date: {txn.date}")
            try:
                print(f"  Application: {txn.application.project_name}")
                print(f"  Producer: {txn.application.producer.name}")
            except Exception as e:
                print(f"  Error accessing relationship: {e}")
        
        # Check applications that are fund_released
        approved_apps = Application.query.filter_by(status='fund_released').all()
        print(f"\nFound {len(approved_apps)} applications with fund_released status")
        
        # Check government approved apps (available for fund release)
        govt_approved_apps = Application.query.filter_by(status='govt_approved').all()
        print(f"Found {len(govt_approved_apps)} applications ready for fund release")

if __name__ == '__main__':
    check_transactions()
