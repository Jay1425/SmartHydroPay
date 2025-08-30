from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, TextAreaField, FloatField, BooleanField, DateField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class OTPVerificationForm(FlaskForm):
    otp_code = StringField('Enter 6-digit OTP', validators=[DataRequired(), Length(min=6, max=6)])

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[
        ('government', 'Government Body'),
        ('producer', 'Green Hydrogen Producer/Startup'),
        ('auditor', 'Auditor'),
        ('bank', 'Bank')
    ], validators=[DataRequired()])

class EditProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    phone = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])
    organization = StringField('Organization/Company', validators=[Optional(), Length(max=200)])
    bio = TextAreaField('Bio/Description', validators=[Optional(), Length(max=500)])
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed!')
    ])
    
    # Producer-specific fields
    company_name = StringField('Company Name', validators=[Optional(), Length(max=200)])
    registration_number = StringField('Registration Number', validators=[Optional(), Length(max=100)])
    gst_number = StringField('GST Number', validators=[Optional(), Length(max=100)])
    contact_person = StringField('Contact Person', validators=[Optional(), Length(max=100)])
    bank_account_number = StringField('Bank Account Number', validators=[Optional(), Length(max=50)])
    bank_name = StringField('Bank Name', validators=[Optional(), Length(max=100)])
    ifsc_code = StringField('IFSC Code', validators=[Optional(), Length(max=20)])
    
    # Auditor-specific fields
    auditor_id_number = StringField('Auditor ID', validators=[Optional(), Length(max=50)])
    certification = StringField('Certification', validators=[Optional(), Length(max=200)])

# 🟦 Producer Forms
class ApplicationForm(FlaskForm):
    # Company Information
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=200)])
    registration_number = StringField('Registration Number', validators=[DataRequired(), Length(max=100)])
    gst_number = StringField('GST Number', validators=[Optional(), Length(max=100)])
    contact_person = StringField('Contact Person Name', validators=[DataRequired(), Length(max=100)])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=10, max=15)])
    
    # Bank Account Details
    bank_account_number = StringField('Bank Account Number', validators=[DataRequired(), Length(max=50)])
    bank_name = StringField('Bank Name', validators=[DataRequired(), Length(max=100)])
    ifsc_code = StringField('IFSC Code', validators=[DataRequired(), Length(max=20)])
    
    # Project Information
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=200)])
    project_title = StringField('Project Title', validators=[DataRequired(), Length(min=2, max=200)])
    project_description = TextAreaField('Project Description', validators=[DataRequired()])
    technology_type = SelectField('Technology Type', choices=[
        ('electrolysis', 'Electrolysis'),
        ('steam_reforming', 'Steam Methane Reforming'),
        ('biomass_gasification', 'Biomass Gasification'),
        ('solar_thermal', 'Solar Thermal'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    capacity_mw = FloatField('Capacity (MW)', validators=[Optional(), NumberRange(min=0.1)])
    capacity_tons = FloatField('Capacity (Tons H₂/year)', validators=[Optional(), NumberRange(min=0.1)])
    project_location = StringField('Project Location', validators=[DataRequired(), Length(max=200)])
    project_latitude = FloatField('Project Latitude', validators=[Optional(), NumberRange(min=-90, max=90)])
    project_longitude = FloatField('Project Longitude', validators=[Optional(), NumberRange(min=-180, max=180)])
    capex_estimate = FloatField('CAPEX Estimate (₹ Crores)', validators=[DataRequired(), NumberRange(min=0.1)])
    opex_estimate = FloatField('OPEX Estimate (₹ Crores/year)', validators=[DataRequired(), NumberRange(min=0.1)])
    expected_completion_date = DateField('Expected Completion Date', validators=[DataRequired()])
    
    # Infrastructure & Compliance
    land_acquisition_status = StringField('Land Acquisition Status', validators=[DataRequired(), Length(max=100)])
    power_supply_arrangement = StringField('Power Supply Arrangement', validators=[DataRequired(), Length(max=200)])
    water_source = StringField('Water Source', validators=[DataRequired(), Length(max=200)])
    environmental_clearance = BooleanField('Environmental Clearance Obtained')
    
    # Document Uploads
    environmental_clearance_file = FileField('Environmental Clearance Document', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'Only PDF, DOC, and image files allowed!')
    ])
    feasibility_report_file = FileField('Feasibility Report', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'xlsx', 'xls'], 'Only PDF, DOC, and Excel files allowed!')
    ])
    
    # Legacy field for backward compatibility
    capacity = FloatField('Overall Capacity', validators=[DataRequired(), NumberRange(min=0.1)])
    project_details = TextAreaField('Additional Project Details', validators=[Optional()])
    document_files = FileField('Upload Supporting Documents', render_kw={"multiple": True})

class MilestoneForm(FlaskForm):
    milestone_name = StringField('Milestone Name', validators=[DataRequired(), Length(max=200)])
    milestone_description = TextAreaField('Milestone Description', validators=[DataRequired()])
    planned_completion_date = DateField('Planned Completion Date', validators=[DataRequired()])
    milestone_percentage = FloatField('Milestone Percentage (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    milestone_amount = FloatField('Milestone Amount (₹)', validators=[DataRequired(), NumberRange(min=1)])
    milestone_document = FileField('Milestone Document', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'xlsx', 'xls'], 'Only PDF, DOC, and Excel files allowed!')
    ])

