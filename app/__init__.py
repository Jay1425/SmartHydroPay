from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # Add Jinja2 filter for currency formatting
    @app.template_filter('format_currency')
    def format_currency(value):
        try:
            return "₹{:,.2f}".format(float(value))
        except Exception:
            return value
    
    # Configuration
    app.config['SECRET_KEY'] = 'a810f367e2a8296a40a7a4073b64f92476d542023a968f44d32e92e21255e427'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smarthydropay.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'aivisionaries.teams@gmail.com'
    app.config['MAIL_PASSWORD'] = 'rves fkcw ikpq mbmw'
    
    # File upload configuration
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'static', 'uploads')
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Create tables first
    with app.app_context():
        # Import models
        from app.models import User, Application, Audit, Transaction
        db.create_all()
    
    # Register blueprints
    from routes.auth import auth
    from routes.producer import producer
    from routes.auditor import auditor
    from routes.government import government
    from routes.bank import bank
    from routes.main import main
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(producer, url_prefix='/producer')
    app.register_blueprint(auditor, url_prefix='/auditor')

    # Add Jinja2 filter for JSON parsing
    import json
    @app.template_filter('loads')
    def jinja2_loads_filter(s):
        try:
            return json.loads(s)
        except Exception:
            return []
    app.register_blueprint(government, url_prefix='/government')
    app.register_blueprint(bank, url_prefix='/bank')
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
