"# SmartHydroPay - Green Hydrogen Subsidy Management System

## 🌱 Overview

SmartHydroPay is a comprehensive web-based platform for managing green hydrogen subsidy disbursement in India. The system streamlines the entire process from application submission to fund release, ensuring transparency, efficiency, and proper oversight.

## 🚀 Key Features

### Role-Based Access Control
- **Producers**: Submit subsidy applications, track status, manage projects
- **Auditors**: Verify and audit applications, provide technical assessments
- **Government**: Approve/reject applications, monitor policy compliance
- **Banks**: Process fund disbursements, manage transactions
- **Admin**: System administration and user management

### Advanced Functionality
- **Email OTP Authentication**: Secure login with Gmail-based OTP verification
- **Real-time Dashboard**: Role-specific dashboards with animated UI
- **Document Management**: Support for PDF uploads and technical documentation
- **Audit Trail**: Complete tracking of all actions and decisions
- **Responsive Design**: Modern UI with Tailwind CSS and custom animations
- **Database Migrations**: Flask-Migrate for schema management

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **Database**: SQLAlchemy with SQLite/PostgreSQL
- **Authentication**: Flask-Login with OTP verification
- **Email**: Flask-Mail with Gmail SMTP
- **Migrations**: Flask-Migrate
- **Forms**: Flask-WTF with CSRF protection

### Frontend
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **Animations**: Custom CSS3 animations with 3D effects
- **Templates**: Jinja2 with responsive design

### Security
- **CSRF Protection**: WTF-Forms integration
- **OTP Authentication**: Time-based email verification
- **Role-based Authorization**: Custom decorators
- **Session Management**: Secure Flask sessions

## 📁 Project Structure

```
SmartHydroPay/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   └── forms.py             # WTF-Forms definitions
├── routes/
│   ├── main.py              # Main routes (dashboard, profile)
│   ├── auth.py              # Authentication routes
│   ├── producer.py          # Producer-specific routes
│   ├── auditor.py           # Auditor-specific routes
│   ├── government.py        # Government routes
│   └── bank.py              # Banking routes
├── templates/
│   ├── base.html            # Base template
│   ├── dashboard.html       # Main dashboard
│   ├── login.html           # Login with OTP
│   ├── signup.html          # Registration
│   ├── 404.html            # Custom error page
│   └── ...                  # Role-specific templates
├── static/
│   └── style.css           # Custom styles
├── migrations/              # Database migrations
├── populate_data.py         # Sample data script
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Jay1425/SmartHydroPay.git
cd SmartHydroPay
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///smarthydropay.db
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-google-app-password
FLASK_ENV=development
```

### 5. Database Setup
```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 6. Populate Sample Data
```bash
python populate_data.py
```

### 7. Run the Application
```bash
python run.py
```

Visit `http://localhost:5000` to access the application.

## 👥 Test User Credentials

After running `populate_data.py`, you can log in with:

**Password for all users**: `password123`

### Government Users
- `sarah.johnson@gov.in` - Dr. Sarah Johnson (Ministry of New & Renewable Energy)
- `rajesh.kumar@gov.in` - Rajesh Kumar (Department of Science & Technology)

### Producer Companies  
- `projects@adanigreen.com` - Adani Green Energy Ltd
- `hydrogen@ril.com` - Reliance New Energy
- `green.energy@tatapower.com` - Tata Power Renewable

### Auditors
- `priya.sharma@audit.in` - Dr. Priya Sharma (Green Energy Certification Institute)
- `vikram.singh@bureau.gov.in` - Vikram Singh (Bureau of Energy Efficiency)

### Banks
- `renewable.finance@sbi.co.in` - State Bank of India
- `green.loans@hdfcbank.com` - HDFC Bank Green Finance

### Administrator
- `admin@smarthydropay.gov.in` - System Administrator

## 🔄 Application Workflow

1. **Producer Registration**: Companies register and create profiles
2. **Application Submission**: Submit detailed project proposals with documents
3. **Technical Audit**: Auditors verify technical specifications and compliance
4. **Government Review**: Policy officers review and approve/reject applications
5. **Fund Disbursement**: Banks process approved subsidies and update records
6. **Tracking & Reporting**: Real-time status updates and comprehensive reporting

## 🎨 UI Features

### Dashboard Highlights
- **Animated Cards**: 3D hover effects and smooth transitions
- **Status Badges**: Color-coded application statuses
- **Progress Indicators**: Visual tracking of application stages
- **Responsive Design**: Mobile-friendly interface

### Custom Animations
- **Particle Effects**: Floating particles on login/index pages
- **3D Transforms**: Card hover effects with perspective
- **Smooth Transitions**: Page transitions and loading states
- **Interactive Elements**: Animated buttons and form elements

## 🔒 Security Features

### Authentication & Authorization
- **OTP Verification**: Email-based one-time passwords
- **Role-based Access**: Granular permissions per user role
- **Session Security**: Secure session management
- **CSRF Protection**: Form submission protection

### Data Security
- **Encrypted Passwords**: Werkzeug password hashing
- **Secure Headers**: Security headers implementation
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📊 Database Schema

### Core Models
- **User**: Authentication and profile management
- **Application**: Subsidy applications with documents
- **Audit**: Technical verification records
- **Transaction**: Fund disbursement tracking

### Relationships
- Users can have multiple applications (Producer role)
- Applications can have multiple audits
- Approved applications generate transactions
- Complete audit trail for all operations

## 🌐 API Endpoints

### Authentication
- `POST /auth/login` - User login with OTP
- `POST /auth/signup` - User registration
- `POST /auth/verify-otp` - OTP verification
- `GET /auth/logout` - User logout

### Applications
- `GET /producer/apply` - Application form
- `POST /producer/apply` - Submit application
- `GET /producer/applications` - List user applications

### Administration
- `GET /auditor/applications` - Pending verifications
- `GET /government/applications` - Approval queue  
- `GET /bank/releases` - Fund release queue

## 🚀 Deployment

### Production Setup
1. **Environment Variables**: Set production configs
2. **Database**: Use PostgreSQL for production
3. **Web Server**: Deploy with Gunicorn + Nginx
4. **SSL**: Enable HTTPS with Let's Encrypt
5. **Monitoring**: Set up logging and monitoring

### Docker Deployment
```bash
# Build image
docker build -t smarthydropay .

# Run container
docker run -p 5000:5000 smarthydropay
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- **Email**: support@smarthydropay.gov.in
- **Issues**: GitHub Issues page
- **Documentation**: Wiki pages

## 🙏 Acknowledgments

- Ministry of New & Renewable Energy, Government of India
- National Green Hydrogen Mission
- Clean Energy Technology Partners
- Open Source Community Contributors

---

**SmartHydroPay** - Accelerating India's Green Hydrogen Revolution through Smart Technology 🌱⚡

# SmartHydroPay - Green Hydrogen Subsidy Management System

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
