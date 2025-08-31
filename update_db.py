#!/usr/bin/env python3
"""
Database update script to add new fields to User and Transaction models
"""
from app import create_app, db
from app.models import User, Transaction
from sqlalchemy import text

def update_database():
    app = create_app()
    
    with app.app_context():
        # Check if user table columns exist and add them if they don't
        inspector = db.inspect(db.engine)
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        
        print("Current columns in user table:", user_columns)
        
        # Add new user columns if they don't exist
        if 'phone' not in user_columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN phone VARCHAR(15)'))
                print("Added phone column")
            except Exception as e:
                print(f"Error adding phone column: {e}")
        
        if 'organization' not in user_columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN organization VARCHAR(200)'))
                print("Added organization column")
            except Exception as e:
                print(f"Error adding organization column: {e}")
        
        if 'bio' not in user_columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN bio TEXT'))
                print("Added bio column")
            except Exception as e:
                print(f"Error adding bio column: {e}")
        
        if 'profile_photo' not in user_columns:
            try:
                db.engine.execute(text("ALTER TABLE user ADD COLUMN profile_photo VARCHAR(200) DEFAULT 'default_avatar.svg'"))
                print("Added profile_photo column")
            except Exception as e:
                print(f"Error adding profile_photo column: {e}")
        
        if 'created_at' not in user_columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
                print("Added created_at column")
            except Exception as e:
                print(f"Error adding created_at column: {e}")
        
        if 'updated_at' not in user_columns:
            try:
                db.engine.execute(text('ALTER TABLE user ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
                print("Added updated_at column")
            except Exception as e:
                print(f"Error adding updated_at column: {e}")
        
        # Check if transaction table exists and add comments column
        try:
            transaction_columns = [col['name'] for col in inspector.get_columns('transaction')]
            print("Current columns in transaction table:", transaction_columns)
            
            if 'comments' not in transaction_columns:
                try:
                    db.engine.execute(text('ALTER TABLE transaction ADD COLUMN comments TEXT'))
                    print("Added comments column to transaction table")
                except Exception as e:
                    print(f"Error adding comments column: {e}")
        except Exception as e:
            print(f"Transaction table doesn't exist yet: {e}")
        
        # Commit changes
        db.session.commit()
        print("Database updated successfully!")

if __name__ == '__main__':
    update_database()
