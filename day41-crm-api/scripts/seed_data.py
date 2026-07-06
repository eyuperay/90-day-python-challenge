import random
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.user import User, UserRole
from app.models.customer import Customer, CustomerStatus
from app.models.lead import Lead, LeadStatus, LeadSource
from app.models.deal import Deal, DealStage
from app.models.interaction import Interaction, InteractionType
from app.models.task import Task, TaskPriority, TaskStatus
from app.core.security import get_password_hash
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    
    try:
        print("🌱 Seed data ekleniyor...")
        
        # Admin kullanıcı oluştur
        admin = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        print("✅ Admin oluşturuldu")
        
        # Sales kullanıcısı oluştur
        sales = User(
            username="sales",
            email="sales@example.com",
            full_name="Sales User",
            hashed_password=get_password_hash("sales123"),
            role=UserRole.SALES
        )
        db.add(sales)
        print("✅ Sales oluşturuldu")
        
        # Support kullanıcısı oluştur
        support = User(
            username="support",
            email="support@example.com",
            full_name="Support User",
            hashed_password=get_password_hash("support123"),
            role=UserRole.SUPPORT
        )
        db.add(support)
        print("✅ Support oluşturuldu")
        
        db.commit()
        print("✅ Kullanıcılar kaydedildi")
        
        # Müşteriler oluştur
        customers_data = [
            {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "company": "Tech Corp"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com", "company": "Design Inc"},
            {"first_name": "Alice", "last_name": "Johnson", "email": "alice@example.com", "company": "Data Solutions"},
            {"first_name": "Bob", "last_name": "Williams", "email": "bob@example.com", "company": "Cloud Systems"},
            {"first_name": "Eva", "last_name": "Brown", "email": "eva@example.com", "company": "AI Innovations"},
            {"first_name": "Michael", "last_name": "Davis", "email": "michael@example.com", "company": "Tech Solutions"},
            {"first_name": "Sarah", "last_name": "Wilson", "email": "sarah@example.com", "company": "Creative Labs"},
            {"first_name": "David", "last_name": "Martinez", "email": "david@example.com", "company": "Data Systems"},
            {"first_name": "Lisa", "last_name": "Anderson", "email": "lisa@example.com", "company": "Cloud Nine"},
            {"first_name": "James", "last_name": "Thomas", "email": "james@example.com", "company": "AI Ventures"},
        ]
        
        for data in customers_data:
            customer = Customer(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                company=data["company"],
                status=random.choice([CustomerStatus.ACTIVE, CustomerStatus.VIP, CustomerStatus.POTENTIAL]),
                assigned_to_id=random.choice([admin.id, sales.id])
            )
            db.add(customer)
        
        db.commit()
        print(f"✅ {len(customers_data)} müşteri eklendi")
        
        # Lead'ler oluştur
        leads_data = [
            {"first_name": "Mike", "last_name": "Taylor", "email": "mike@example.com", "company": "Startup X"},
            {"first_name": "Sarah", "last_name": "Davis", "email": "sarah@example.com", "company": "Enterprise Y"},
            {"first_name": "Tom", "last_name": "Wilson", "email": "tom@example.com", "company": "Scale Z"},
            {"first_name": "Emily", "last_name": "Clark", "email": "emily@example.com", "company": "Growth Inc"},
            {"first_name": "Daniel", "last_name": "Rodriguez", "email": "daniel@example.com", "company": "Future Systems"},
            {"first_name": "Laura", "last_name": "Lee", "email": "laura@example.com", "company": "Innovation Hub"},
        ]
        
        for data in leads_data:
            lead = Lead(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                company=data["company"],
                status=random.choice([LeadStatus.NEW, LeadStatus.CONTACTED, LeadStatus.QUALIFIED]),
                source=random.choice([LeadSource.WEBSITE, LeadSource.REFERRAL, LeadSource.SOCIAL_MEDIA]),
                score=random.randint(0, 100),
                assigned_to_id=random.choice([admin.id, sales.id])
            )
            db.add(lead)
        
        db.commit()
        print(f"✅ {len(leads_data)} lead eklendi")
        
        # Deal'ler oluştur
        customers = db.query(Customer).all()
        deals_data = [
            {"name": "Enterprise Deal - Tech Corp", "amount": 50000},
            {"name": "Design Package - Design Inc", "amount": 15000},
            {"name": "Data Solutions Contract", "amount": 25000},
            {"name": "Cloud Migration Project", "amount": 75000},
            {"name": "AI Development Deal", "amount": 100000},
        ]
        
        for data in deals_data:
            if customers:
                deal = Deal(
                    name=data["name"],
                    amount=data["amount"],
                    stage=random.choice([DealStage.PROSPECTING, DealStage.QUALIFICATION, DealStage.PROPOSAL, DealStage.NEGOTIATION]),
                    probability=random.randint(0, 100),
                    customer_id=random.choice(customers).id,
                    assigned_to_id=random.choice([admin.id, sales.id])
                )
                db.add(deal)
        
        db.commit()
        print(f"✅ {len(deals_data)} anlaşma eklendi")
        
        print("🎉 Veritabanı başarıyla dolduruldu!")
        print("📊 Kullanıcılar:")
        print("   👤 Admin: admin/admin123")
        print("   👤 Sales: sales/sales123")
        print("   👤 Support: support/support123")
        print(f"📦 {len(customers_data)} müşteri eklendi")
        print(f"📋 {len(leads_data)} lead eklendi")
        print(f"💰 {len(deals_data)} anlaşma eklendi")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()