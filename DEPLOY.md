# Deploy Marrow to Railway

Get a public URL in ~5 minutes.

## Prerequisites

- [Railway](https://railway.app) account (free tier works)
- GitHub repo with your Marrow code
- Supabase project (already set up)
- OpenAI API key

## Steps

### 1. Push to GitHub

If you haven't already:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/marrow.git
git push -u origin main
```

### 2. Create a Railway project

1. Go to [railway.app](https://railway.app) and sign in (use GitHub)
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your Marrow repo
5. **Important:** Set **Root Directory** to `backend`
   - Click the service → **Settings** → **Root Directory** → enter `backend`

### 3. Add environment variables

In Railway: **Settings** → **Variables** → **Add Variable**

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Supabase connection string (direct, port 5432) |
| `OPENAI_API_KEY` | Your OpenAI API key |

Use the same values from your local `.env`.

### 4. Deploy

Railway deploys automatically when you push. If it doesn't start:

- Go to **Settings** → **Deploy** → trigger a redeploy
- Or push a small commit to trigger a new build

### 5. Generate a public URL

1. Go to **Settings** → **Networking**
2. Click **Generate Domain**
3. Railway assigns a URL like `marrow-api-production-xxxx.up.railway.app`

### 6. Test it

**Option A:** Use your existing API key from `seed_app` (same Supabase, same data).

**Option B:** Create a new key via the API (no seed script needed):

```bash
curl -X POST https://YOUR-RAILWAY-URL/v1/apps \
  -H "Content-Type: application/json" \
  -d '{"name": "my-app"}'
```

Returns `{"api_key": "marrow_...", ...}`. Use that for all memory operations.

```bash
# Replace YOUR-URL with your Railway domain (e.g. marrow-api-production-xxxx.up.railway.app)
curl https://YOUR-URL/health
# → {"status":"ok"}

curl -X POST https://YOUR-URL/v1/memories/recall \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "query": "travel", "limit": 5}'
```

Docs: `https://YOUR-URL/docs`

### 7. Use the Python SDK

```bash
pip install "git+https://github.com/YOUR_USERNAME/marrow.git#subdirectory=sdk/python"
```

```python
from marrow import Marrow
client = Marrow(api_key="your_key", base_url="https://YOUR-URL")
client.store("user_123", "Hello from hosted Marrow!")
print(client.recall("user_123", "greetings"))
```

---

## Troubleshooting

**Build fails:** Ensure `backend` is set as Root Directory. Railway needs to find `requirements.txt` and `main.py` there.

**App crashes on startup:** Check that `DATABASE_URL` and `OPENAI_API_KEY` are set. Railway logs: **Deployments** → click deployment → **View Logs**.

**502 Bad Gateway:** The app may still be starting. Wait 30–60 seconds and retry.
