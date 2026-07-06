
---

### **57. docs/database_schema.md**
```markdown
# Database Schema - CRM API

## Tables

### Users
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Primary key |
| email | String(255) | Unique email |
| username | String(100) | Unique username |
| hashed_password | String(255) | Password hash |
| full_name | String(255) | Full name |
| role | Enum | admin/sales/support/viewer |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |

### Customers
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Primary key |
| first_name | String(100) | First name |
| last_name | String(100) | Last name |
| email | String(255) | Unique email |
| phone | String(20) | Phone number |
| company | String(255) | Company name |
| status | Enum | active/vip/potential |
| assigned_to_id | Integer (FK) | Assigned user |

### Leads
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Primary key |
| first_name | String(100) | First name |
| last_name | String(100) | Last name |
| email | String(255) | Unique email |
| status | Enum | new/contacted/qualified |
| source | Enum | website/referral |
| score | Integer | Lead score (0-100) |
| assigned_to_id | Integer (FK) | Assigned user |

### Interactions
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Primary key |
| interaction_type | Enum | call/email/meeting |
| subject | String(255) | Subject |
| description | Text | Description |
| customer_id | Integer (FK) | Related customer |
| lead_id | Integer (FK) | Related lead |
| user_id | Integer (FK) | Created by |

### Deals
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Primary key |
| name | String(255) | Deal name |
| amount | Float | Deal amount |
| stage | Enum | prospecting/qualification |
| probability | Integer | Success probability |
| customer_id | Integer (FK) | Related customer |
| assigned_to_id | Integer (FK) | Assigned user |

### Tasks
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Primary key |
| title | String(255) | Task title |
| priority | Enum | low/medium/high |
| status | Enum | pending/completed |
| due_date | DateTime | Due date |
| assigned_to_id | Integer (FK) | Assigned user |
| customer_id | Integer (FK) | Related customer |