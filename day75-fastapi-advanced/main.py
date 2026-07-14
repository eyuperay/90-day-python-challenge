#!/usr/bin/env python3
"""
Day 75 - FastAPI Advanced
Advanced API with CRUD operations using FastAPI
"""

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import engine, get_db, Base
from models import Product, Customer, Order
from schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    CustomerCreate, CustomerUpdate, CustomerResponse,
    OrderCreate, OrderUpdate, OrderResponse
)
from crud import (
    create_product, get_product, get_products, update_product, delete_product,
    create_customer, get_customer, get_customers, update_customer, delete_customer,
    create_order, get_order, get_orders, update_order, delete_order
)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Advanced API",
    description="Advanced API with CRUD operations for products, customers, and orders",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== ROOT ENDPOINT ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Advanced API",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "products": "/products",
            "customers": "/customers",
            "orders": "/orders"
        }
    }


# ==================== PRODUCT ENDPOINTS ====================

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    return create_product(db, product)


@app.get("/products", response_model=List[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all products with optional category filter"""
    return get_products(db, skip=skip, limit=limit, category=category)


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product_by_id(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update product by ID"""
    product = update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Delete product by ID (soft delete)"""
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")


# ==================== CUSTOMER ENDPOINTS ====================

@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    return create_customer(db, customer)


@app.get("/customers", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all customers"""
    return get_customers(db, skip=skip, limit=limit)


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    """Get customer by ID"""
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer_by_id(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Update customer by ID"""
    customer = update_customer(db, customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    """Delete customer by ID"""
    if not delete_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")


# ==================== ORDER ENDPOINTS ====================

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order with items"""
    return create_order(db, order)


@app.get("/orders", response_model=List[OrderResponse])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List all orders with optional customer filter"""
    return get_orders(db, skip=skip, limit=limit, customer_id=customer_id)


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """Get order by ID"""
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order_by_id(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Update order by ID"""
    order = update_order(db, order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """Delete order by ID"""
    if not delete_order(db, order_id):
        raise HTTPException(status_code=404, detail="Order not found")


# ==================== SEARCH ENDPOINT ====================

@app.get("/search")
async def search_products(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Search products by name or description"""
    results = db.query(Product).filter(
        (Product.name.contains(q)) | (Product.description.contains(q))
    ).all()
    
    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# ==================== STATS ENDPOINT ====================

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get API statistics"""
    product_count = db.query(Product).filter(Product.is_active == True).count()
    customer_count = db.query(Customer).count()
    order_count = db.query(Order).count()
    
    # Total revenue
    total_revenue = db.query(Order).filter(Order.status == "completed").with_entities(
        Order.total_amount
    ).all()
    total_revenue = sum(r[0] for r in total_revenue) if total_revenue else 0
    
    return {
        "total_products": product_count,
        "total_customers": customer_count,
        "total_orders": order_count,
        "total_revenue": round(total_revenue, 2)
    }


# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
