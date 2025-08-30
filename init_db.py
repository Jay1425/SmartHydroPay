#!/usr/bin/env python3
"""
Database initialization script for SmartHydroPay
Creates sample users for testing each role
"""

from app import create_app, db
from app.models import User, Application, Audit, Transaction

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if users already exist
        if User.query.first():
            print("Database already has users. Skipping initialization.")
            return
        
        # Create sample users for each role
        users_data = [
            {
                'name': 'Government Officer',
                'email': 'gov@smarthydropay.com',
                'password': 'password123',
                'role': 'government'
            },
            {
                'name': 'Green Energy Producer',
                'email': 'producer@example.com',
                'password': 'password123',
                'role': 'producer'
            },
            {
                'name': 'Project Auditor',
                'email': 'auditor@example.com',
                'password': 'password123',
                'role': 'auditor'
            },
            {
                'name': 'Bank Officer',
                'email': 'bank@example.com',
                'password': 'password123',
                'role': 'bank'
            }
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        
        print("Sample users created:")
        for user in users:
            print(f"- {user.role}: {user.email} (password: password123)")
        
        # Create a sample application
        producer = User.query.filter_by(role='producer').first()
        if producer:
            sample_app = Application(
                producer_id=producer.id,
                project_name="GreenH2 Renewable Energy Plant",
                capacity=50.0,
                documents="""Project Overview:
- Location: Maharashtra, India
- Technology: Electrolysis-based green hydrogen production
- Estimated Production: 10 tons/day
- Investment: $5 million
- Timeline: 18 months construction

Technical Specifications:
- Electrolysis capacity: 50 MW
- Renewable energy source: Solar + Wind hybrid
- Storage capacity: 500 kg H2
- Distribution: Pipeline and truck transport

Environmental Impact:
- Zero carbon emissions during operation
- Waste water treatment integrated
- Circular economy approach

Financial Projections:
- ROI: 15% over 10 years
- Job creation: 50 direct, 200 indirect
- Local community benefits included""",
                status='pending'
            )
            db.session.add(sample_app)
            db.session.commit()
            print(f"Sample application created: {sample_app.project_name}")
        
        print("\nDatabase initialized successfully!")
        print("You can now run the application with: python run.py")

if __name__ == '__main__':
    init_database()
