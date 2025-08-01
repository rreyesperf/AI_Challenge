# Travel Chat AI Challenge

A comprehensive travel assistant application with AI-powered chat capabilities, built with Python Flask API and React UI.

## 🏗️ Architecture

This project consists of two main components:

- **API** (`app/`) - Python Flask backend with AI/LLM integration
- **UI** (`app/UI/`) - React frontend for user interaction

## 🚀 Quick Start

### Prerequisites

- Docker
- Azure CLI
- Node.js 18+ (for UI development)
- Python 3.11+ (for API development)

### Local Development

#### API Development
```bash
cd app
pip install -r requirements.txt
python startup.py
```

#### UI Development
```bash
cd app/UI
npm install
npm start
```

## 🐳 Docker Deployment

### Build and Run API
```bash
cd app
docker build -t travel-chat-api .
docker run -p 8080:8080 travel-chat-api
```

### Build and Run UI
```bash
cd app/UI
docker build -t travel-chat-ui .
docker run -p 80:80 travel-chat-ui
```

## ☁️ Azure Deployment

This project uses GitHub Actions for automated deployment to Azure Container Apps:

- **API Deployment** - Triggers on changes to `app/**` (excluding UI)
- **UI Deployment** - Triggers on changes to `app/UI/**`

**Azure Resources:**
- Registry: `registry`
- Resource Group: `resource_group`
- API App: `travel-chat-api-app`
- UI App: `travel-chat-ui-app`

See [Deployment Guide](docs/deployment/DEPLOYMENT.md) for setup instructions.

## 📁 Project Structure

```
├── .github/workflows/          # GitHub Actions
│   ├── deploy-api.yml         # API deployment
│   └── deploy-ui.yml          # UI deployment
├── app/                       # Python Flask API
│   ├── services/              # AI/LLM services
│   ├── auth/                  # Authentication
│   ├── tests/                 # API tests
│   ├── Dockerfile             # API container config
│   ├── requirements.txt       # Python dependencies
│   └── UI/                    # React UI
│       ├── src/               # React source code
│       ├── public/            # Static assets
│       ├── Dockerfile         # UI container config
│       └── package.json       # Node.js dependencies
├── docs/                      # Documentation
│   └── deployment/            # Deployment guides
└── Postman/                   # API testing collection
```

## 🧪 Testing

### API Tests
```bash
cd app
python -m pytest tests/ -v
```

### UI Tests
```bash
cd app/UI
npm test
```

### Postman Collection
Import `Postman/travel_collection.json` for API testing.

## 🔧 Configuration

### Required Environment Variables

#### API
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google API key
- `AZURE_OPENAI_API_KEY` - Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint
- `APP_INSIGHTS_INSTRUMENTATION_KEY` - Application Insights

#### GitHub Secrets (for deployment)
- `AZURE_CREDENTIALS` - Azure service principal
- `ACR_USERNAME` - Container registry username
- `ACR_PASSWORD` - Container registry password

## 📚 Documentation

- [Deployment Guide](docs/deployment/DEPLOYMENT.md) - Complete deployment setup
- [API Documentation](app/AGENTIC_API_DOCS.md) - Python Flask API reference
- [API README](app/README.md) - API development guide
- [UI Documentation](app/UI/README.md) - React UI details

## 🏥 Health Checks

### API Endpoints
- Health: `http://localhost:8080/api/health`
- AI Health: `http://localhost:8080/api/ai/health`
- Providers: `http://localhost:8080/api/ai/providers`

### UI
- Main page: `http://localhost:3000`

## 🛠️ Development Workflow

1. **Make Changes**
   - API changes: Edit files in `app/`
   - UI changes: Edit files in `app/UI/`

2. **Test Locally**
   - Run tests and verify functionality

3. **Deploy**
   - Push to `main` branch
   - GitHub Actions will automatically deploy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

[Add your license information here]

---

**Note**: This is an AI Challenge project focusing on conversational travel assistance with modern deployment practices using Azure Container Apps and GitHub Actions.
