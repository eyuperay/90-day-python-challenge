from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    VIP = "vip"
    POTENTIAL = "potential"

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    company = Column(String(255))
    position = Column(String(100))
    status = Column(Enum(CustomerStatus), default=CustomerStatus.POTENTIAL)
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    revenue = Column(Float, default=0)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    assigned_to = relationship("User", back_populates="customers")
    interactions = relationship("Interaction", back_populates="customer")
    deals = relationship("Deal", back_populates="customer")
    tasks = relationship("Task", back_populates="customer")