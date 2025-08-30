#!/usr/bin/env python3
"""
Database update script to add new fields to User model
"""
from app import create_app, db
from app.models import User
from sqlalchemy import text

def update_database():
    app = create_app()
    
    with app.app_context():
        # Check if columns exist and add them if they don't
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('user')]
        
        print("Current columns in user table:", columns)
        
        # Add new columns if they don't exist
        if 'phone' not in columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN phone VARCHAR(15)'))
                print("Added phone column")
            except Exception as e:
                print(f"Error adding phone column: {e}")
        
        if 'organization' not in columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN organization VARCHAR(200)'))
                print("Added organization column")
            except Exception as e:
                print(f"Error adding organization column: {e}")
        
        if 'bio' not in columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN bio TEXT'))
                print("Added bio column")
            except Exception as e:
                print(f"Error adding bio column: {e}")
        
        if 'created_at' not in columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
                print("Added created_at column")
            except Exception as e:
                print(f"Error adding created_at column: {e}")
        
        if 'updated_at' not in columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
                print("Added updated_at column")
            except Exception as e:
                print(f"Error adding updated_at column: {e}")
        
        # Commit changes
        db.session.commit()
        print("Database updated successfully!")

if __name__ == '__main__':
    update_database()
