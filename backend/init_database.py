"""
Script to initialize database tables.
Can be run manually to create tables if they don't exist.
"""
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.database import init_db, engine, DATABASE_URL
from sqlalchemy import inspect

def main():
    """Initialize database tables."""
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)
    print(f"Database URL: {DATABASE_URL[:50]}..." if len(DATABASE_URL) > 50 else f"Database URL: {DATABASE_URL}")
    print()
    
    # Check current tables
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"Existing tables: {existing_tables}")
        print()
    except Exception as e:
        print(f"⚠️  Error checking existing tables: {e}")
        print()
    
    # Initialize database
    print("Initializing database tables...")
    try:
        init_db()
        print("✓ Database tables initialized successfully!")
        print()
        
        # Verify tables were created
        inspector = inspect(engine)
        new_tables = inspector.get_table_names()
        print(f"Tables after initialization: {new_tables}")
        print()
        
        expected_tables = ["users", "user_profiles", "user_cvs"]
        missing_tables = [table for table in expected_tables if table not in new_tables]
        
        if missing_tables:
            print(f"⚠️  Warning: Some expected tables are missing: {missing_tables}")
        else:
            print("✓ All expected tables exist:")
            for table in expected_tables:
                print(f"  - {table}")
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Database initialization complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

