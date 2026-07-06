from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:
    @staticmethod
    def get_customers(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None
    ):
        query = db.query(Customer)
        if search:
            query = query.filter(
                (Customer.first_name.ilike(f"%{search}%")) |
                (Customer.last_name.ilike(f"%{search}%")) |
                (Customer.email.ilike(f"%{search}%")) |
                (Customer.company.ilike(f"%{search}%"))
            )
        if status:
            query = query.filter(Customer.status == status)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_customer_by_id(db: Session, customer_id: int):
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        db_customer = Customer(**customer.model_dump())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not db_customer:
            return None
        for key, value in customer.model_dump(exclude_unset=True).items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return False
        db.delete(customer)
        db.commit()
        return True