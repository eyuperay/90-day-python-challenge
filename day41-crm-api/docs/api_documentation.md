# CRM API Documentation

## Base URL
`http://localhost:8000/api/v1`

## Authentication

### Register User
- **POST** `/auth/register`
- **Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "password123"
}