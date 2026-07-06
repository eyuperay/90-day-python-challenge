import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole

# Test veritabanı (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Test istemcisi fixture'ı"""
    # Test veritabanını oluştur
    Base.metadata.create_all(bind=engine)
    
    # Test kullanıcısı oluştur
    db = TestingSessionLocal()
    test_user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("test123"),
        role=UserRole.EMPLOYEE
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    yield TestClient(app)
    
    # Test veritabanını temizle
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def admin_client():
    """Admin test istemcisi fixture'ı"""
    # Test veritabanını oluştur
    Base.metadata.create_all(bind=engine)
    
    # Admin kullanıcısı oluştur
    db = TestingSessionLocal()
    admin_user = User(
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin_user)
    db.commit()
    db.close()
    
    yield TestClient(app)
    
    # Test veritabanını temizle
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_token(client):
    """Test kullanıcısı için token fixture'ı"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    return response.json().get("access_token")

@pytest.fixture
def admin_token(admin_client):
    """Admin kullanıcısı için token fixture'ı"""
    response = admin_client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    return response.json().get("access_token")