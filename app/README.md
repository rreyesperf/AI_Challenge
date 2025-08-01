# Agentic RAG API

A powerful Flask-based API that provides advanced conversational AI capabilities with multiple LLM providers, travel planning features, and Retrieval-Augmented Generation (RAG) functionality.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (recommended)
- Virtual environment (recommended)
- At least one LLM provider API key OR local Ollama installation

### 1. Clone and Setup Environment
```bash
# Clone the repository (if applicable)
# cd to the project directory

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# Or install manually:
pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2 gunicorn==21.2.0
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your configuration
```

### 4. Run the Application
```bash
# Development mode
python app.py

# Or using Flask CLI
flask run

# Production mode (with Gunicorn)
gunicorn --bind 0.0.0.0:5000 startup:app
```

The API will be available at `http://localhost:5000`

## 📋 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following configuration:

#### LLM Provider Configuration (Choose at least one)

```env
# OpenAI (Recommended)
OPENAI_API_KEY=your_openai_api_key

# Anthropic Claude (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Google Gemini (Optional)
GOOGLE_API_KEY=your_google_api_key

# Azure OpenAI (Optional)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Local LLM (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
```

#### General Configuration
```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# LLM Settings
DEFAULT_LLM_PROVIDER=ollama
DEFAULT_MODEL=llama3
MAX_TOKENS=2000
TEMPERATURE=0.7

# RAG Configuration (Optional)
CHROMA_PERSIST_DIRECTORY=./data/chroma
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7

# Vector Database (Optional)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# Azure Monitoring (Optional)
APP_INSIGHTS_INSTRUMENTATION_KEY=your_insights_key
```

## 🔧 Installation Options

### Option 1: Basic Installation (Core Features Only)
```bash
pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2 gunicorn==21.2.0
```

### Option 2: With OpenAI Support
```bash
pip install -r requirements.txt
# Uncomment OpenAI line in requirements.txt or:
pip install openai==1.98.0
```

### Option 3: Full Installation (All Features)
```bash
# Install all dependencies
pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2 gunicorn==21.2.0

# LLM Providers
pip install openai==1.98.0
pip install anthropic==0.25.9
pip install google-generativeai==0.5.4

# Document Processing
pip install PyPDF2==3.0.1 python-docx==1.1.0

# RAG Capabilities
pip install sentence-transformers==2.7.0 chromadb==0.4.24 tiktoken==0.7.0 numpy==1.26.4

# Azure Monitoring
pip install opencensus-ext-azure==1.1.13 opencensus-ext-flask==0.8.0
```

## 🤖 Local LLM Setup (Ollama)

### Install Ollama
```bash
# Windows: Download installer from https://ollama.ai/download
# macOS:
brew install ollama
# Linux:
curl -fsSL https://ollama.ai/install.sh | sh
```

### Setup Models
```bash
# Start Ollama service
ollama serve

# Download models
ollama pull llama3        # Latest Llama model
ollama pull mistral       # Mistral 7B
ollama pull codellama     # Code-focused model

# List available models
ollama list

# Test model
ollama run llama3 "Hello, how are you?"
```

### Configuration
Ollama runs on `http://localhost:11434` by default. The API will automatically detect and use available Ollama models with the highest priority.

## 🏗️ Project Structure

```
app/
├── app.py                      # Main application entry point
├── startup.py                  # Production startup script
├── routes.py                   # API routes and endpoints
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.template              # Environment template
├── services/                  # Core services
│   ├── llm_service.py         # LLM provider management
│   ├── lmintegration.py       # Agentic workflows
│   ├── rag_service.py         # RAG functionality
│   ├── aggregation.py         # Travel data aggregation
│   ├── flights.py             # Flight search
│   ├── hotels.py              # Hotel search
│   ├── dining.py              # Restaurant search
│   ├── transportation.py      # Transportation options
│   └── geolocation.py         # Location services
├── auth/                      # Authentication
│   └── jwt_auth.py           # JWT authentication
├── tests/                     # Test suite
├── data/                      # Data storage
│   └── chroma/               # Vector database
├── UI/                        # React frontend
└── docs/                      # Documentation
```