# 🟩 Government Forms  
class GovernmentReviewForm(FlaskForm):
    # Review Decision
    approved = BooleanField('Approve Application')
    approval_reference_number = StringField('Approval Reference Number', validators=[Optional(), Length(max=100)])
    approval_conditions = TextAreaField('Approval Conditions', validators=[Optional()])
    subsidy_amount_approved = FloatField('Subsidy Amount Approved (₹)', validators=[Optional(), NumberRange(min=0)])
    rejection_reason = TextAreaField('Rejection Reason', validators=[Optional()])
    
    # Comments and Documentation
    govt_comments = TextAreaField('Government Review Comments', validators=[DataRequired()])
    approval_document = FileField('Approval/Rejection Document', validators=[
        FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and DOC files allowed!')
    ])
    
    # Legacy fields for compatibility
    comments = TextAreaField('Additional Comments', validators=[Optional()])

# 🟥 Auditor Forms
class AuditForm(FlaskForm):
    # Compliance Assessment
    technical_compliance = SelectField('Technical Compliance', choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partially_compliant', 'Partially Compliant')
    ], validators=[DataRequired()])
    
    financial_compliance = SelectField('Financial Compliance', choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partially_compliant', 'Partially Compliant')
    ], validators=[DataRequired()])
    
    environmental_compliance = SelectField('Environmental Compliance', choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partially_compliant', 'Partially Compliant')
    ], validators=[DataRequired()])
    
    overall_compliance_score = IntegerField('Overall Compliance Score (0-100)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    
    compliance_status = SelectField('Overall Compliance Status', choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('requires_revision', 'Requires Revision')
    ], validators=[DataRequired()])
    
    # Audit Details
    audit_comments = TextAreaField('Detailed Audit Comments', validators=[DataRequired()])
    recommendations = TextAreaField('Recommendations for Improvement', validators=[Optional()])
    audit_report_file = FileField('Comprehensive Audit Report', validators=[
        FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and DOC files allowed!')
    ])
    
    # Decision
    verified = BooleanField('Approve for Next Stage')
    
    # Legacy fields for compatibility
    comments = TextAreaField('Additional Comments', validators=[Optional()])

# 🟨 Bank Forms
class TransactionForm(FlaskForm):
    # Transaction Details
    transaction_amount = FloatField('Transaction Amount (₹)', validators=[DataRequired(), NumberRange(min=1)])
    transaction_type = SelectField('Transaction Type', choices=[
        ('subsidy_payment', 'Subsidy Payment'),
        ('milestone_payment', 'Milestone Payment'),
        ('advance_payment', 'Advance Payment'),
        ('final_payment', 'Final Payment')
    ], validators=[DataRequired()])
    transaction_reference = StringField('Transaction Reference Number', validators=[DataRequired(), Length(max=100)])
    
    # Beneficiary Details
    beneficiary_account_number = StringField('Beneficiary Account Number', validators=[DataRequired(), Length(max=50)])
    beneficiary_bank_name = StringField('Beneficiary Bank Name', validators=[DataRequired(), Length(max=100)])
    beneficiary_ifsc_code = StringField('Beneficiary IFSC Code', validators=[DataRequired(), Length(max=20)])
    
    # Additional Information
    transaction_comments = TextAreaField('Transaction Comments', validators=[Optional()])
    transaction_document = FileField('Transaction Document/Receipt', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed!')
    ])
    
    # Legacy fields for backward compatibility
    amount = FloatField('Amount (Legacy)', validators=[Optional(), NumberRange(min=0)])
    comments = TextAreaField('Comments (Legacy)', validators=[Optional()])

# Admin Forms for Policy Management
class SubsidyPolicyForm(FlaskForm):
    policy_name = StringField('Policy Name', validators=[DataRequired(), Length(max=200)])
    technology_type = SelectField('Technology Type', choices=[
        ('electrolysis', 'Electrolysis'),
        ('steam_reforming', 'Steam Methane Reforming'),
        ('biomass_gasification', 'Biomass Gasification'),
        ('solar_thermal', 'Solar Thermal'),
        ('all', 'All Technologies')
    ], validators=[DataRequired()])
    rate_per_ton = FloatField('Rate per Ton (₹)', validators=[Optional(), NumberRange(min=0)])
    rate_per_mw = FloatField('Rate per MW (₹)', validators=[Optional(), NumberRange(min=0)])
    rate_percentage_capex = FloatField('Rate as % of CAPEX', validators=[Optional(), NumberRange(min=0, max=100)])
    min_capacity_threshold = FloatField('Minimum Capacity Threshold', validators=[Optional(), NumberRange(min=0)])
    max_capacity_threshold = FloatField('Maximum Capacity Threshold', validators=[Optional(), NumberRange(min=0)])
    policy_start_date = DateField('Policy Start Date', validators=[Optional()])
    policy_end_date = DateField('Policy End Date', validators=[Optional()])
    eligibility_criteria = TextAreaField('Eligibility Criteria', validators=[Optional()])
    is_active = BooleanField('Active Policy', default=True)
