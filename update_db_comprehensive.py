#!/usr/bin/env python3
"""
Comprehensive Database Update Script for SmartHydroPay
Adds all new fields for enhanced producer, government, auditor, and bank functionality
"""

from app import create_app, db
from app.models import User, Application, Audit, Transaction, Milestone, SubsidyPolicy
from datetime import datetime
import json

def update_database():
    """Update database schema with new comprehensive fields"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Starting comprehensive database update...")
        
        try:
            # Drop all tables and recreate (for development)
            print("📋 Recreating database tables...")
            db.drop_all()
            db.create_all()
            
            # Create sample subsidy policies
            print("💰 Creating sample subsidy policies...")
            create_sample_policies()
            
            # Create sample users with comprehensive data
            print("👥 Creating sample users...")
            create_sample_users()
            
            print("✅ Database update completed successfully!")
            print("\n📊 Database Summary:")
            print(f"   Users: {User.query.count()}")
            print(f"   Applications: {Application.query.count()}")
            print(f"   Subsidy Policies: {SubsidyPolicy.query.count()}")
            
        except Exception as e:
            print(f"❌ Error updating database: {str(e)}")
            db.session.rollback()
            raise

def create_sample_policies():
    """Create sample subsidy policies"""
    policies = [
        {
            'policy_name': 'Electrolysis Subsidy Scheme 2025',
            'technology_type': 'electrolysis',
            'rate_per_ton': 50000,  # ₹50,000 per ton
            'rate_per_mw': 5000000,  # ₹50 lakh per MW
            'rate_percentage_capex': 30,  # 30% of CAPEX
            'eligibility_criteria': json.dumps({
                'min_capacity_mw': 1,
                'min_efficiency': 75,
                'environmental_clearance': True
            })
        },
        {
            'policy_name': 'Steam Reforming Modernization Scheme',
            'technology_type': 'steam_reforming',
            'rate_per_ton': 30000,  # ₹30,000 per ton
            'rate_percentage_capex': 20,  # 20% of CAPEX
            'eligibility_criteria': json.dumps({
                'carbon_capture': True,
                'efficiency_improvement': 15
            })
        },
        {
            'policy_name': 'Biomass Gasification Incentive',
            'technology_type': 'biomass_gasification',
            'rate_per_ton': 40000,  # ₹40,000 per ton
            'rate_percentage_capex': 35,  # 35% of CAPEX
            'eligibility_criteria': json.dumps({
                'sustainable_biomass': True,
                'rural_location': True
            })
        }
    ]
    
    for policy_data in policies:
        policy = SubsidyPolicy(**policy_data)
        db.session.add(policy)
    
    db.session.commit()

def create_sample_users():
    """Create sample users with comprehensive data"""
    
    # Producer (Startup)
    producer = User(
        name='GreenH2 Industries',
        email='producer@greenh2.com',
        role='producer',
        phone='+91-9876543210',
        organization='GreenH2 Industries Pvt Ltd',
        bio='Leading green hydrogen producer focused on electrolysis technology',
        company_name='GreenH2 Industries Pvt Ltd',
        registration_number='U40300DL2023PTC123456',
        gst_number='07AABCU9603R1ZX',
        contact_person='Rajesh Kumar',
        bank_account_number='1234567890123456',
        bank_name='State Bank of India',
        ifsc_code='SBIN0001234',
        bank_verification_status='verified',
        is_verified=True
    )
    producer.set_password('producer123')
    
    # Government Official
    govt = User(
        name='Ministry of New & Renewable Energy',
        email='govt@mnre.gov.in',
        role='government',
        phone='+91-9876543211',
        organization='MNRE',
        bio='Government body overseeing green hydrogen policy implementation',
        is_verified=True
    )
    govt.set_password('govt123')
    
    # Auditor
    auditor = User(
        name='Energy Audit Solutions',
        email='auditor@energyaudit.com',
        role='auditor',
        phone='+91-9876543212',
        organization='Energy Audit Solutions Ltd',
        bio='Certified energy and environmental auditor',
        auditor_id_number='EA2025001',
        certification='ISO 50001 Lead Auditor',
        is_verified=True
    )
    auditor.set_password('auditor123')
    
    # Bank
    bank = User(
        name='Green Finance Bank',
        email='bank@greenfinance.com',
        role='bank',
        phone='+91-9876543213',
        organization='Green Finance Bank Ltd',
        bio='Specialized bank for green energy financing',
        is_verified=True
    )
    bank.set_password('bank123')
    
    # Add users to database
    users = [producer, govt, auditor, bank]
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    
    # Create sample application
    application = Application(
        producer_id=producer.id,
        project_name='Solar Electrolysis Plant Mumbai',
        project_title='Large Scale Solar-Powered Electrolysis Facility',
        project_description='A 10 MW solar-powered electrolysis plant for green hydrogen production',
        technology_type='electrolysis',
        capacity_mw=10.0,
        capacity_tons=1000,
        project_location='Mumbai, Maharashtra',
        capex_estimate=5000,  # ₹50 crores
        opex_estimate=500,    # ₹5 crores per year
        capacity=10.0,  # Legacy field
        project_details='Comprehensive green hydrogen production facility using advanced PEM electrolysis',
        status='pending'
    )
    
    db.session.add(application)
    db.session.commit()
    
    print(f"✅ Created sample users and application")

if __name__ == '__main__':
    update_database()
