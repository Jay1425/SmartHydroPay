from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smarthydropay.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # File upload configuration
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'static', 'uploads')
    
    # Initialize extensions
    db.init_app(app)
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
    app.register_blueprint(government, url_prefix='/government')
    app.register_blueprint(bank, url_prefix='/bank')
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
