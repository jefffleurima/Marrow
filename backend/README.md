# Marrow API

**AI Memory Infrastructure** — Store, recall, forget. The memory layer for AI.

## Quick Start

### 1. Prerequisites

- Python 3.11+
- [Supabase](https://supabase.com) account
- [OpenAI](https://platform.openai.com) API key

### 2. Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run the migration:
   - Copy contents of `supabase/migrations/001_initial_schema.sql`
   - Execute in the SQL Editor

3. Get your **Database URL**:
   - Project Settings → Database → Connection string (URI)
   - Use the **direct connection** string (not the pooler for async)

### 3. Install & Configure

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
OPENAI_API_KEY=sk-...
```

### 4. Get an API Key

**Option A:** Run the seed script (one-time):

```bash
python -m scripts.seed_app
```

**Option B:** If the API is already running, create an app via API:

```bash
curl -X POST http://localhost:8000/v1/apps -H "Content-Type: application/json" -d '{"name": "my-app"}'
```

Copy the API key. You'll use it for all memory requests.

### 5. Run the API

```bash
uvicorn main:app --reload
```

API runs at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

## API Usage

**Create app (no auth):** `POST /v1/apps` — returns an API key.

**Memory endpoints** require an API key via header:

- `X-API-Key: your_api_key`
- or `Authorization: Bearer your_api_key`

### Store a memory

```bash
curl -X POST http://localhost:8000/v1/memories \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "content": "Prefers window seats on flights", "metadata": {"source": "travel_app"}}'
```

### Recall memories

```bash
curl -X POST http://localhost:8000/v1/memories/recall \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "query": "travel preferences", "limit": 5}'
```

### Update a memory

```bash
curl -X PATCH http://localhost:8000/v1/memories/{memory_id} \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "content": "Prefers aisle seats on flights"}'
```

### Forget a memory

```bash
curl -X DELETE "http://localhost:8000/v1/memories/{memory_id}?user_id=user_123" \
  -H "X-API-Key: YOUR_KEY"
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app
├── marrow/
│   ├── api/routes/         # apps (create key), memory (store/recall/update/forget)
│   ├── auth.py             # API key verification
│   ├── config.py           # Settings
│   ├── db.py               # Connection pool
│   ├── models.py           # Pydantic schemas
│   └── services/           # embeddings, memory
├── scripts/
│   └── seed_app.py         # Create dev app (optional)
└── supabase/
    └── migrations/         # SQL schema
```

## License

Proprietary — Marrow
