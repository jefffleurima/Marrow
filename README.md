# Marrow

**The memory layer for AI.** Add persistent memory to your app in 5 minutes. Store, recall, forget—semantic search built in.

```python
from marrow import Marrow

client = Marrow(api_key="your_api_key")

# Store a memory
client.store("user_123", "Prefers window seats on flights")

# Recall relevant memories (semantic search)
memories = client.recall("user_123", "travel preferences")
# → [{"content": "Prefers window seats on flights", ...}]
```

Works with any LLM. No vector DB to manage. No embeddings pipeline. Just memory.

---

## Quick Start

### 1. Install

```bash
pip install marrow
```

*Not on PyPI yet?* Install from repo: `pip install "git+https://github.com/YOUR_USERNAME/marrow.git#subdirectory=sdk/python"`

### 2. Get an API key

**Hosted** — No setup. Create an app and get your key:

```bash
curl -X POST https://YOUR-API-URL/v1/apps \
  -H "Content-Type: application/json" \
  -d '{"name": "my-app"}'
```

Returns `{"api_key": "marrow_...", ...}`. Store it securely.

*Deploy your own API in ~5 min: [DEPLOY.md](DEPLOY.md). Then replace `YOUR-API-URL` with your Railway URL.*

**Self-host (15–20 min)** — Run your own instance. Full setup: [backend/README.md](backend/README.md).

### 3. Your first recall

```python
from marrow import Marrow

client = Marrow(api_key="your_api_key", base_url="https://YOUR-API-URL")  # omit base_url if using default

# Store something
client.store("user_123", "I'm building a memory startup")

# Recall it
results = client.recall("user_123", "what am I working on?")
print(results[0]["content"])  # → "I'm building a memory startup"
```

That's it. You have semantic memory.

---

## API

| Method | What it does |
|--------|--------------|
| `store(user_id, content, metadata?)` | Store a fact, preference, or event. Returns the memory ID. |
| `recall(user_id, query, limit?)` | Retrieve relevant memories via semantic search. |
| `update(user_id, memory_id, content)` | Update an existing memory. |
| `forget(user_id, memory_id)` | Delete a memory. |

All operations are scoped to your app (via API key). `user_id` is yours—use it to scope memories per end-user.

---

## How it works

1. **Store**: We embed your content with OpenAI, store it in a vector DB. You get back an ID.
2. **Recall**: We embed your query, run semantic search, return the most relevant memories.
3. **Update / Forget**: Standard CRUD. Update re-embeds the new content.

You don't touch embeddings, vectors, or databases. We handle it.

---

## Requirements

- Python 3.11+
- An API key (from hosted API or self-hosted instance)
- For self-hosting: Supabase (Postgres + pgvector), OpenAI API key

---

## Links

- **API docs**: `http://localhost:8000/docs` (when running locally)
- **Python SDK**: [sdk/python/](sdk/python/)
- **Self-host setup**: [backend/README.md](backend/README.md)
- **Deploy to Railway**: [DEPLOY.md](DEPLOY.md) — get a public URL in ~5 min

---

*Marrow: The memory layer for AI. We don't build the models. We give them memory.*
