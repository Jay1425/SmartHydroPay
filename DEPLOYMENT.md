# SmartHydroPay - Deployment Guide

## 🚀 Quick Start

### Option 1: Local Development
```bash
# Clone repository
git clone https://github.com/Jay1425/SmartHydroPay.git
cd SmartHydroPay

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up database
flask db init
flask db migrate -m "Initial migration" 
flask db upgrade

# Populate sample data
python populate_data.py

# Run application
python run.py
```

### Option 2: Production Deployment

#### Environment Variables (.env)
```env
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password
FLASK_ENV=production
```

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

## 🔧 Configuration

### Gmail SMTP Setup
1. Enable 2-factor authentication on Gmail
2. Generate an App Password (16 characters)
3. Use the App Password in MAIL_PASSWORD (not your regular password)

### Database Options
- **Development**: SQLite (default)
- **Production**: PostgreSQL recommended
- **Docker**: PostgreSQL container

## 📊 Sample Data

After running `populate_data.py`, you get:
- **10 Users** across all roles
- **5 Applications** in various stages
- **3 Audit Records** with detailed reviews  
- **1 Transaction** for fund release

### Test Login Credentials
**Password**: `password123` (for all users)

**Roles Available**:
- Government: `sarah.johnson@gov.in`
- Producer: `projects@adanigreen.com`
- Auditor: `priya.sharma@audit.in` 
- Bank: `renewable.finance@sbi.co.in`
- Admin: `admin@smarthydropay.gov.in`

## 🌐 Access URLs

- **Homepage**: http://localhost:5000
- **Login**: http://localhost:5000/auth/login
- **Dashboard**: http://localhost:5000/dashboard
- **404 Test**: http://localhost:5000/nonexistent-page

## 📱 Features to Test

### Authentication Flow
1. Register new user with OTP verification
2. Login with existing credentials
3. Password reset functionality

### Role-Based Features
- **Producer**: Submit applications, track status
- **Auditor**: Verify pending applications
- **Government**: Approve/reject applications
- **Bank**: Process fund releases

### UI Features
- Animated dashboard cards
- Responsive design on mobile
- Custom 404 error page
- Real-time status updates

## 🔍 Troubleshooting

### Common Issues

1. **OTP not received**
   - Check Gmail settings
   - Verify App Password
   - Check spam folder

2. **Database errors**
   - Run migrations: `flask db upgrade`
   - Reset database: Delete .db file and re-run migrations

3. **Module not found**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

### Error Logs
Check terminal output for detailed error messages.

## 🚢 Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Use PostgreSQL database  
- [ ] Enable HTTPS with SSL certificate
- [ ] Set up monitoring and logging
- [ ] Configure proper SMTP settings
- [ ] Set up backup procedures
- [ ] Configure firewall rules
- [ ] Set up domain and DNS

## 📞 Support

For technical support:
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check README.md for detailed information
- **Email**: Contact system administrator

---

**Happy Deploying!** 🎉
