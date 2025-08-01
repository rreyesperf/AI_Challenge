# Agentic RAG API Documentation

## Overview

The Agentic RAG API provides advanced conversational AI capabilities with intelligent agentic workflows, multi-LLM provider support, and Retrieval-Augmented Generation (RAG) functionality. This API is designed for building sophisticated AI applications that can handle complex travel planning, document analysis, and multi-provider consensus scenarios.

## 🤖 Agentic Features

### What Makes This API "Agentic"

1. **Multi-Step Reasoning**: The API can break down complex queries into multiple steps and execute them intelligently
2. **Provider Fallback**: Automatically tries multiple LLM providers in priority order for reliability
3. **Context Awareness**: Maintains conversation context and uses it for better decision-making
4. **Travel Planning Agent**: Specialized agent for comprehensive travel planning with real-time data
5. **Document Intelligence**: RAG system that can understand and reason about uploaded documents
6. **Consensus Building**: Aggregates responses from multiple LLMs to provide balanced insights

### Provider Priority System

The API automatically selects the best available LLM provider using this priority order:

1. **Ollama** (Local LLM) - Highest priority, cost-effective, private
2. **OpenAI** - High-quality responses, widely compatible  
3. **Anthropic Claude** - Strong reasoning capabilities
4. **Google Gemini** - Good for diverse tasks

This ensures reliability and cost optimization while maintaining high-quality responses.

## 🎯 Core Agentic Workflows

### 1. Intelligent Travel Planning Agent

The travel planning agent demonstrates advanced agentic behavior by:
- Analyzing user intent and extracting structured information
- Coordinating multiple travel services (flights, hotels, dining)
- Providing personalized recommendations based on preferences
- Handling complex multi-step travel scenarios

**Capabilities:**
- Budget analysis and optimization
- Multi-destination trip planning
- Real-time availability checking
- Preference learning and adaptation
- Alternative suggestion generation

### 2. Multi-Provider Consensus Engine

This workflow showcases collective intelligence by:
- Querying multiple LLM providers simultaneously
- Analyzing different perspectives on the same question
- Synthesizing responses into a balanced consensus
- Identifying areas of agreement and disagreement

**Use Cases:**
- Critical decision making
- Research and analysis
- Complex problem solving
- Quality assurance for AI responses

### 3. RAG-Powered Document Intelligence

The RAG system provides document-aware intelligence by:
- Processing and understanding various document types
- Creating semantic embeddings for intelligent retrieval
- Providing context-aware answers based on document content
- Maintaining source attribution and confidence scores

**Document Support:**
- PDF files (reports, manuals, guides)
- Word documents (policies, procedures)
- Text files (data, logs, notes)
- HTML content (web pages, articles)

## 🌐 Environment Configuration

For installation and setup instructions, see `README.md`. Here are the key agentic-specific configurations:

### LLM Provider Priority Configuration
```env
# The API will try providers in this order:
# 1. Ollama (if available)
# 2. OpenAI (if API key configured)
# 3. Anthropic (if API key configured)  
# 4. Google (if API key configured)

# Local LLM (Highest Priority)
OLLAMA_BASE_URL=http://localhost:11434

# Cloud Providers (Fallback)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# Advanced LLM Settings
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### RAG System Configuration
```env
# Vector Database Settings
CHROMA_PERSIST_DIRECTORY=./data/chroma
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7

# Alternative: Pinecone (Cloud Vector DB)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

## 📡 API Endpoints

### Core Chat & Conversation Endpoints

#### POST `/api/ai/chat`
Enhanced conversational chat with automatic provider selection and travel intelligence.

**Request:**
```json
{
  "message": "I need help planning a trip to Tokyo for 5 days under $2000",
  "conversation_history": [],  // optional
  "provider": "ollama",        // optional - if not specified, uses priority order
  "system_message": "You are a helpful travel assistant",  // optional
  "max_tokens": 1000,         // optional
  "temperature": 0.7          // optional
}
```

