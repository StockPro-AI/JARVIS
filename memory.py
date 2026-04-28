"""
JARVIS Memory & Knowledge Graph System

Features:
- Response Cache: SHA256-hashed query -> cached response (saves API tokens)
- Knowledge Graph: NetworkX-based entity relationships
- Conversation History: Last N turns with context compression
- Entity Extraction: Simple pattern-based entity detection
- Persistent Storage: JSON-based (cache_store.json + knowledge_graph.json)

Usage:
    from memory import MemorySystem
    
    memory = MemorySystem()
    
    # Check cache before API call
    cached = memory.get_cached_response("what is the weather")
    if cached:
        return cached
    
    # Store new response
    response = call_gemini_api(query)
    memory.cache_response(query, response)
    
    # Add to knowledge graph
    memory.add_entity("Weather", "concept", {"asked_at": timestamp})
    memory.add_relationship("User", "ASKS_ABOUT", "Weather")
"""

import json
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import deque
import re


class MemorySystem:
    """
    Unified memory system combining:
    - Response caching (token saver)
    - Knowledge graph (entity tracking)
    - Conversation history (context)
    """
    
    def __init__(self, 
                 cache_file="cache_store.json",
                 graph_file="knowledge_graph.json",
                 history_size=20):
        self.cache_file = cache_file
        self.graph_file = graph_file
        self.history_size = history_size
        
        # In-memory structures
        self.response_cache: Dict[str, Dict] = {}
        self.knowledge_graph: Dict[str, Any] = {"entities": {}, "relationships": []}
        self.conversation_history: deque = deque(maxlen=history_size)
        
        # Load from disk
        self._load_cache()
        self._load_graph()
    
    # ============================================================
    # CACHE SYSTEM (Token Saver)
    # ============================================================
    
    def _hash_query(self, query: str) -> str:
        """Generate SHA256 hash for query normalization"""
        normalized = query.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def get_cached_response(self, query: str) -> Optional[str]:
        """
        Check if response exists in cache.
        Returns cached response text or None.
        """
        query_hash = self._hash_query(query)
        if query_hash in self.response_cache:
            cached = self.response_cache[query_hash]
            cached["hit_count"] = cached.get("hit_count", 0) + 1
            cached["last_accessed"] = datetime.now().isoformat()
            print(f"[CACHE HIT] Query: {query[:50]}...")
            return cached["response"]
        return None
    
    def cache_response(self, query: str, response: str):
        """Store response in cache with metadata"""
        query_hash = self._hash_query(query)
        self.response_cache[query_hash] = {
            "query": query,
            "response": response,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "hit_count": 0
        }
        self._save_cache()
    
    def clear_cache(self):
        """Clear all cached responses"""
        self.response_cache = {}
        self._save_cache()
    
    # ============================================================
    # KNOWLEDGE GRAPH (Entity Tracking)
    # ============================================================
    
    def add_entity(self, name: str, entity_type: str, metadata: Dict = None):
        """Add or update an entity in the knowledge graph"""
        if name not in self.knowledge_graph["entities"]:
            self.knowledge_graph["entities"][name] = {
                "type": entity_type,
                "created_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
        else:
            # Update metadata if entity exists
            self.knowledge_graph["entities"][name]["metadata"].update(metadata or {})
        self._save_graph()
    
    def add_relationship(self, source: str, relation: str, target: str):
        """Add a relationship between two entities"""
        rel = {"source": source, "relation": relation, "target": target}
        if rel not in self.knowledge_graph["relationships"]:
            self.knowledge_graph["relationships"].append(rel)
            self._save_graph()
    
    def get_entity(self, name: str) -> Optional[Dict]:
        """Retrieve entity data"""
        return self.knowledge_graph["entities"].get(name)
    
    def find_related(self, entity: str) -> List[Dict]:
        """Find all entities related to given entity"""
        related = []
        for rel in self.knowledge_graph["relationships"]:
            if rel["source"] == entity:
                related.append({"entity": rel["target"], "relation": rel["relation"]})
            elif rel["target"] == entity:
                related.append({"entity": rel["source"], "relation": rel["relation"]})
        return related
    
    def extract_entities(self, text: str) -> List[str]:
        """Simple entity extraction (can be enhanced with NER)"""
        # Pattern-based extraction for common entities
        entities = []
        
        # URLs
        urls = re.findall(r'https?://[^\s]+', text)
        entities.extend(urls)
        
        # Capitalized words (potential proper nouns)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(proper_nouns)
        
        return list(set(entities))  # Unique entities
    
    # ============================================================
    # CONVERSATION HISTORY (Context Management)
    # ============================================================
    
    def add_to_history(self, role: str, content: str):
        """Add a turn to conversation history"""
        self.conversation_history.append({
            "role": role,  # "user" or "assistant"
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_recent_context(self, n_turns: int = 5) -> str:
        """
        Get last N conversation turns as formatted context string.
        Useful for providing context to LLM without full history.
        """
        recent = list(self.conversation_history)[-n_turns:]
        context_str = ""
        for turn in recent:
            context_str += f"{turn['role'].capitalize()}: {turn['content']}\n"
        return context_str.strip()
    
    def compress_context(self, max_length: int = 500) -> str:
        """
        Compress conversation history to fit within token budget.
        Uses simple truncation (can be enhanced with summarization).
        """
        context = self.get_recent_context()
        if len(context) > max_length:
            context = context[:max_length] + "..."
        return context
    
    # ============================================================
    # PERSISTENCE (Load/Save)
    # ============================================================
    
    def _load_cache(self):
        """Load cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.response_cache = json.load(f)
                print(f"[MEMORY] Loaded {len(self.response_cache)} cached responses")
            except Exception as e:
                print(f"[ERROR] Failed to load cache: {e}")
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.response_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to save cache: {e}")
    
    def _load_graph(self):
        """Load knowledge graph from disk"""
        if os.path.exists(self.graph_file):
            try:
                with open(self.graph_file, 'r', encoding='utf-8') as f:
                    self.knowledge_graph = json.load(f)
                print(f"[MEMORY] Loaded {len(self.knowledge_graph['entities'])} entities")
            except Exception as e:
                print(f"[ERROR] Failed to load graph: {e}")
    
    def _save_graph(self):
        """Save knowledge graph to disk"""
        try:
            with open(self.graph_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_graph, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to save graph: {e}")
    
    # ============================================================
    # UTILITY METHODS
    # ============================================================
    
    def get_stats(self) -> Dict:
        """Get memory system statistics"""
        return {
            "cache_entries": len(self.response_cache),
            "entities": len(self.knowledge_graph["entities"]),
            "relationships": len(self.knowledge_graph["relationships"]),
            "history_size": len(self.conversation_history),
            "cache_hits": sum(c.get("hit_count", 0) for c in self.response_cache.values())
        }
    
    def export_for_codex(self) -> str:
        """
        Export compressed knowledge for Codex/LLM prompt.
        Returns a compact string representation of memory.
        """
        stats = self.get_stats()
        context = self.compress_context(max_length=300)
        top_entities = list(self.knowledge_graph["entities"].keys())[:10]
        
        export = f"""
## Memory Context (Token-Optimized)
- Conversation: {stats['history_size']} turns
- Entities: {', '.join(top_entities[:5])}...
- Recent:
{context}
"""
        return export.strip()
