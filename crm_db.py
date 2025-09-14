# crm_db.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    total_purchases = Column(Float, default=0.0)  # synthetic feature for churn model
    avg_session_time = Column(Float, default=0.0) # synthetic feature
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text, default="")

def get_session(db_path="sqlite:///crm.db"):
    engine = create_engine(db_path, echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    return Session()
