from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

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

class ApplicationForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=200)])
    capacity = FloatField('Capacity (MW)', validators=[DataRequired(), NumberRange(min=0.1)])
    documents = TextAreaField('Documents/Details', validators=[DataRequired()])

class AuditForm(FlaskForm):
    comments = TextAreaField('Audit Comments', validators=[DataRequired()])
    verified = BooleanField('Verified')

class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
