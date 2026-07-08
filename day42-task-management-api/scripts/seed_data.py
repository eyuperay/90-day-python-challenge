import asyncio

from sqlalchemy import select

from app.core.database import async_session_maker, init_db
from app.core.security import get_password_hash
from app.models.comment import Comment
from app.models.inventory import Inventory
from app.models.project import Project
from app.models.task import Task
from app.models.user import User


async def seed():
    await init_db()

    async with async_session_maker() as db:
        result = await db.execute(select(User).where(User.email == "admin@example.com"))
        admin = result.scalar_one_or_none()

        if admin is None:
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                is_superuser=True,
            )
            db.add(admin)
            await db.commit()
            await db.refresh(admin)

        result = await db.execute(select(Project).where(Project.name == "Demo Project"))
        project = result.scalar_one_or_none()
        if project is None:
            project = Project(name="Demo Project", description="Seed project", owner_id=admin.id)
            db.add(project)
            await db.commit()
            await db.refresh(project)

        result = await db.execute(select(Task).where(Task.title == "First Task"))
        task = result.scalar_one_or_none()
        if task is None:
            task = Task(
                title="First Task",
                description="Seed task",
                status="todo",
                priority="high",
                project_id=project.id,
                assignee_id=admin.id,
            )
            db.add(task)
            await db.commit()
            await db.refresh(task)

        result = await db.execute(select(Comment).where(Comment.content == "Welcome"))
        comment = result.scalar_one_or_none()
        if comment is None:
            comment = Comment(content="Welcome", task_id=task.id, author_id=admin.id)
            db.add(comment)

        result = await db.execute(select(Inventory).where(Inventory.sku == "SKU-001"))
        item = result.scalar_one_or_none()
        if item is None:
            item = Inventory(name="Laptop", sku="SKU-001", quantity=10, location="Istanbul")
            db.add(item)

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())