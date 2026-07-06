from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to_id: Optional[int] = None,
        customer_id: Optional[int] = None
    ):
        query = db.query(Task)
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if assigned_to_id:
            query = query.filter(Task.assigned_to_id == assigned_to_id)
        if customer_id:
            query = query.filter(Task.customer_id == customer_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def create_task(db: Session, task: TaskCreate):
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def update_task(db: Session, task_id: int, task: TaskUpdate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        if task.status == "completed" and db_task.status != "completed":
            task.completed_at = datetime.now()
        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def delete_task(db: Session, task_id: int):
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        db.delete(task)
        db.commit()
        return True