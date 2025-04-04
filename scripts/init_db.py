import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from api.database import engine, Base
from api.models.db_models import User
from api.auth.utils import get_password_hash

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a default admin user if it doesn't exist
    from sqlalchemy.orm import Session
    from api.database import SessionLocal

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@medbot.com").first()
        if not admin:
            admin = User(
                email="admin@medbot.com",
                username="admin",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),  # Change this in production
                is_active=True,
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("Created default admin user")
        else:
            print("Admin user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database initialization complete!") 