**Response:**
```json
{
  "success": true,
  "response": "I'd be happy to help you plan your Tokyo trip! Based on your $2000 budget for 5 days...",
  "provider": "ollama",
  "model": "llama3:8b",
  "conversation_type": "travel_planning",
  "status": "collecting_info"
}
```

#### POST `/api/ai/conversation`
Multi-turn conversation with context preservation.

**Request:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a travel planning expert"},
    {"role": "user", "content": "What's the best time to visit Japan?"},
    {"role": "assistant", "content": "The best times to visit Japan are..."},
    {"role": "user", "content": "What about cherry blossom season specifically?"}
  ],
  "provider": "openai"  // optional
}
```

### 🤖 Advanced Agentic Workflows

#### POST `/api/ai/travel-agent`
Intelligent travel planning agent with multi-step reasoning and real-time data integration.

**Agentic Behavior:**
1. **Intent Analysis**: Extracts travel preferences, budget, dates, and requirements
2. **Service Coordination**: Coordinates flights, hotels, dining, and activities
3. **Recommendation Engine**: Provides personalized suggestions based on analysis
4. **Alternative Planning**: Suggests alternatives if initial preferences aren't available

**Request:**
```json
{
  "query": "Plan a romantic weekend in Paris for our anniversary, budget around $1500",
  "flight_params": {
    "origin": "NYC",
    "destination": "CDG", 
    "departure_date": "2024-09-15",
    "return_date": "2024-09-17"
  },
  "hotel_params": {
    "location": "Paris",
    "checkin_date": "2024-09-15",
    "checkout_date": "2024-09-17",
    "guests": 2
  },
  "preferences": {
    "trip_type": "romantic",
    "accommodation_type": "boutique_hotel",
    "dining_style": "fine_dining",
    "activities": ["museums", "Seine_cruise", "Eiffel_Tower"]
  }
}
```

**Response:**
```json
{
  "user_query": "Plan a romantic weekend in Paris...",
  "intent_analysis": {
    "trip_type": "romantic leisure",
    "budget_range": "$1500",
    "duration": "2 days",
    "destination": "Paris, France",
    "special_occasion": "anniversary",
    "traveler_count": 2
  },
  "travel_analysis": {
    "recommendations": "For your romantic Paris anniversary...",
    "flight_options": [...],
    "hotel_recommendations": [...],
    "dining_suggestions": [...],
    "activity_plan": [...],
    "budget_breakdown": {...},
    "provider_used": "ollama"
  },
  "timestamp": "2025-07-31T10:30:00Z"
}
```

#### POST `/api/ai/consensus`
Multi-provider consensus engine for complex decision making.

**Agentic Behavior:**
1. **Parallel Querying**: Simultaneously queries multiple LLM providers
2. **Response Analysis**: Analyzes different perspectives and approaches
3. **Consensus Building**: Synthesizes responses into balanced recommendations
4. **Confidence Scoring**: Provides confidence levels for different aspects

**Request:**
```json
{
  "prompt": "What are the most important factors to consider when choosing a travel destination during economic uncertainty?",
  "providers": ["ollama", "openai", "anthropic"],  // optional - uses all available if not specified
  "consensus_type": "balanced"  // options: "balanced", "conservative", "optimistic"
}
```

**Response:**
```json
{
  "success": true,
  "question": "What are the most important factors...",
  "individual_responses": {
    "ollama": {
      "response": "During economic uncertainty, travelers should prioritize...",
      "model": "llama3:8b",
      "confidence": 0.85
    },
    "openai": {
      "response": "Key considerations include exchange rates...",
      "model": "gpt-3.5-turbo", 
      "confidence": 0.92
    },
    "anthropic": {
      "response": "Economic factors that affect travel decisions...",
      "model": "claude-3-sonnet",
      "confidence": 0.88
    }
  },
  "consensus": "Based on analysis from multiple AI perspectives, the most critical factors during economic uncertainty are: 1) Exchange rate stability and currency strength, 2) Political and economic stability of the destination...",
  "confidence_score": 0.88,
  "agreement_level": "high",
  "providers_used": ["ollama", "openai", "anthropic"],
  "processing_time": "3.2s"
}
```

### 🧠 RAG (Retrieval-Augmented Generation) Endpoints

#### POST `/api/ai/rag/ingest`
Intelligent document ingestion with semantic understanding.

**Agentic Behavior:**
1. **Format Detection**: Automatically detects and processes different file types
2. **Semantic Chunking**: Intelligently splits documents preserving context
3. **Metadata Extraction**: Extracts relevant metadata and document structure
4. **Vector Embedding**: Creates semantic embeddings for intelligent retrieval

**Request:**
```json
{
  "file_path": "/path/to/travel_guide.pdf",
  "metadata": {
    "category": "travel_guide",
    "region": "Europe",
    "language": "en"
  },
  "processing_options": {
    "chunk_size": 1000,
    "overlap": 200,
    "preserve_structure": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully ingested travel guide with semantic analysis",
  "document_hash": "abc123def456789",
  "chunk_count": 24,
  "metadata": {
    "file_name": "travel_guide.pdf",
    "file_type": "pdf",
    "file_size": 2048000,
    "processing_time": "15.3s",
    "language_detected": "en",
    "topic_categories": ["travel", "europe", "culture"],
    "processed_at": "2025-07-31T10:30:00Z"
  },
  "indexing_stats": {
    "total_tokens": 15420,
    "unique_concepts": 347,
    "embedding_model": "sentence-transformers",
    "vector_dimensions": 384
  }
}
```

#### POST `/api/ai/rag/query`
Intelligent document querying with context-aware responses.

**Agentic Behavior:**
1. **Query Understanding**: Analyzes intent and extracts key concepts
2. **Semantic Search**: Finds relevant content across all ingested documents
3. **Context Assembly**: Combines multiple relevant chunks intelligently
4. **Source Attribution**: Maintains clear source references and confidence

**Request:**
```json
{
  "question": "What are the best budget accommodations in Rome with good transportation links?",
  "top_k": 5,
  "filters": {
    "document_type": "travel_guide",
    "region": "Europe",
    "topic": ["accommodation", "transportation"]
  },
  "provider": "ollama",  // optional
  "include_sources": true
}
```

**Response:**
```json
{
  "success": true,
  "question": "What are the best budget accommodations in Rome...",
  "answer": "Based on the travel guides, here are the top budget accommodations in Rome with excellent transportation links: 1) Hotel Artemide near Termini Station offers...",
  "sources": [
    {
      "text": "Hotel Artemide, located just 200 meters from Roma Termini station...",
      "file_name": "rome_travel_guide.pdf",
      "similarity_score": 0.92,
      "chunk_index": 15,
      "page_number": 23,
      "confidence": 0.89
    },
    {
      "text": "For budget travelers, Hostel Alessandro Palace provides...",
      "file_name": "italy_budget_travel.pdf", 
      "similarity_score": 0.87,
      "chunk_index": 8,
      "page_number": 12,
      "confidence": 0.84
    }
  ],
  "llm_provider": "ollama",
  "llm_model": "llama3:8b",
  "chunks_used": 3,
  "total_documents_searched": 5,
  "search_time": "0.8s",
  "response_time": "2.1s"
}
```

#### DELETE `/api/ai/rag/delete`
Remove documents from the RAG system.

**Request:**
```json
{
  "document_hash": "abc123def456789"
}
```

### 🛠️ System & Utility Endpoints

#### GET `/api/ai/providers`
List available LLM providers with status and capabilities.

**Response:**
```json
{
  "available_providers": [
    {
      "name": "ollama",
      "status": "active",
      "model": "llama3:8b",
      "priority": 1,
      "capabilities": ["chat", "completion", "reasoning"],
      "cost": "free",
      "latency": "low"
    },
    {
      "name": "openai", 
      "status": "configured",
      "model": "gpt-3.5-turbo",
      "priority": 2,
      "capabilities": ["chat", "completion", "code", "analysis"],
      "cost": "paid",
      "latency": "medium"
    }
  ],
  "total_count": 2,
  "active_provider": "ollama",
  "fallback_chain": ["ollama", "openai"]
}
```

#### GET `/api/ai/health`
Comprehensive health check for AI services.

**Response:**
```json
{
  "status": "healthy",
  "available_providers": 2,
  "providers": {
    "ollama": {
      "status": "healthy",
      "response_time": "0.5s",
      "last_check": "2025-07-31T10:29:45Z"
    },
    "openai": {
      "status": "healthy", 
      "response_time": "1.2s",
      "last_check": "2025-07-31T10:29:45Z"
    }
  },
  "rag_enabled": true,
  "rag_status": {
    "vector_db": "chromadb",
    "documents_indexed": 15,
    "total_chunks": 342,
    "last_indexed": "2025-07-31T09:15:30Z"
  },
  "system_health": {
    "memory_usage": "512MB",
    "disk_space": "2.1GB available",
    "uptime": "2h 15m"
  },
  "timestamp": "2025-07-31T10:30:00Z"
}
```

### 🌍 Legacy Travel Endpoints

These endpoints are maintained for backward compatibility:

- `GET /api/flights` - Flight search functionality
- `GET /api/hotels` - Hotel search functionality  
- `GET /api/dining` - Restaurant search functionality
- `GET /api/transportation` - Transportation options
- `POST /api/aggregate` - Aggregate travel results

## Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   Create a `.env` file with your API keys and configuration.

3. **Initialize vector database:**
   The ChromaDB will be automatically initialized on first use.

4. **Run the application:**
   ```bash
   python app.py
   ```

## Usage Examples

### 1. Travel Planning with AI Agent
```python
import requests

response = requests.post('http://localhost:5000/api/ai/travel-agent', json={
    "query": "Plan a romantic weekend in Rome for $1500",
    "flight_params": {"origin": "LAX", "destination": "FCO", "date": "2024-06-15"},
    "hotel_params": {"location": "Rome", "checkin_date": "2024-06-15", "checkout_date": "2024-06-17"}
})

print(response.json())
```

### 2. Document Q&A with RAG
```python
# First, ingest a document
requests.post('http://localhost:5000/api/ai/rag/ingest', json={
    "file_path": "./travel_guide.pdf"
})

# Then query it
response = requests.post('http://localhost:5000/api/ai/rag/query', json={
    "question": "What are the best restaurants in Rome?",
    "provider": "anthropic"
})

print(response.json()['answer'])
```

### 3. Multi-Provider Consensus
```python
response = requests.post('http://localhost:5000/api/ai/consensus', json={
    "prompt": "What factors should I consider when choosing a hotel?",
    "providers": ["openai", "anthropic"]
})

print(response.json()['consensus'])
```

## Architecture

The agentic API is built with a modular architecture:

- **LLM Service**: Manages multiple LLM providers with unified interface
- **RAG Service**: Handles document processing, vector storage, and retrieval
- **Agentic Workflows**: Implements intelligent multi-step processes
- **Route Handlers**: Flask endpoints for all functionality

## Supported File Types

- **PDF**: `.pdf` files using PyPDF2
- **Word Documents**: `.docx` files using python-docx  
- **Text Files**: `.txt` files with UTF-8 encoding
- **HTML**: `.html` files with BeautifulSoup parsing

## Error Handling

All endpoints include comprehensive error handling and return structured error responses:

```json
{
  "success": false,
  "error": "Detailed error message",
  "timestamp": "2024-01-15T10:30:00"
}
```

## Scaling Considerations

- Use environment variables for configuration
- Consider using Redis for caching
- Implement rate limiting for production use
- Use async processing for large document ingestion
- Consider distributed vector databases for large-scale deployments
