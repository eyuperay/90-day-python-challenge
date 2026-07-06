from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    
    tasks = query.offset(skip).limit(limit).all()
    
    result = []
    for task in tasks:
        task_dict = task.__dict__.copy()
        task_dict['assigned_to_name'] = task.assigned_to.full_name if task.assigned_to else None
        task_dict['customer_name'] = task.customer.first_name + " " + task.customer.last_name if task.customer else None
        task_dict['lead_name'] = task.lead.first_name + " " + task.lead.last_name if task.lead else None
        result.append(TaskResponse(**task_dict))
    
    return result

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    
    task_dict = task.__dict__.copy()
    task_dict['assigned_to_name'] = task.assigned_to.full_name if task.assigned_to else None
    task_dict['customer_name'] = task.customer.first_name + " " + task.customer.last_name if task.customer else None
    task_dict['lead_name'] = task.lead.first_name + " " + task.lead.last_name if task.lead else None
    return TaskResponse(**task_dict)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SALES, UserRole.SUPPORT]))
):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    task_dict = db_task.__dict__.copy()
    task_dict['assigned_to_name'] = db_task.assigned_to.full_name if db_task.assigned_to else None
    task_dict['customer_name'] = db_task.customer.first_name + " " + db_task.customer.last_name if db_task.customer else None
    task_dict['lead_name'] = db_task.lead.first_name + " " + db_task.lead.last_name if db_task.lead else None
    return TaskResponse(**task_dict)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SALES, UserRole.SUPPORT]))
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    
    # If task is being completed, set completed_at
    if task.status == "completed" and db_task.status != "completed":
        task.completed_at = datetime.now()
    
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    
    task_dict = db_task.__dict__.copy()
    task_dict['assigned_to_name'] = db_task.assigned_to.full_name if db_task.assigned_to else None
    task_dict['customer_name'] = db_task.customer.first_name + " " + db_task.customer.last_name if db_task.customer else None
    task_dict['lead_name'] = db_task.lead.first_name + " " + db_task.lead.last_name if db_task.lead else None
    return TaskResponse(**task_dict)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    
    db.delete(task)
    db.commit()