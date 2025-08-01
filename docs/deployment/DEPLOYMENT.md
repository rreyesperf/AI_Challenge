# Deployment Guide

## Overview

This project uses **two separate GitHub Actions workflows** for independent deployments:

- **API Deployment** (`deploy-api.yml`) - Python Flask API from `app/`
- **UI Deployment** (`deploy-ui.yml`) - React UI from `app/UI/`

## File Structure

```
├── .github/workflows/
│   ├── deploy-api.yml    # API deployment workflow
│   └── deploy-ui.yml     # UI deployment workflow
├── app/
│   ├── Dockerfile        # API Docker config
│   └── UI/
│       └── Dockerfile    # UI Docker config
```

## How Deployments Work

### API Deployment
- **Triggers**: Changes to `app/**` (excluding `app/UI/**`)
- **Deploys**: `travel-chat-api-app` Container App
- **Port**: 8080

### UI Deployment  
- **Triggers**: Changes to `app/UI/**`
- **Deploys**: `travel-chat-ui-app` Container App
- **Port**: 80

## Required GitHub Secrets

Configure these in GitHub repository settings:

```
AZURE_CREDENTIALS           # Azure service principal JSON
ACR_USERNAME                # Container registry username
ACR_PASSWORD                # Container registry password
OPENAI_API_KEY             # OpenAI API key
ANTHROPIC_API_KEY          # Anthropic API key
GOOGLE_API_KEY             # Google API key
AZURE_OPENAI_API_KEY       # Azure OpenAI API key
AZURE_OPENAI_ENDPOINT      # Azure OpenAI endpoint
APP_INSIGHTS_INSTRUMENTATION_KEY  # Application Insights
```

## Azure Resources

```
Registry: cr81aichallenge-hed7gqfvbbcub6az.azurecr.io
Resource Group: rg_grupo81
Environment: travel-chat-env
API App: travel-chat-api-app
UI App: travel-chat-ui-app
```

## Testing Deployments

### Test API Deployment
```bash
echo "# Test" >> app/README.md
git add app/README.md
git commit -m "Test API deployment"
git push
```

### Test UI Deployment
```bash
echo "/* Test */" >> app/UI/src/App.css
git add app/UI/src/App.css
git commit -m "Test UI deployment"
git push
```

## Health Checks

- **API**: `https://your-api-url/api/health`
- **UI**: `https://your-ui-url/` (main page)

## Troubleshooting

1. **Secret errors**: Verify all secrets are configured in GitHub
2. **Build failures**: Check Docker configurations and dependencies
3. **Deployment timeouts**: Monitor Azure resource limits
