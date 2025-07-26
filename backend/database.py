from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
from models import Base

# Load environment variables
load_dotenv()

# Database configuration
# Try PostgreSQL first, fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce_chatbot.db")

# If using PostgreSQL, uncomment the line below and comment the SQLite line above
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ecommerce_chatbot")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
    except SQLAlchemyError as e:
        print(f"❌ Error creating tables: {e}")
        raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test connection and create tables
    if test_connection():
        create_tables()
