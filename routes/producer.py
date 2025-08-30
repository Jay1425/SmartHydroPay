from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import Application, Milestone, SubsidyPolicy
from app.forms import ApplicationForm, MilestoneForm
import os, json
from werkzeug.utils import secure_filename
from datetime import datetime

producer = Blueprint('producer', __name__)

@producer.before_request
@login_required
def require_producer():
    if current_user.role != 'producer':
        abort(403)

@producer.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    
    # Populate technology choices from subsidy policies
    policies = SubsidyPolicy.query.all()
    tech_choices = [(p.technology_type, p.technology_type.replace('_', ' ').title()) for p in policies]
    form.technology_type.choices = tech_choices
    
    if form.validate_on_submit():
        # Handle file uploads
        doc_files = []
        
        # Handle environmental clearance file
        if form.environmental_clearance_file.data:
            file = form.environmental_clearance_file.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'environmental', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            doc_files.append(f'uploads/environmental/{filename}')
        
        # Handle feasibility report file
        if form.feasibility_report_file.data:
            file = form.feasibility_report_file.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'feasibility', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            doc_files.append(f'uploads/feasibility/{filename}')
        
        # Handle additional document files
        files = request.files.getlist('document_files')
        for file in files:
            if file and hasattr(file, 'filename') and file.filename:
                filename = secure_filename(file.filename)
                upload_path = os.path.join('static', 'uploads', 'documents', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                doc_files.append(f'uploads/documents/{filename}')
        
        # Create comprehensive application
        application = Application(
            producer_id=current_user.id,
            project_name=form.project_name.data,
            project_title=form.project_title.data,
            project_description=form.project_description.data,
            technology_type=form.technology_type.data,
            capacity_mw=form.capacity_mw.data,
            capacity_tons=form.capacity_tons.data,
            project_location=form.project_location.data,
            project_latitude=form.project_latitude.data,
            project_longitude=form.project_longitude.data,
            capex_estimate=form.capex_estimate.data,
            opex_estimate=form.opex_estimate.data,
            expected_completion_date=form.expected_completion_date.data,
            environmental_clearance=form.environmental_clearance.data,
            land_acquisition_status=form.land_acquisition_status.data,
            power_supply_arrangement=form.power_supply_arrangement.data,
            water_source=form.water_source.data,
            documents=json.dumps(doc_files),
            # Legacy fields for backward compatibility
            capacity=form.capacity_mw.data,
            project_details=form.project_description.data,
            status='pending'
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Comprehensive application submitted successfully! Your application is now under review.', 'success')
        return redirect(url_for('producer.my_applications'))
    
    return render_template('apply_form_comprehensive.html', form=form)

@producer.route('/my_applications')
def my_applications():
    applications = Application.query.filter_by(producer_id=current_user.id).order_by(Application.created_at.desc()).all()
    return render_template('my_applications_enhanced.html', applications=applications)

@producer.route('/application/<int:app_id>/milestones', methods=['GET', 'POST'])
def manage_milestones(app_id):
    application = Application.query.get_or_404(app_id)
    
    # Ensure the application belongs to the current producer
    if application.producer_id != current_user.id:
        abort(403)
    
    form = MilestoneForm()
    
    if form.validate_on_submit():
        # Handle milestone document upload
        milestone_doc = None
        if form.milestone_document.data:
            file = form.milestone_document.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'uploads', 'milestones', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            milestone_doc = f'uploads/milestones/{filename}'
        
        milestone = Milestone(
            application_id=application.id,
            milestone_name=form.milestone_name.data,
            milestone_description=form.milestone_description.data,
            planned_completion_date=form.planned_completion_date.data,
            milestone_percentage=form.milestone_percentage.data,
            milestone_amount=form.milestone_amount.data,
            milestone_document_path=milestone_doc,
            status='planned'
        )
        
        db.session.add(milestone)
        db.session.commit()
        
        flash('Milestone created successfully!', 'success')
        return redirect(url_for('producer.manage_milestones', app_id=app_id))
    
    milestones = Milestone.query.filter_by(application_id=app_id).order_by(Milestone.milestone_percentage).all()
    return render_template('manage_milestones.html', application=application, milestones=milestones, form=form)

@producer.route('/milestone/<int:milestone_id>/update', methods=['POST'])
def update_milestone(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    
    # Ensure the milestone belongs to the current producer's application
    if milestone.application.producer_id != current_user.id:
        abort(403)
    
    if request.form.get('action') == 'complete':
        milestone.status = 'completed'
        milestone.actual_completion_date = datetime.utcnow()
        
        # Handle completion document upload
        if 'completion_document' in request.files:
            file = request.files['completion_document']
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_path = os.path.join('static', 'uploads', 'milestone_completions', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                milestone.completion_document_path = f'uploads/milestone_completions/{filename}'
        
        db.session.commit()
        flash('Milestone marked as completed!', 'success')
    
    return redirect(url_for('producer.manage_milestones', app_id=milestone.application_id))

@producer.route('/profile/update', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        # Update company information
        current_user.company_name = request.form.get('company_name', current_user.company_name)
        current_user.registration_number = request.form.get('registration_number', current_user.registration_number)
        current_user.gst_number = request.form.get('gst_number', current_user.gst_number)
        current_user.contact_person = request.form.get('contact_person', current_user.contact_person)
        
        # Update bank details
        current_user.bank_account_number = request.form.get('bank_account_number', current_user.bank_account_number)
        current_user.bank_name = request.form.get('bank_name', current_user.bank_name)
        current_user.ifsc_code = request.form.get('ifsc_code', current_user.ifsc_code)
        
        # Update contact details
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.bio = request.form.get('bio', current_user.bio)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('edit_profile.html', user=current_user)
