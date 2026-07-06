# Database Schema

## Tables

### Users
- id (PK)
- email (unique)
- username (unique)
- hashed_password
- full_name
- role (admin/employee/customer)
- is_active
- created_at
- updated_at

### Categories
- id (PK)
- name (unique)
- description
- is_active

### Products
- id (PK)
- name
- description
- sku (unique)
- price
- cost
- stock_quantity
- is_active
- category_id (FK)
- created_at
- updated_at

### Orders
- id (PK)
- order_number (unique)
- status (pending/processing/completed/cancelled)
- total_amount
- customer_name
- customer_email
- shipping_address
- user_id (FK)
- created_at

### Order Items
- id (PK)
- order_id (FK)
- product_id (FK)
- quantity
- price

### Inventory
- id (PK)
- product_id (FK, unique)
- quantity
- reserved_quantity
- available_quantity
- reorder_point
- last_updated

### Inventory Logs
- id (PK)
- inventory_id (FK)
- user_id (FK)
- action
- quantity_change
- previous_quantity
- new_quantity
- notes
- created_at