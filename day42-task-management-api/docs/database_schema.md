# Database Schema

## users
- id
- email
- hashed_password
- full_name
- is_active
- is_superuser

## projects
- id
- name
- description
- owner_id

## tasks
- id
- title
- description
- status
- priority
- project_id
- assignee_id

## comments
- id
- content
- task_id
- author_id

## inventory
- id
- name
- sku
- quantity
- location