## 🚦 Testing the Installation

### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-31T12:00:00",
  "services": {
    "enhanced_chat": true,
    "llm_service": true
  }
}
```

### 2. Test AI Services
```bash
curl http://localhost:5000/api/ai/health
```

### 3. Test Chat Endpoint
```bash
curl -X POST http://localhost:5000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### 4. Check Available Providers
```bash
curl http://localhost:5000/api/ai/providers
```

## 🔍 Troubleshooting

### Common Issues

#### 1. No LLM Providers Available
**Problem**: API returns "No LLM providers available"
**Solution**: 
- Ensure at least one API key is configured in `.env`
- For Ollama: Check if service is running with `ollama list`
- Verify API keys are valid

#### 2. Import Errors
**Problem**: Missing module errors
**Solution**: 
- Install missing dependencies: `pip install -r requirements.txt`
- Activate virtual environment
- Check Python version (3.11+ recommended)

#### 3. Port Already in Use
**Problem**: Port 5000 already occupied
**Solution**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process or use different port
python app.py --port 5001
```

#### 4. Ollama Connection Issues
**Problem**: Cannot connect to Ollama
**Solution**:
```bash
# Check if Ollama is running
ollama list
# Start Ollama service
ollama serve
# Check URL in .env file
OLLAMA_BASE_URL=http://localhost:11434
```

### Debug Mode
Run with debug information:
```bash
export FLASK_ENV=development
export LOG_LEVEL=DEBUG
python app.py
```

## 🎯 Priority System

The API uses a strict priority system for LLM providers:

1. **Ollama** (Local LLM) - Highest priority
2. **OpenAI** - Second priority
3. **Anthropic** - Third priority
4. **Google** - Fourth priority

This ensures local models are preferred when available, falling back to cloud providers only when needed.

## 📈 Performance Optimization

### Production Deployment
```bash
# Use Gunicorn for production
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 startup:app

# With logging
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 --access-logfile - --error-logfile - startup:app
```

### Memory Management
- Start with basic installation and add features as needed
- Use local LLMs (Ollama) to reduce API costs
- Configure appropriate chunk sizes for RAG functionality

### Scaling Considerations
- Use Redis for caching (optional)
- Configure load balancing for multiple instances
- Monitor API usage and implement rate limiting

## 🔐 Security

### Production Security Checklist
- [ ] Use strong SECRET_KEY
- [ ] Store API keys securely (environment variables)
- [ ] Enable HTTPS in production
- [ ] Implement rate limiting
- [ ] Use authentication for sensitive endpoints
- [ ] Regular security updates

### Environment Security
```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use secure secret generation
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Docker Deployment
```bash
docker build -t agentic-rag-api .
docker run -p 5000:8080 --env-file .env agentic-rag-api
```

### Azure Container Apps
The application is configured for Azure Container Apps deployment with automatic CI/CD. See `AZURE_CONTAINER_APPS_DEPLOYMENT.md` for detailed deployment instructions.

## 📚 Next Steps

1. **Read the API Documentation**: See `AGENTIC_API_DOCS.md` for detailed API usage
2. **Set up Frontend**: Configure the React UI in the `UI/` directory
3. **Configure RAG**: Set up document processing for enhanced capabilities
4. **Deploy to Production**: Use Azure Container Apps or your preferred platform

## 🆘 Support

### Getting Help
- Check the troubleshooting section above
- Review logs for detailed error messages
- Verify all dependencies are installed correctly
- Ensure environment variables are properly configured

### Common Commands
```bash
# Check Python version
python --version

# List installed packages
pip list

# Check virtual environment
pip show pip

# Test API connectivity
curl http://localhost:5000/api/health

# Check Ollama status
ollama list

# View application logs
tail -f app.log
```

---

## 📝 Additional Documentation

- `AGENTIC_API_DOCS.md` - Complete API documentation and agentic features
- `AZURE_CONTAINER_APPS_DEPLOYMENT.md` - Production deployment guide
- `UI/README.md` - Frontend setup and configuration
