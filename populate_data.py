#!/usr/bin/env python3
"""
Sample data population script for SmartHydroPay
Run this script to add realistic test data to your database
"""

from app import create_app, db
from app.models import User, Application, Audit, Transaction
from datetime import datetime, timedelta
import random

def create_sample_users():
    """Create sample users for all roles"""
    users = [
        # Government officials
        {
            'name': 'Dr. Sarah Johnson', 
            'email': 'sarah.johnson@gov.in', 
            'role': 'government',
            'phone': '+91-9876543210',
            'organization': 'Ministry of New & Renewable Energy',
            'bio': 'Senior Policy Officer specializing in green hydrogen initiatives and renewable energy policy development.'
        },
        {
            'name': 'Rajesh Kumar', 
            'email': 'rajesh.kumar@gov.in', 
            'role': 'government',
            'phone': '+91-9876543211',
            'organization': 'Department of Science & Technology',
            'bio': 'Director of Clean Energy Programs with 15+ years in sustainable energy policy.'
        },
        
        # Producers
        {
            'name': 'Adani Green Energy Ltd', 
            'email': 'projects@adanigreen.com', 
            'role': 'producer',
            'phone': '+91-9876543212',
            'organization': 'Adani Green Energy Limited',
            'bio': 'Leading renewable energy company focused on solar, wind, and green hydrogen projects across India.'
        },
        {
            'name': 'Reliance New Energy', 
            'email': 'hydrogen@ril.com', 
            'role': 'producer',
            'phone': '+91-9876543213',
            'organization': 'Reliance Industries Limited',
            'bio': 'Pioneer in green hydrogen production with integrated renewable energy and electrolyzer manufacturing.'
        },
        {
            'name': 'Tata Power Renewable', 
            'email': 'green.energy@tatapower.com', 
            'role': 'producer',
            'phone': '+91-9876543214',
            'organization': 'Tata Power Renewable Energy Ltd',
            'bio': 'Clean energy subsidiary of Tata Power focusing on utility-scale renewable projects and green hydrogen.'
        },
        
        # Auditors
        {
            'name': 'Dr. Priya Sharma', 
            'email': 'priya.sharma@audit.in', 
            'role': 'auditor',
            'phone': '+91-9876543215',
            'organization': 'Green Energy Certification Institute',
            'bio': 'Certified energy auditor with expertise in renewable energy project assessment and compliance verification.'
        },
        {
            'name': 'Vikram Singh', 
            'email': 'vikram.singh@bureau.gov.in', 
            'role': 'auditor',
            'phone': '+91-9876543216',
            'organization': 'Bureau of Energy Efficiency',
            'bio': 'Senior technical auditor specializing in green hydrogen production facility assessments.'
        },
        
        # Banks
        {
            'name': 'State Bank of India', 
            'email': 'renewable.finance@sbi.co.in', 
            'role': 'bank',
            'phone': '+91-9876543217',
            'organization': 'SBI Renewable Energy Division',
            'bio': 'Leading public sector bank with specialized renewable energy and green hydrogen financing solutions.'
        },
        {
            'name': 'HDFC Bank Green Finance', 
            'email': 'green.loans@hdfcbank.com', 
            'role': 'bank',
            'phone': '+91-9876543218',
            'organization': 'HDFC Bank Limited',
            'bio': 'Private sector bank offering comprehensive green financing products for clean energy projects.'
        },
        
        # Admin
        {
            'name': 'System Administrator', 
            'email': 'admin@smarthydropay.gov.in', 
            'role': 'admin',
            'phone': '+91-9876543219',
            'organization': 'SmartHydroPay Platform',
            'bio': 'Platform administrator responsible for system management and user coordination.'
        }
    ]
    
    created_users = []
    for user_data in users:
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone'],
            organization=user_data['organization'],
            bio=user_data['bio']
        )
        user.set_password('password123')  # Default password for all test users
        db.session.add(user)
        created_users.append(user)
    
    db.session.commit()
    print(f"✅ Created {len(created_users)} sample users")
    return created_users

