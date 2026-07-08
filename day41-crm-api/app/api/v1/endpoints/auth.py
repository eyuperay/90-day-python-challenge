from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu kullanıcı adı veya email zaten kayıtlı"
        )
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ============================================================
# YENİ login FONKSİYONU (JSON KABUL EDER)
# ============================================================
@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    JSON formatında kullanıcı girişi.
    """
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz kullanıcı adı veya şifre",
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# ============================================================
# ESKİ login FONKSİYONU (YORUMLANDI - İSTEĞE BAĞLI KALDIR)
# ============================================================
# @router.post("/login", response_model=Token)
# async def login_old(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Geçersiz kullanıcı adı veya şifre",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(
#         data={"sub": str(user.id), "username": user.username}
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user