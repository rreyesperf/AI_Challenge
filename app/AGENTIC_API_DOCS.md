# Agentic RAG API Documentation

## Overview

This Flask application provides an advanced Agentic API that connects to multiple LLM models for Retrieval-Augmented Generation (RAG) analysis. The API supports multiple LLM providers, document ingestion, intelligent travel planning, and multi-provider consensus mechanisms.

## Features

- **Multi-LLM Support**: OpenAI, Anthropic, Google Gemini, Azure OpenAI
- **RAG Capabilities**: Document ingestion, vector search, and context-aware responses
- **Agentic Workflows**: Intelligent travel planning, document Q&A, consensus analysis
- **Vector Databases**: ChromaDB, Pinecone, FAISS support
- **Document Processing**: PDF, DOCX, TXT, HTML file support

## Environment Variables

### Required LLM API Keys (at least one must be configured):
```env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# Azure OpenAI (uses standard openai package)
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Vector Database Configuration:
```env
# ChromaDB (default)
CHROMA_PERSIST_DIRECTORY=./data/chroma

# Pinecone (optional)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

### LLM Configuration:
```env
DEFAULT_LLM_PROVIDER=local_llm
DEFAULT_MODEL=local-model
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### RAG Configuration:
```env
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7
```

## API Endpoints

### 1. Basic Chat Endpoints

#### POST `/api/ai/chat`
Basic chat with provider selection.

**Request:**
```json
{
  "message": "Hello, how can you help me?",
  "provider": "openai",  // optional
  "system_message": "You are a helpful assistant",  // optional
  "max_tokens": 1000,  // optional
  "temperature": 0.7  // optional
}
```

**Response:**
```json
{
  "success": true,
  "response": "Hello! I'm here to help...",
  "provider": "openai",
  "model": "gpt-3.5-turbo"
}
```

#### POST `/api/ai/conversation`
Multi-turn conversation support.

**Request:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is the weather like?"},
    {"role": "assistant", "content": "I don't have access to real-time weather data..."},
    {"role": "user", "content": "Can you help me with travel planning?"}
  ],
  "provider": "anthropic"  // optional
}
```

### 2. Agentic Workflows

#### POST `/api/ai/travel-agent`
Intelligent travel planning agent that analyzes travel queries and provides recommendations.

**Request:**
```json
{
  "query": "I need a family vacation to Paris for 5 days under $3000",
  "flight_params": {
    "origin": "NYC",
    "destination": "CDG",
    "date": "2024-08-15"
  },
  "hotel_params": {
    "location": "Paris",
    "checkin_date": "2024-08-15",
    "checkout_date": "2024-08-20"
  }
}
```

**Response:**
```json
{
  "user_query": "I need a family vacation to Paris...",
  "intent_analysis": "Travel type: family leisure, Budget: $3000, Destination: Paris...",
  "travel_analysis": {
    "recommendations": "Based on your requirements...",
    "provider_used": "openai_gpt4"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

#### POST `/api/ai/consensus`
Get consensus from multiple LLM providers.

**Request:**
```json
{
  "prompt": "What are the best practices for sustainable travel?",
  "providers": ["openai", "anthropic", "google"]
}
```

**Response:**
```json
{
  "success": true,
  "question": "What are the best practices for sustainable travel?",
  "individual_responses": {
    "openai": {"response": "Sustainable travel involves..."},
    "anthropic": {"response": "To travel sustainably..."},
    "google": {"response": "Eco-friendly travel means..."}
  },
  "consensus": "Based on multiple AI perspectives, sustainable travel best practices include...",
  "providers_used": ["openai", "anthropic", "google"]
}
```

### 3. RAG (Retrieval-Augmented Generation) Endpoints

#### POST `/api/ai/rag/ingest`
Ingest documents into the RAG system.

**Request:**
```json
{
  "file_path": "/path/to/document.pdf"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully ingested 15 chunks",
  "document_hash": "abc123def456",
  "chunk_count": 15,
  "metadata": {
    "file_name": "document.pdf",
    "file_type": ".pdf",
    "file_size": 1024000,
    "processed_at": "2024-01-15T10:30:00"
  }
}
```

#### POST `/api/ai/rag/query`
Query documents using RAG.

**Request:**
```json
{
  "question": "What are the main points about customer service?",
  "top_k": 5,  // optional
  "provider": "openai"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "question": "What are the main points about customer service?",
  "answer": "Based on the documents, the main points about customer service are...",
  "sources": [
    {
      "text": "Customer service is crucial for business success...",
      "file_name": "business_guide.pdf",
      "similarity_score": 0.89,
      "chunk_index": 3
    }
  ],
  "llm_provider": "openai",
  "llm_model": "gpt-3.5-turbo",
  "chunks_used": 3
}
```

#### DELETE `/api/ai/rag/delete`
Delete a document from the RAG system.

**Request:**
```json
{
  "document_hash": "abc123def456"
}
```

### 4. Utility Endpoints

#### GET `/api/ai/providers`
List available LLM providers.

**Response:**
```json
{
  "available_providers": ["openai", "openai_gpt4", "anthropic", "google"],
  "total_count": 4
}
```

#### GET `/api/ai/health`
Health check for AI services.

**Response:**
```json
{
  "status": "healthy",
  "available_providers": 4,
  "providers": ["openai", "anthropic", "google", "azure_openai"],
  "rag_enabled": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 5. Existing Travel Endpoints

The API maintains backward compatibility with existing travel endpoints:

- `GET /api/flights` - Flight search
- `GET /api/hotels` - Hotel search  
- `GET /api/dining` - Restaurant search
- `GET /api/transportation` - Transportation options
- `POST /aggregate` - Aggregate travel results

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