def create_sample_applications(users):
    """Create sample applications from producers"""
    producers = [u for u in users if u.role == 'producer']
    
    applications_data = [
        {
            'project_name': 'Gujarat Solar-Green Hydrogen Hub',
            'capacity': 500.0,
            'documents': '''Project Overview: Large-scale integrated solar-green hydrogen production facility in Gujarat
            
Technical Specifications:
• Solar PV Capacity: 1000 MW
• Electrolyzer Capacity: 500 MW
• Expected Green Hydrogen Production: 200 tonnes/day
• Technology: Alkaline Electrolysis
• Location: Kutch District, Gujarat
            
Financial Details:
• Total Project Cost: ₹4,500 Crores
• Subsidy Request: ₹900 Crores (20%)
• Expected ROI: 12% over 20 years
• Job Creation: 2,000+ direct and indirect jobs
            
Environmental Impact:
• CO2 Reduction: 1.2 million tonnes annually
• Water Usage: Seawater desalination facility
• Land Requirement: 2,500 acres
            
Timeline:
• Phase 1 (Year 1-2): Solar installation and infrastructure
• Phase 2 (Year 3): Electrolyzer commissioning
• Full Operations: Year 4''',
            'status': 'pending'
        },
        {
            'project_name': 'Rajasthan Wind-Hydrogen Complex',
            'capacity': 300.0,
            'documents': '''Project Overview: Wind-powered green hydrogen production facility in Rajasthan
            
Technical Specifications:
• Wind Power Capacity: 600 MW
• Electrolyzer Capacity: 300 MW
• Expected Production: 120 tonnes H2/day
• Technology: PEM Electrolysis
• Location: Jaisalmer, Rajasthan
            
Financial Projections:
• Investment: ₹2,700 Crores
• Subsidy Requirement: ₹540 Crores
• Payback Period: 8 years
• Employment: 1,500 jobs
            
Sustainability Metrics:
• Renewable Energy: 100% wind-powered
• Carbon Neutrality: Achieved from day 1
• Water Conservation: Closed-loop system''',
            'status': 'auditor_verified'
        },
        {
            'project_name': 'Tamil Nadu Offshore Wind H2 Project',
            'capacity': 750.0,
            'documents': '''Project Overview: India's first offshore wind-hydrogen integrated project
            
Technical Details:
• Offshore Wind: 1500 MW
• Electrolyzer: 750 MW
• H2 Production: 300 tonnes/day
• Technology: Advanced PEM + Alkaline hybrid
• Location: Gulf of Mannar, Tamil Nadu
            
Economic Impact:
• Total Investment: ₹7,500 Crores
• Subsidy Request: ₹1,500 Crores
• Export Potential: ₹2,000 Crores annually
• Local Employment: 3,000+ jobs
            
Innovation Features:
• Floating wind turbines
• Subsea hydrogen pipeline
• Green ammonia co-production
• Smart grid integration''',
            'status': 'govt_approved'
        },
        {
            'project_name': 'Maharashtra Industrial H2 Cluster',
            'capacity': 200.0,
            'documents': '''Project Overview: Industrial green hydrogen cluster for steel and chemical industries
            
Technical Specifications:
• Solar Capacity: 400 MW
• Electrolyzer: 200 MW
• H2 Production: 80 tonnes/day
• End Users: Tata Steel, Bajaj Group
• Location: Aurangabad, Maharashtra
            
Business Model:
• Captive consumption: 60%
• Merchant sales: 40%
• Long-term contracts: 15 years
• Price competitive with grey hydrogen
            
Supply Chain Integration:
• Direct pipeline to steel plant
• Truck-based distribution network
• Storage: 500 tonnes capacity
• Quality: 99.99% purity''',
            'status': 'fund_released'
        },
        {
            'project_name': 'Odisha Coastal Green H2 Export Hub',
            'capacity': 1000.0,
            'documents': '''Project Overview: Mega green hydrogen export facility with dedicated port infrastructure
            
Scale and Scope:
• Solar + Wind: 2000 MW
• Electrolyzer: 1000 MW
• H2 Production: 400 tonnes/day
• Export Terminal: Paradip Port
• Target Markets: Japan, South Korea, Europe
            
Infrastructure Development:
• Dedicated hydrogen storage: 2000 tonnes
• Liquefaction facility: 100 tonnes/day
• Port handling: Specialized H2 carriers
• Pipeline network: 50 km integrated system
            
Strategic Partnerships:
• Technology: Siemens Energy
• Shipping: Kawasaki Heavy Industries  
• Off-take: JERA (Japan), Hyundai (Korea)
• Financing: JBIC, KfW development banks''',
            'status': 'pending'
        }
    ]
    
    created_applications = []
    for i, app_data in enumerate(applications_data):
        producer = producers[i % len(producers)]  # Cycle through producers
        
        # Create applications with dates spread over last 6 months
        created_date = datetime.utcnow() - timedelta(days=random.randint(30, 180))
        
        application = Application(
            producer_id=producer.id,
            project_name=app_data['project_name'],
            capacity=app_data['capacity'],
            documents=app_data['documents'],
            status=app_data['status'],
            created_at=created_date
        )
        db.session.add(application)
        created_applications.append(application)
    
    db.session.commit()
    print(f"✅ Created {len(created_applications)} sample applications")
    return created_applications

