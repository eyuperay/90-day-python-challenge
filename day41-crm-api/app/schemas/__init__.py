"""Pydantic schemas for CRM API."""
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.schemas.deal import DealCreate, DealUpdate, DealResponse
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse