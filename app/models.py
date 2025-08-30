from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # government, producer, auditor, bank
    phone = db.Column(db.String(15), nullable=True)
    organization = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_photo = db.Column(db.String(200), nullable=True, default='default_avatar.svg')
    is_verified = db.Column(db.Boolean, default=False)  # Email verification status
    otp_code = db.Column(db.String(6), nullable=True)  # Temporary OTP storage
    otp_expires = db.Column(db.DateTime, nullable=True)  # OTP expiration time
    
    # Producer-specific fields
    company_name = db.Column(db.String(200), nullable=True)
    registration_number = db.Column(db.String(100), nullable=True)
    gst_number = db.Column(db.String(100), nullable=True)
    contact_person = db.Column(db.String(100), nullable=True)
    bank_account_number = db.Column(db.String(50), nullable=True)
    bank_name = db.Column(db.String(100), nullable=True)
    ifsc_code = db.Column(db.String(20), nullable=True)
    bank_verification_status = db.Column(db.String(20), default='pending')  # pending, verified, failed
    
    # Auditor-specific fields
    auditor_id_number = db.Column(db.String(50), nullable=True)
    certification = db.Column(db.String(200), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='producer', lazy=True)
    audits = db.relationship('Audit', backref='auditor', lazy=True)
    transactions = db.relationship('Transaction', backref='bank', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Basic project info
    project_name = db.Column(db.String(200), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.Text, nullable=True)
    technology_type = db.Column(db.String(100), nullable=True)  # Electrolysis, Steam Reforming, etc.
    capacity_mw = db.Column(db.Float, nullable=True)  # Capacity in MW
    capacity_tons = db.Column(db.Float, nullable=True)  # Capacity in tons H2
    project_location = db.Column(db.String(200), nullable=True)
    project_latitude = db.Column(db.Float, nullable=True)  # Latitude for map display
    project_longitude = db.Column(db.Float, nullable=True)  # Longitude for map display
    capex_estimate = db.Column(db.Float, nullable=True)
    opex_estimate = db.Column(db.Float, nullable=True)
    
    # Legacy fields for backward compatibility
    capacity = db.Column(db.Float, nullable=False, default=0)
    project_details = db.Column(db.Text)
    documents = db.Column(db.Text)  # JSON string of file paths
    
    # Status and workflow
    status = db.Column(db.String(50), default='pending')  # pending, auditor_verified, govt_approved, fund_released, rejected
    
    # Government review fields
    verification_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    review_notes = db.Column(db.Text, nullable=True)
    approval_decision = db.Column(db.String(20), nullable=True)  # approved, rejected
    approval_reason = db.Column(db.Text, nullable=True)
    subsidy_eligibility_criteria = db.Column(db.Text, nullable=True)  # JSON string
    subsidy_rate_per_ton = db.Column(db.Float, nullable=True)
    subsidy_rate_per_mw = db.Column(db.Float, nullable=True)
    subsidy_rate_percentage = db.Column(db.Float, nullable=True)
    total_sanctioned_amount = db.Column(db.Float, nullable=True)
    disbursement_schedule = db.Column(db.Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    
    # Legacy field
    govt_comments = db.Column(db.Text, nullable=True)
    
    # Relationships
    audits = db.relationship('Audit', backref='application', lazy=True)
    transactions = db.relationship('Transaction', backref='application', lazy=True)
    milestones = db.relationship('Milestone', backref='application', lazy=True)
    
    def calculate_subsidy_amount(self):
        """Calculate total subsidy amount based on rates and capacity"""
        total = 0
        if self.subsidy_rate_per_ton and self.capacity_tons:
            total += self.subsidy_rate_per_ton * self.capacity_tons
        if self.subsidy_rate_per_mw and self.capacity_mw:
            total += self.subsidy_rate_per_mw * self.capacity_mw
        if self.subsidy_rate_percentage and self.capex_estimate:
            total += (self.subsidy_rate_percentage / 100) * self.capex_estimate
        return total
    
    def __repr__(self):
        return f'<Application {self.project_name}>'

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    milestone_name = db.Column(db.String(200), nullable=False)
    milestone_date = db.Column(db.DateTime, nullable=False)
    production_data_tons_month = db.Column(db.Float, nullable=True)
    expenditure_report_path = db.Column(db.String(300), nullable=True)  # PDF/Excel file path
    compliance_certificate_path = db.Column(db.String(300), nullable=True)  # PDF file path
    status = db.Column(db.String(20), default='pending')  # pending, completed, verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Milestone {self.milestone_name}>'

class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    auditor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Audit details
    audit_report_path = db.Column(db.String(300), nullable=True)  # PDF file path
    audit_comments = db.Column(db.Text, nullable=True)
    compliance_status = db.Column(db.String(10), nullable=False, default='pending')  # pass, fail, pending
    
    # Legacy fields
    comments = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    
    # Audit logs (auto-generated)
    audit_log = db.Column(db.Text, nullable=True)  # JSON string of audit actions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def add_audit_log(self, action, user_id, details=None):
        """Add an entry to the audit log"""
        if not self.audit_log:
            self.audit_log = '[]'
        
        log_entries = json.loads(self.audit_log)
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'user_id': user_id,
            'details': details
        }
        log_entries.append(log_entry)
        self.audit_log = json.dumps(log_entries)
    
    def __repr__(self):
        return f'<Audit {self.id}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    
    # Bank transaction details
    subsidy_request_id = db.Column(db.String(100), unique=True, nullable=False)  # Auto-generated
    transaction_id = db.Column(db.String(100), nullable=True)  # From bank API or manual
    amount_disbursed = db.Column(db.Float, nullable=False)
    disbursement_date = db.Column(db.DateTime, nullable=True)
    payment_confirmation_path = db.Column(db.String(300), nullable=True)  # Bank statement upload
    
    # Status tracking
    disbursement_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    
    # Legacy fields
    amount = db.Column(db.Float, nullable=False, default=0)
    comments = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def generate_request_id(self):
        """Generate unique subsidy request ID"""
        import uuid
        self.subsidy_request_id = f"SR{datetime.utcnow().strftime('%Y%m%d')}{str(uuid.uuid4().hex[:6]).upper()}"
    
    def __repr__(self):
        return f'<Transaction {self.subsidy_request_id}>'

class SubsidyPolicy(db.Model):
    """Policy database for subsidy rules and rates"""
    id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(200), nullable=False)
    technology_type = db.Column(db.String(100), nullable=False)
    rate_per_ton = db.Column(db.Float, nullable=True)
    rate_per_mw = db.Column(db.Float, nullable=True)
    rate_percentage_capex = db.Column(db.Float, nullable=True)
    eligibility_criteria = db.Column(db.Text, nullable=True)  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SubsidyPolicy {self.policy_name}>'
