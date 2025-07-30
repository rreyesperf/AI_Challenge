# Installation Guide for Agentic RAG API

## Step-by-Step Installation

### 1. Core Installation (Required)
Install the basic Flask app first:

```bash
pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2
```

### 2. LLM Providers (Choose What You Need)

#### OpenAI (Recommended - also supports Azure OpenAI)
```bash
pip install openai==1.35.3
```

#### Anthropic Claude (Optional)
```bash
pip install anthropic==0.25.9
```

#### Google Gemini (Optional)
```bash
pip install google-generativeai==0.5.4
```

### 3. Document Processing (Optional)
Only install if you want to process documents:

```bash
pip install PyPDF2==3.0.1 python-docx==1.1.0
```

### 4. RAG Capabilities (Optional)
Only install if you want RAG functionality:

```bash
pip install numpy==1.26.4
pip install sentence-transformers==2.7.0
pip install tiktoken==0.7.0
pip install chromadb==0.4.24
```

## Alternative: All-in-One Installation

If you want everything:

```bash
pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2 openai==1.35.3 anthropic==0.25.9 google-generativeai==0.5.4 PyPDF2==3.0.1 python-docx==1.1.0 numpy==1.26.4 sentence-transformers==2.7.0 tiktoken==0.7.0 chromadb==0.4.24
```

## Troubleshooting Common Issues

### 1. ChromaDB Installation Issues
If ChromaDB fails to install:
```bash
# Try installing dependencies first
pip install numpy==1.26.4 sqlite3
pip install chromadb==0.4.24
```

### 2. Sentence Transformers Issues
If sentence-transformers fails:
```bash
# Install PyTorch first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers==2.7.0
```

### 3. Windows-Specific Issues
On Windows, you might need:
```bash
# Install Visual C++ Build Tools if compilation fails
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use pre-compiled wheels
pip install --only-binary=all chromadb
```

### 4. macOS-Specific Issues
On macOS:
```bash
# Install Xcode command line tools if needed
xcode-select --install

# Install dependencies
brew install sqlite3
```

## Minimal Working Setup

For a minimal working setup with just OpenAI:

```bash
pip install Flask==3.0.0 requests==2.31.0 python-dotenv==1.0.1 beautifulsoup4==4.12.2 openai==1.35.3
```

Then set your environment variable:
```bash
export OPENAI_API_KEY=your_key_here
```

## Testing Installation

After installation, test with:

```python
# test_install.py
try:
    import flask
    print("✓ Flask installed")
except ImportError:
    print("✗ Flask not installed")

try:
    import openai
    print("✓ OpenAI installed")
except ImportError:
    print("✗ OpenAI not installed")

try:
    import anthropic
    print("✓ Anthropic installed")
except ImportError:
    print("✗ Anthropic not installed")

try:
    import google.generativeai
    print("✓ Google Generative AI installed")
except ImportError:
    print("✗ Google Generative AI not installed")

try:
    import chromadb
    print("✓ ChromaDB installed")
except ImportError:
    print("✗ ChromaDB not installed")

print("\nInstallation test complete!")
```

Run with: `python test_install.py`

## Environment Setup

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

3. Start the application:
```bash
python app.py
```

## What Works With Minimal Installation

Even with just the core packages, you'll have:
- ✓ Flask web server
- ✓ Basic chat endpoints 
- ✓ OpenAI integration (if API key provided)
- ✓ Travel planning agent (basic functionality)
- ✓ Health check endpoints

Additional features require their respective packages:
- RAG functionality → ChromaDB + sentence-transformers
- Document processing → PyPDF2 + python-docx
- Multiple LLM providers → anthropic + google-generativeai
