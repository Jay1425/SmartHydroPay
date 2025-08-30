"# SmartHydroPay - Green Hydrogen Subsidy Management System

A Flask web application for managing green hydrogen project subsidies with role-based access control for Government Bodies, Producers, Auditors, and Banks.

## Features

### 🏛️ **Government Body**
- Review auditor-verified applications
- Approve or reject subsidy applications
- Monitor fund allocation and project progress
- Dashboard with approval statistics

### 🏭 **Green Hydrogen Producer/Startup**
- Submit subsidy applications with project details
- Track application status in real-time
- View application history and progress
- Upload project documentation

### 🔍 **Auditor** 
- Review and verify producer applications
- Add audit comments and recommendations
- Mark applications as verified/unverified
- Ensure compliance with subsidy criteria

### 🏦 **Bank**
- Disburse approved subsidy funds
- Process fund release transactions
- View transaction history
- Manage pending fund releases

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 templates with TailwindCSS
- **Authentication**: Flask-Login with role-based access
- **Forms**: Flask-WTF with validation

## Project Structure

```
SmartHydroPay/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   └── forms.py             # Form definitions
├── routes/
│   ├── auth.py              # Authentication routes
│   ├── producer.py          # Producer routes
│   ├── auditor.py           # Auditor routes
│   ├── government.py        # Government routes
│   ├── bank.py              # Bank routes
│   └── main.py              # Main routes
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template
│   ├── dashboard.html      # Role-specific dashboards
│   ├── login.html          # Login page
│   ├── signup.html         # Registration page
│   └── [other templates]
├── static/
│   └── style.css           # Custom CSS
├── requirements.txt        # Python dependencies
├── run.py                 # Application entry point
└── init_db.py            # Database initialization
```

## Installation & Setup

### 1. Clone or Extract the Project
```bash
cd SmartHydroPay
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python init_db.py
```

This will create sample users for testing:
- **Government**: gov@smarthydropay.com / password123
- **Producer**: producer@example.com / password123  
- **Auditor**: auditor@example.com / password123
- **Bank**: bank@example.com / password123

### 5. Run the Application
```bash
python run.py
```

The application will be available at: `http://localhost:5000`

## Usage Workflow

### 1. **Producer Flow**
1. Login as producer
2. Submit new application with project details
3. Track application status in dashboard
4. Receive notifications on status updates

### 2. **Auditor Flow**  
1. Login as auditor
2. Review pending applications
3. Add audit comments and verification status
4. Mark applications as verified/rejected

### 3. **Government Flow**
1. Login as government officer
2. Review auditor-verified applications
3. View detailed project information and audit reports
4. Approve or reject applications

### 4. **Bank Flow**
1. Login as bank officer
2. View government-approved applications
3. Process fund release with specified amounts
4. Track transaction history

## Database Models

### User
- id, name, email, password_hash, role
- Supports four roles: government, producer, auditor, bank

### Application  
- id, producer_id, project_name, capacity, documents, status
- Status flow: pending → auditor_verified → govt_approved → fund_released

### Audit
- id, application_id, auditor_id, comments, verified

### Transaction
- id, bank_id, application_id, amount, date

## Security Features

- Password hashing using Werkzeug
- Session-based authentication with Flask-Login  
- Role-based access control
- CSRF protection with Flask-WTF
- Input validation and sanitization

## Test the Application

Sample users for testing:
- **Government**: gov@smarthydropay.com / password123
- **Producer**: producer@example.com / password123  
- **Auditor**: auditor@example.com / password123
- **Bank**: bank@example.com / password123

---

**SmartHydroPay** - Accelerating India's Green Hydrogen Revolution through Smart Subsidy Management 🌱" 