def create_sample_audits(applications, users):
    """Create sample audit records"""
    auditors = [u for u in users if u.role == 'auditor']
    
    audit_data = [
        {
            'comments': '''Technical Assessment:
✅ Solar/Wind resource assessment verified
✅ Electrolyzer specifications meet industry standards
✅ Environmental clearances in progress
✅ Financial projections realistic
✅ Technology provider credentials verified

Compliance Check:
✅ All regulatory requirements met
✅ Land acquisition documents complete  
✅ Power evacuation approval obtained
✅ Water usage permits secured

Recommendation: APPROVED - Project meets all technical and financial criteria for subsidy eligibility.''',
            'verified': True
        },
        {
            'comments': '''Detailed Technical Review:
✅ Wind resource data validated (capacity factor: 35%)
✅ PEM technology selection appropriate for variable wind
✅ Grid integration studies completed
✅ Hydrogen storage and distribution plan robust
✅ Safety protocols comprehensive

Risk Assessment:
⚠️ Wind variability impact on production
✅ Mitigation through battery storage included
✅ Long-term wind data available (10+ years)
✅ Insurance coverage adequate

Final Assessment: VERIFIED - Recommend for government approval with minor conditions.''',
            'verified': True
        },
        {
            'comments': '''Comprehensive Audit Report:
✅ Offshore wind feasibility study excellent
✅ Hybrid electrolyzer approach innovative
✅ Environmental impact assessment thorough
✅ Export infrastructure planning detailed
✅ Financial modeling sophisticated

Technical Excellence:
✅ Cutting-edge floating wind technology
✅ Subsea hydrogen pipeline engineering validated
✅ International compliance standards met
✅ Risk mitigation strategies comprehensive

Recommendation: STRONGLY APPROVED - Flagship project with export potential.''',
            'verified': True
        }
    ]
    
    created_audits = []
    verified_apps = [app for app in applications if app.status in ['auditor_verified', 'govt_approved', 'fund_released']]
    
    for i, app in enumerate(verified_apps[:3]):  # Create audits for first 3 verified applications
        auditor = auditors[i % len(auditors)]
        audit_date = app.created_at + timedelta(days=random.randint(15, 45))
        
        audit = Audit(
            application_id=app.id,
            auditor_id=auditor.id,
            comments=audit_data[i]['comments'],
            verified=audit_data[i]['verified'],
            created_at=audit_date
        )
        db.session.add(audit)
        created_audits.append(audit)
    
    db.session.commit()
    print(f"✅ Created {len(created_audits)} sample audit records")
    return created_audits

def create_sample_transactions(applications, users):
    """Create sample transactions for fund releases"""
    banks = [u for u in users if u.role == 'bank']
    
    # Create transactions for applications with 'fund_released' status
    released_apps = [app for app in applications if app.status == 'fund_released']
    
    created_transactions = []
    for app in released_apps:
        bank = random.choice(banks)
        
        # Calculate subsidy amount (₹100,000 per MW)
        subsidy_amount = app.capacity * 100000
        
        # Transaction date after government approval
        transaction_date = app.created_at + timedelta(days=random.randint(60, 120))
        
        transaction = Transaction(
            bank_id=bank.id,
            application_id=app.id,
            amount=subsidy_amount,
            date=transaction_date
        )
        db.session.add(transaction)
        created_transactions.append(transaction)
    
    db.session.commit()
    print(f"✅ Created {len(created_transactions)} sample transactions")
    return created_transactions

def main():
    """Main function to populate all sample data"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting SmartHydroPay sample data population...")
        print("=" * 60)
        
        # Clear existing data (optional - uncomment if needed)
        # print("🗑️  Clearing existing data...")
        # db.drop_all()
        # db.create_all()
        
        # Create sample data
        users = create_sample_users()
        applications = create_sample_applications(users)
        audits = create_sample_audits(applications, users)
        transactions = create_sample_transactions(applications, users)
        
        print("=" * 60)
        print("🎉 Sample data population completed successfully!")
        print("\n📊 Summary:")
        print(f"   👥 Users: {len(users)}")
        print(f"   📄 Applications: {len(applications)}")  
        print(f"   🔍 Audits: {len(audits)}")
        print(f"   💰 Transactions: {len(transactions)}")
        print("\n🔑 Test Login Credentials:")
        print("   Email: Any user email from above")
        print("   Password: password123")
        print("\n🌟 Sample Users by Role:")
        
        role_counts = {}
        for user in users:
            if user.role not in role_counts:
                role_counts[user.role] = []
            role_counts[user.role].append(user)
        
        for role, users_in_role in role_counts.items():
            print(f"   {role.title()}: {len(users_in_role)} users")
            for user in users_in_role[:2]:  # Show first 2 users per role
                print(f"     • {user.name} ({user.email})")

if __name__ == '__main__':
    main()
