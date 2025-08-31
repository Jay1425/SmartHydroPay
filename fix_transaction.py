#!/usr/bin/env python3
"""
Quick script to add comments column to transaction table
"""
from app import create_app, db

def add_comments_column():
    app = create_app()
    
    with app.app_context():
        try:
            # Use raw SQL with connection.execute() and quote the table name
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE "transaction" ADD COLUMN comments TEXT'))
                conn.commit()
            print("Added comments column to transaction table successfully!")
        except Exception as e:
            print(f"Error or column already exists: {e}")

if __name__ == '__main__':
    add_comments_column()
