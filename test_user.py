#!/usr/bin/env python3
"""
Test script to create a user and test photo upload functionality
"""

from app import create_app, db
from app.models import User

def create_test_user():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if test user already exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            print("Test user already exists.")
            print(f"User: {test_user.name} ({test_user.email})")
            print(f"Profile photo: {test_user.profile_photo}")
            return
        
        # Create test user
        user = User(
            name='Test User',
            email='test@example.com',
            role='producer',
            phone='1234567890',
            organization='Test Company',
            bio='This is a test user for photo upload testing.'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        print("Test user created successfully!")
        print(f"Email: test@example.com")
        print(f"Password: password123")
        print(f"Profile photo: {user.profile_photo}")

if __name__ == '__main__':
    create_test_user()
