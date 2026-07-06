import random
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.product import Product
from app.models.inventory import Inventory
from app.core.security import get_password_hash

def seed_database():
    db = SessionLocal()
    
    try:
        # Admin kullanıcı oluştur
        admin = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        
        # Kategoriler oluştur
        categories = [
            Category(name="Electronics", description="Electronic devices and accessories"),
            Category(name="Clothing", description="Apparel and fashion items"),
            Category(name="Books", description="Books and publications"),
            Category(name="Home & Garden", description="Home improvement and garden supplies"),
        ]
        
        for cat in categories:
            db.add(cat)
        
        db.commit()
        
        # Örnek ürünler oluştur
        products_data = [
            {"name": "Laptop", "sku": "LAP001", "price": 999.99, "stock_quantity": 10},
            {"name": "Smartphone", "sku": "PHN001", "price": 699.99, "stock_quantity": 25},
            {"name": "Headphones", "sku": "AUD001", "price": 49.99, "stock_quantity": 50},
            {"name": "T-Shirt", "sku": "CLT001", "price": 19.99, "stock_quantity": 100},
            {"name": "Python Book", "sku": "BOK001", "price": 39.99, "stock_quantity": 30},
            {"name": "Wireless Mouse", "sku": "MOU001", "price": 29.99, "stock_quantity": 75},
            {"name": "Keyboard", "sku": "KEY001", "price": 59.99, "stock_quantity": 40},
            {"name": "Monitor", "sku": "MON001", "price": 299.99, "stock_quantity": 15},
        ]
        
        for data in products_data:
            product = Product(
                name=data["name"],
                sku=data["sku"],
                price=data["price"],
                stock_quantity=data["stock_quantity"],
                category_id=random.randint(1, 4)
            )
            db.add(product)
            db.flush()
            
            # Envanter oluştur
            inventory = Inventory(
                product_id=product.id,
                quantity=data["stock_quantity"],
                available_quantity=data["stock_quantity"],
                reserved_quantity=0,
                reorder_point=10
            )
            db.add(inventory)
        
        db.commit()
        print("✅ Veritabanı başarıyla dolduruldu!")
        print("📊 Admin kullanıcı oluşturuldu:")
        print("   👤 Kullanıcı adı: admin")
        print("   🔑 Şifre: admin123")
        print(f"📦 {len(products_data)} ürün eklendi")
        print(f"📁 {len(categories)} kategori eklendi")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()