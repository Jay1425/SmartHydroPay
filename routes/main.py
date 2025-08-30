from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Application, Audit, Transaction
import os
import uuid

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_profile_photo(photo):
    """Save uploaded photo and return filename"""
    try:
        if photo and photo.filename and allowed_file(photo.filename):
            print(f"Processing photo: {photo.filename}")  # Debug
            
            # Generate unique filename
            filename = secure_filename(photo.filename)
            unique_filename = str(uuid.uuid4()) + '_' + filename
            
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'profile_photos')
            os.makedirs(upload_dir, exist_ok=True)
            print(f"Upload directory: {upload_dir}")  # Debug
            
            # Save file
            file_path = os.path.join(upload_dir, unique_filename)
            photo.save(file_path)
            print(f"Photo saved to: {file_path}")  # Debug
            
            # Verify file was saved
            if os.path.exists(file_path):
                print(f"File verification successful: {file_path}")  # Debug
                return unique_filename
            else:
                print(f"File verification failed: {file_path}")  # Debug
                return None
        else:
            print(f"Invalid photo or filename: {photo}, {photo.filename if photo else 'None'}")  # Debug
            return None
    except Exception as e:
        print(f"Error saving photo: {str(e)}")  # Debug
        return None

@main.route('/debug_profile')
@login_required
def debug_profile():
    """Debug route to check profile photo functionality"""
    import os
    upload_dir = os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'profile_photos')
    
    debug_info = {
        'user_id': current_user.id,
        'user_name': current_user.name,
        'profile_photo': current_user.profile_photo,
        'upload_dir': upload_dir,
        'upload_dir_exists': os.path.exists(upload_dir),
        'files_in_upload_dir': os.listdir(upload_dir) if os.path.exists(upload_dir) else []
    }
    
    return f"<pre>{debug_info}</pre>"

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from app.forms import EditProfileForm
    form = EditProfileForm(obj=current_user)
    
    print(f"edit_profile route called with method: {request.method}")  # Debug
    
    if form.validate_on_submit():
        print("Form validation successful")  # Debug
        try:
            # Handle photo upload first
            if form.profile_photo.data:
                print(f"Photo data received: {form.profile_photo.data.filename}")  # Debug
                photo_filename = save_profile_photo(form.profile_photo.data)
                if photo_filename:
                    print(f"Photo saved as: {photo_filename}")  # Debug
                    # Delete old photo if it's not the default
                    if current_user.profile_photo and current_user.profile_photo != 'default_avatar.svg':
                        old_photo_path = os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'profile_photos', current_user.profile_photo)
                        if os.path.exists(old_photo_path):
                            os.remove(old_photo_path)
                            print(f"Deleted old photo: {current_user.profile_photo}")  # Debug
                    
                    current_user.profile_photo = photo_filename
                    print(f"Updated user profile_photo to: {current_user.profile_photo}")  # Debug
                else:
                    flash('Failed to upload photo. Please try again.', 'error')
            
            # Update other fields
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.organization = form.organization.data
            current_user.bio = form.bio.data
            
            if form.password.data:
                current_user.set_password(form.password.data)
            
            from app import db
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main.profile'))
            
        except Exception as e:
            print(f"Error updating profile: {str(e)}")  # Debug
            flash(f'Error updating profile: {str(e)}', 'error')
            from app import db
            db.session.rollback()
    else:
        if request.method == 'POST':
            print(f"Form validation failed. Errors: {form.errors}")  # Debug
    
    return render_template('edit_profile.html', form=form)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'producer':
        applications = Application.query.filter_by(producer_id=current_user.id).all()
        return render_template('dashboard.html', applications=applications)
    
    elif current_user.role == 'auditor':
        applications = Application.query.filter_by(status='pending').all()
        return render_template('dashboard.html', applications=applications)
    
    elif current_user.role == 'government':
        applications = Application.query.filter_by(status='auditor_verified').all()
        return render_template('dashboard.html', applications=applications)
    
    elif current_user.role == 'bank':
        applications = Application.query.filter_by(status='govt_approved').all()
        transactions = Transaction.query.filter_by(bank_id=current_user.id).all()
        return render_template('dashboard.html', applications=applications, transactions=transactions)
    
    return render_template('dashboard.html')

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404