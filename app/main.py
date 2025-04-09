from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@db:3306/fastapi_db")

# Define retry parameters
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

# Initialize engine with connection pooling settings
def get_engine():
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt+1}/{MAX_RETRIES})...")
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
            return engine
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
    
    logger.error(f"Failed to connect to database after {MAX_RETRIES} attempts")
    raise Exception("Database connection failed")

# Create engine with retry
engine = None
SessionLocal = None
Base = declarative_base()

# Define a model
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(255))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="FastAPI with MySQL")

@app.on_event("startup")
async def startup():
    global engine, SessionLocal
    
    # Initialize database connection
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

@app.get("/")
def read_root():
    return {"message": "FastAPI with MySQL and PHPMyAdmin"}

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

@app.post("/items/")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item 