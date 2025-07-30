# Quick Start Guide

## Installation

1. **Install core dependencies:**
   ```bash
   pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2
   ```

2. **Install OpenAI (recommended):**
   ```bash
   pip install openai==1.35.3
   ```

3. **Set up environment:**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env and add your API key:
   OPENAI_API_KEY=your_key_here
   ```

## Running the Application

### Method 1: Using flask run (recommended)
```bash
flask run
```

### Method 2: Using python directly
```bash
python app.py
```

### Method 3: Using python with routes
```bash
python routes.py
```

## Testing the Installation

1. **Check what's working:**
   ```bash
   python test_installation.py
   ```

2. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:5000/api/health
   
   # AI health check (if LLM installed)
   curl http://localhost:5000/api/ai/health
   ```

## Available Endpoints

- `GET /` - API information
- `GET /api/health` - Service status
- `GET /api/ai/health` - AI service status
- `POST /api/ai/chat` - Basic chat (requires LLM)
- `GET /api/flights` - Flight search (if service available)
- `GET /api/hotels` - Hotel search (if service available)

## Troubleshooting

### If `flask run` doesn't work:
1. Make sure Flask is installed: `pip install Flask`
2. Check if `.flaskenv` file exists
3. Try: `python app.py` instead

### If you get import errors:
- The app is designed to work with missing services
- Check which services are available at `/api/health`
- Install missing packages as needed

### If no AI features work:
- Install OpenAI: `pip install openai==1.35.3`
- Set your API key in `.env`
- Check `/api/ai/health` for status

## What Works with Minimal Installation

Even with just Flask + OpenAI, you get:
- ✅ Web server running
- ✅ Health check endpoints
- ✅ Basic chat functionality
- ✅ Service status monitoring
- ⚠️ Other services gracefully disabled
