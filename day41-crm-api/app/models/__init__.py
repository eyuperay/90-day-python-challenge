"""Database models for CRM API."""
from app.models.user import User, UserRole
from app.models.customer import Customer, CustomerStatus
from app.models.lead import Lead, LeadStatus, LeadSource
from app.models.interaction import Interaction, InteractionType
from app.models.deal import Deal, DealStage
from app.models.task import Task, TaskPriority, TaskStatus