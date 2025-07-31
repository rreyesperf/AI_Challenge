# Local LLM Integration Guide

This guide explains how to set up and use local LLM services with your AI Travel Platform.

## Supported Local LLM Solutions

### 1. Ollama (Recommended)
Ollama is the easiest way to run local LLMs. It provides a simple API and manages model downloads automatically.

#### Installation
```bash
# Windows (using installer)
# Download from: https://ollama.ai/download

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Setup
```bash
# Start Ollama service (usually runs automatically after installation)
ollama serve

# Pull and run models
ollama pull llama2          # 7B parameter model
ollama pull codellama       # Code-focused model
ollama pull mistral         # 7B parameter model
ollama pull neural-chat     # Optimized for chat

# List available models
ollama list

# Test the model
ollama run llama2 "Hello, how are you?"
```

#### Configuration
Add to your environment variables or `.env` file:
```bash
# Ollama configuration (optional - defaults shown)
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LLM_PROVIDER=ollama_llama2
```

### 2. Local OpenAI-Compatible Servers

#### Text Generation WebUI
```bash
# Clone and setup
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
pip install -r requirements.txt

# Run with OpenAI API compatibility
python server.py --api --listen --listen-port 8000
```

#### LM Studio
1. Download from: https://lmstudio.ai/
2. Install and download a model (e.g., Llama 2, Code Llama)
3. Start local server with OpenAI API compatibility
4. Default runs on `http://localhost:11434`

#### Configuration
```bash
# Local LLM server configuration
LOCAL_LLM_BASE_URL=http://localhost:11434  # or http://localhost:1234 for LM Studio
LOCAL_LLM_API_KEY=your_api_key_if_required  # Optional
DEFAULT_LLM_PROVIDER=local_llm
```

## Environment Variables

Add these to your `.env` file or environment:

```bash
# Ollama (runs on port 11434 by default)
OLLAMA_BASE_URL=http://localhost:11434

# Generic local LLM server (OpenAI-compatible)
LOCAL_LLM_BASE_URL=http://localhost:8000
LOCAL_LLM_API_KEY=optional_api_key

# Set default provider to use local LLM
DEFAULT_LLM_PROVIDER=ollama  # or ollama_llama2, local_llm, etc.
```

## Available Providers

After setup, your application will automatically detect and register these providers:

### Ollama Providers
- `ollama` - Default Ollama model
- `ollama_llama2` - Llama 2 model
- `ollama_codellama` - Code Llama model
- `ollama_mistral` - Mistral model
- `ollama_neural-chat` - Neural Chat model

### Local LLM Providers
- `local_llm` - Generic OpenAI-compatible local server

## Usage Examples

### 1. Using Local LLM via API

```bash
# Test with curl
curl -X POST http://localhost:5000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Plan a trip to Paris",
    "provider": "ollama_llama2"
  }'
```

### 2. Using in Python Code

```python
from services.llm_service import llm_service

# Generate response with local Ollama
response = llm_service.generate_response(
    prompt="What are the best travel destinations?",
    provider_name="ollama_llama2",
    max_tokens=500,
    temperature=0.7
)

# Chat completion with local LLM
messages = [
    {"role": "user", "content": "I want to plan a trip to Japan"}
]
response = llm_service.chat_completion(
    messages=messages,
    provider_name="local_llm"
)
```

### 3. Using Travel Agent with Local LLM

```bash
curl -X POST http://localhost:5000/api/ai/travel-agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Plan a weekend trip to New York",
    "flight_params": {
      "origin": "Boston",
      "destination": "New York",
      "departureDate": "2025-08-15",
      "returnDate": "2025-08-17"
    }
  }'
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Make sure the local LLM service is running
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Check if local LLM server is running
   curl http://localhost:8000/v1/models
   ```

2. **Model Not Found**: Ensure the model is downloaded
   ```bash
   # For Ollama
   ollama pull llama2
   
   # For other servers, check their documentation
   ```

3. **Slow Response**: Local LLMs can be slower than cloud APIs
   - Use smaller models for faster responses
   - Consider using GPU acceleration if available
   - Adjust timeout settings if needed

### Performance Tips

1. **Model Selection**:
   - 7B models (Llama 2, Mistral): Good balance of speed and quality
   - 13B+ models: Better quality but slower
   - Code models: Better for technical content

2. **Hardware Recommendations**:
   - Minimum: 8GB RAM for 7B models
   - Recommended: 16GB RAM + GPU for better performance
   - SSD storage for faster model loading

3. **Configuration Optimization**:
   - Adjust `max_tokens` and `temperature` based on your needs
   - Use shorter prompts for faster responses
   - Cache frequently used responses

## Security Considerations

1. **Local Network**: Local LLMs run on your network, keeping data private
2. **No API Keys**: No need to share sensitive data with external services
3. **Firewall**: Ensure local LLM ports are not exposed to the internet
4. **Resource Usage**: Monitor CPU/RAM/GPU usage

## Monitoring and Logs

The application logs local LLM connection status:
- Check application logs for connection success/failure
- Monitor response times in the logs
- Use health check endpoints to verify service status

```bash
# Check provider status
curl http://localhost:5000/api/ai/health
```

## Model Recommendations

### For Travel Planning:
- **Llama 2**: Great general purpose model
- **Mistral**: Good balance of speed and intelligence
- **Neural Chat**: Optimized for conversational AI

### For Code Generation:
- **Code Llama**: Specialized for code tasks
- **Deepseek Coder**: Alternative code-focused model

### For Performance:
- **TinyLlama**: Very fast, smaller model for simple tasks
- **Phi-2**: Microsoft's efficient small model

## Next Steps

1. Install Ollama or your preferred local LLM solution
2. Download and test a model
3. Update your environment variables
4. Test the integration using the API endpoints
5. Monitor performance and adjust settings as needed

For more advanced setups, consider:
- GPU acceleration
- Model quantization for better performance
- Multiple model deployment for different use cases
- Custom fine-tuned models for travel-specific tasks
