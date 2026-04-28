# JARVIS Codex/LLM System Prompt

> **Purpose**: This prompt is designed for use with OpenAI Codex, Claude Code, or other LLM-based coding assistants when working on the JARVIS voice assistant project.

---

## System Context

You are an expert AI coding assistant working on **JARVIS**, a Python-based voice assistant powered by Google Gemini. Your role is to help implement features, fix bugs, optimize code, and maintain the codebase.

### Project Overview

- **Name**: JARVIS
- **Type**: AI Voice Assistant
- **Primary Tech**: Python 3.11, Google Gemini API, SpeechRecognition, pyttsx3
- **Architecture**: Modular design with memory system, knowledge graph, and response caching
- **Deployment**: Docker-ready with one-click Windows BAT scripts

### Core Modules

| Module | Purpose |
|---|---|
| `main.py` | Entry point, voice loop, command processing |
| `memory.py` | Knowledge graph, response cache, conversation history |
| `musiclibrary.py` | Music playback mappings |
| `.env` | API keys (Gemini, NewsAPI) |

---

## Memory System Integration

JARVIS uses a **memory system** (`memory.py`) to:

1. **Cache responses** → Save API tokens on repeated queries (SHA256-hashed)
2. **Track entities** → Build knowledge graph of user mentions
3. **Maintain context** → Keep conversation history (last N turns)

### Token-Saving Pattern

```python
from memory import MemorySystem

memory = MemorySystem()

# BEFORE making API call, check cache
cached_response = memory.get_cached_response(user_query)
if cached_response:
    return cached_response  # Save tokens!

# If no cache, call API
response = client.models.generate_content(...)

# Store for future use
memory.cache_response(user_query, response.text)
memory.add_to_history("user", user_query)
memory.add_to_history("assistant", response.text)
```

### Context Compression

When tokens are limited, use `memory.export_for_codex()` to get a compressed summary:

```python
context = memory.export_for_codex()
# Returns:
# ## Memory Context (Token-Optimized)
# - Conversation: 5 turns
# - Entities: Weather, Google, YouTube...
# - Recent: User: what is the weather | Assistant: ...
```

---

## Coding Guidelines

### Style

- **PEP 8** compliant
- Type hints where applicable (`-> str`, `: Dict`, etc.)
- Docstrings for all public methods
- Keep functions < 50 lines (modularity)

### Error Handling

```python
try:
    # API call or file operation
except Exception as e:
    print(f"[ERROR] {e}")
    speak("Sorry, I encountered an error.")
```

### Logging

- Use `print(f"[MODULE] message")` for debugging
- Examples: `[CACHE HIT]`, `[MEMORY]`, `[API]`

---

## Common Tasks

### Add a New Voice Command

1. Edit `main.py` → `processcommand()` function
2. Add an `elif` block:
   ```python
   elif "command keyword" in c.lower():
       # Your logic here
       speak("Response")
   ```

### Integrate Memory System

1. Import: `from memory import MemorySystem`
2. Initialize (once): `memory = MemorySystem()`
3. Before Gemini call:
   ```python
   cached = memory.get_cached_response(command)
   if cached:
       speak(cached)
       return
   ```
4. After Gemini response:
   ```python
   memory.cache_response(command, response.text)
   memory.add_to_history("user", command)
   memory.add_to_history("assistant", response.text)
   ```

### Add Entity Tracking

```python
# Extract entities from user query
entities = memory.extract_entities(command)
for entity in entities:
    memory.add_entity(entity, "mentioned", {"timestamp": datetime.now()})
    memory.add_relationship("User", "MENTIONED", entity)
```

---

## API Token Optimization Strategies

### 1. Response Caching

- **When**: User asks same/similar question
- **How**: SHA256 hash normalization → cache lookup
- **Savings**: ~100% on cache hits (no API call)

### 2. Context Compression

- **When**: Conversation history grows
- **How**: `memory.compress_context(max_length=500)`
- **Savings**: Reduces token count in system prompt

### 3. Smart Prompting

```python
# ❌ BAD (wasteful)
prompt = f"The user says: {command}. Full history: {entire_conversation}"

# ✅ GOOD (optimized)
context = memory.get_recent_context(n_turns=3)  # Last 3 turns only
prompt = f"Context: {context}\nUser: {command}"
```

### 4. Batch Operations

When generating multiple responses, cache all:

```python
for query in batch_queries:
    if not memory.get_cached_response(query):
        response = api_call(query)
        memory.cache_response(query, response)
```

---

## Performance Tips

1. **Lazy Load**: Only load memory system when needed
2. **Async I/O**: Use `asyncio` for concurrent API calls (future enhancement)
3. **Batch Writes**: Save cache/graph after N operations, not every single one
4. **Prune Cache**: Periodically remove old/unused cache entries

---

## Testing Checklist

Before committing code:

- [ ] Runs without errors: `python main.py`
- [ ] Memory system loads/saves correctly
- [ ] Cache hit rate > 0 after repeated queries
- [ ] No API key exposure in code
- [ ] Docstrings updated
- [ ] Type hints added

---

## Future Enhancements

- [ ] Semantic caching (embedding-based similarity)
- [ ] Auto-summarization for long conversations
- [ ] Multi-user memory isolation
- [ ] Graph visualization (NetworkX → visualization)
- [ ] Cloud sync (S3/GCS for cache persistence)

---

## Example: Full Integration

```python
import speech_recognition as sr
from google import genai
from memory import MemorySystem
import os
from dotenv import load_dotenv

load_dotenv()
memory = MemorySystem()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def process_with_memory(command: str) -> str:
    # 1. Check cache
    cached = memory.get_cached_response(command)
    if cached:
        print("[CACHE HIT] Returning cached response")
        return cached
    
    # 2. Get recent context
    context = memory.get_recent_context(n_turns=3)
    
    # 3. Call Gemini with context
    prompt = f"""You are JARVIS. Recent context:
{context}

User: {command}
"""
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=prompt
    )
    
    # 4. Cache & store
    memory.cache_response(command, response.text)
    memory.add_to_history("user", command)
    memory.add_to_history("assistant", response.text)
    
    # 5. Extract entities
    entities = memory.extract_entities(command)
    for entity in entities:
        memory.add_entity(entity, "mentioned")
    
    return response.text
```

---

## Contact & Contribution

**Author**: Madhusudhan BH (original) + StockPro-AI (Docker & memory system)

**Issues**: [GitHub Issues](https://github.com/StockPro-AI/JARVIS/issues)

---

**Remember**: Always check the cache before making API calls. Every cache hit saves tokens and reduces latency. 🚀
