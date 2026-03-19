# Marrow Python SDK

The memory layer for AI. Add persistent memory to your app in 5 minutes.

## Install

```bash
pip install marrow
```

Or from source:

```bash
pip install .
```

Or from the repo (when not yet on PyPI):

```bash
pip install "marrow @ git+https://github.com/YOUR_USERNAME/marrow.git#subdirectory=sdk/python"
```

## Usage

```python
from marrow import Marrow

client = Marrow(api_key="your_api_key", base_url="https://your-api.up.railway.app")

# Store a memory
memory = client.store("user_123", "Prefers window seats on flights")
print(memory["id"])  # UUID of the stored memory

# Recall relevant memories (semantic search)
memories = client.recall("user_123", "travel preferences")
for m in memories:
    print(m["content"])

# Update a memory
client.update("user_123", memory["id"], "Prefers aisle seats")

# Forget a memory
client.forget("user_123", memory["id"])
```

## API

| Method | Description |
|--------|-------------|
| `store(user_id, content, metadata?)` | Store a memory. Returns the created memory. |
| `recall(user_id, query, limit?)` | Semantic search. Returns list of memories. |
| `update(user_id, memory_id, content)` | Update a memory. Returns the updated memory. |
| `forget(user_id, memory_id)` | Delete a memory. |

## Requirements

- Python 3.10+
- An API key (from `POST /v1/apps` on your Marrow API)
