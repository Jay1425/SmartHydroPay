from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, TextAreaField, FloatField, BooleanField
from flask_wtf.file import FileField
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

class ApplicationForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=200)])
    capacity = FloatField('Capacity (MW)', validators=[DataRequired(), NumberRange(min=0.1)])
    project_details = TextAreaField('Project Details', validators=[Optional()])
    document_files = FileField('Upload Documents', render_kw={"multiple": True})


class AuditForm(FlaskForm):
    comments = TextAreaField('Audit Comments', validators=[DataRequired()])
    verified = BooleanField('Verified')

class GovernmentReviewForm(FlaskForm):
    comments = TextAreaField('Government Review Comments', validators=[DataRequired()])
    approved = BooleanField('Approved')

class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
