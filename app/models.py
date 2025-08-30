from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

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
    project_name = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    project_details = db.Column(db.Text)  # Project details text
    documents = db.Column(db.Text)  # JSON string or file paths
    status = db.Column(db.String(50), default='pending')  # pending, auditor_verified, govt_approved, fund_released
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    govt_comments = db.Column(db.Text)  # Government review comments
    
    # Relationships
    audits = db.relationship('Audit', backref='application', lazy=True)
    transactions = db.relationship('Transaction', backref='application', lazy=True)
    
    def __repr__(self):
        return f'<Application {self.project_name}>'

class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    auditor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Audit {self.id}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transaction {self.amount}>'
