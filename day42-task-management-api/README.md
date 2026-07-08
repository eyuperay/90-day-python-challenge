# Day42 Task Management API

FastAPI tabanlı, JWT auth destekli task management backend.

## Özellikler
- JWT login/register
- Project / Task / Comment / Inventory CRUD
- Async SQLAlchemy
- CORS hazır
- Redis cache altyapısı

## Çalıştırma
1. `.env.example` dosyasını `.env` olarak kopyala
2. Kurulum yap:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlat:
   ```bash
   uvicorn app.main:app --reload
   ```

## Swagger
`/docs`