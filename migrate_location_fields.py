#!/usr/bin/env python3
"""
Database Migration: Add Latitude and Longitude Fields
"""

from app import create_app, db
from app.models import Application
from sqlalchemy import text

def migrate_database():
    """Add latitude and longitude fields to Application model"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Adding latitude and longitude fields to Application table...")
        
        try:
            # Add new columns to existing table
            db.engine.execute(text("""
                ALTER TABLE application 
                ADD COLUMN project_latitude FLOAT NULL,
                ADD COLUMN project_longitude FLOAT NULL
            """))
            
            db.session.commit()
            print("✅ Successfully added latitude and longitude fields!")
            
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e):
                print("ℹ️  Latitude and longitude columns already exist, skipping...")
            else:
                print(f"❌ Error during migration: {str(e)}")
                db.session.rollback()
                raise

if __name__ == '__main__':
    migrate_database()
