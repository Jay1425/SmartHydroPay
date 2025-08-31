from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from app import db, mail
from app.models import User
from app.forms import LoginForm, SignupForm, OTPVerificationForm
import secrets
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

def send_otp_email(email, otp):
    """Send OTP via email"""
    try:
        msg = Message(
            'SmartHydroPay - Your OTP Code',
            sender='aivisionaries.teams@gmail.com',
            recipients=[email]
        )
        msg.body = f'''
        Your OTP code for SmartHydroPay is: {otp}
        
        This code will expire in 5 minutes.
        
        If you didn't request this code, please ignore this email.
        '''
        msg.html = f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #10b981;">SmartHydroPay - OTP Verification</h2>
            <p>Your verification code is:</p>
            <div style="background: #f3f4f6; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                <h1 style="color: #1f2937; font-size: 32px; letter-spacing: 8px; margin: 0;">{otp}</h1>
            </div>
            <p>This code will expire in <strong>5 minutes</strong>.</p>
            <p style="color: #6b7280; font-size: 14px;">If you didn't request this code, please ignore this email.</p>
        </div>
        '''
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Generate OTP
            otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            user.otp_code = otp
            user.otp_expires = datetime.utcnow() + timedelta(minutes=5)
            db.session.commit()
            
            # Send OTP email
            if send_otp_email(user.email, otp):
                session['temp_user_id'] = user.id
                flash('OTP sent to your email. Please verify to continue.', 'info')
                return redirect(url_for('auth.verify_otp'))
            else:
                flash('Failed to send OTP. Please try again.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)

@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'temp_user_id' not in session:
        return redirect(url_for('auth.login'))
    
    form = OTPVerificationForm()
    if form.validate_on_submit():
        user = User.query.get(session['temp_user_id'])
        if user and user.otp_code == form.otp_code.data:
            if user.otp_expires and datetime.utcnow() <= user.otp_expires:
                # Clear OTP data
                user.otp_code = None
                user.otp_expires = None
                user.is_verified = True
                db.session.commit()
                
                # Log in user
                login_user(user)
                session.pop('temp_user_id', None)
                
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                flash('OTP has expired. Please login again.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    
    return render_template('verify_otp.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return render_template('signup.html', form=form)
        
        # Generate OTP
        otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            otp_code=otp,
            otp_expires=datetime.utcnow() + timedelta(minutes=5)
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Send OTP email
        if send_otp_email(user.email, otp):
            session['temp_user_id'] = user.id
            flash('Account created! OTP sent to your email for verification.', 'success')
            return redirect(url_for('auth.verify_otp'))
        else:
            # Delete user if email failed
            db.session.delete(user)
            db.session.commit()
            flash('Failed to send verification email. Please try again.', 'danger')
    
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
