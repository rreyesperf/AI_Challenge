# API GitHub Actions Workflow - Configuration Updates

## ✅ Changes Applied to API Deployment Workflow

The GitHub Actions workflow for the API (`/.github/workflows/deploy.yml`) has been updated to use your specific Azure resources, matching the same configuration pattern used for the UI workflow.

## 🔧 Updated Configuration

### **Environment Variables Changed:**

| Previous (Secrets-based) | Updated (Your Resources) |
|--------------------------|---------------------------|
| `REGISTRY: ${{ secrets.AZURE_CONTAINER_REGISTRY }}` | `AZURE_CONTAINER_REGISTRY: cr81aichallenge-hed7gqfvbbcub6az.azurecr.io` |
| `RESOURCE_GROUP: ${{ secrets.AZURE_RESOURCE_GROUP }}` | `RESOURCE_GROUP_NAME: rg_grupo81` |
| `CONTAINER_APP_NAME: ${{ secrets.AZURE_CONTAINER_APP_NAME }}` | `CONTAINER_APP_NAME: travel-chat-api-app` |
| `CONTAINER_APP_ENV: ${{ secrets.AZURE_CONTAINER_APP_ENV }}` | `CONTAINER_APP_ENV: travel-chat-env` |

### **Authentication Updated:**

| Previous | Updated |
|----------|---------|
| `username: ${{ secrets.AZURE_CLIENT_ID }}` | `username: ${{ secrets.ACR_USERNAME }}` |
| `password: ${{ secrets.AZURE_CLIENT_SECRET }}` | `password: ${{ secrets.ACR_PASSWORD }}` |

## 📋 Required GitHub Secrets for API Deployment

You need to configure the same secrets for the API repository as you did for the UI:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `ACR_USERNAME` | `cr81aichallenge-hed7gqfvbbcub6az` | Container registry username |
| `ACR_PASSWORD` | `[your-acr-password]` | Container registry password |
| `AZURE_CREDENTIALS` | `[service-principal-json]` | Azure service principal for deployment |

### **Additional API-Specific Secrets:**

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `OPENAI_API_KEY` | OpenAI API key for LLM services | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | `anthropic_...` |
| `GOOGLE_API_KEY` | Google AI API key | `google_...` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | `azure_...` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | `https://your-openai.openai.azure.com/` |
| `APP_INSIGHTS_INSTRUMENTATION_KEY` | Azure Application Insights key | `instrumentation-key` |

## 🔄 Workflow Behavior

The updated API workflow will now:

1. **Build and test** the Python Flask API
2. **Build Docker image** and push to `cr81aichallenge-hed7gqfvbbcub6az.azurecr.io`
3. **Deploy to Container App** named `travel-chat-api-app` in resource group `rg_grupo81`
4. **Validate deployment** with health checks and API endpoint tests

## 🎯 Container App Configuration

The workflow deploys with these settings:
- **Target Port**: 8080
- **Ingress**: External (publicly accessible)
- **Environment**: Production-ready with all required environment variables
- **Secrets**: Securely configured for API keys and sensitive data

## 🔗 Integration with UI

Once both deployments are complete:

1. **API will be available** at: `https://travel-chat-api-app.[random-id].azurecontainerapps.io`
2. **Update UI GitHub Secret** `REACT_APP_API_URL` with the API URL
3. **UI will connect** to the deployed API automatically

## ⚡ Quick Setup Steps

1. **Configure GitHub secrets** in your API repository (same as UI secrets)
2. **Add API-specific secrets** for LLM providers (optional, but recommended)
3. **Push to main branch** to trigger automatic deployment
4. **Get the API URL** from deployment logs
5. **Update UI repository** with the API URL as `REACT_APP_API_URL` secret

## 🔍 Validation

After deployment, the workflow automatically tests:
- ✅ Health endpoint (`/api/health`)
- ✅ AI health endpoint (`/api/ai/health`) 
- ✅ Providers endpoint (`/api/ai/providers`)
- ✅ Basic API functionality

## 📊 Deployment Summary

Both your UI and API are now configured for:
- **Consistent naming** and resource usage
- **Same Azure Container Registry** for both applications
- **Same resource group** (`rg_grupo81`) for easy management
- **Automated CI/CD** with comprehensive testing and validation
- **Production-ready** configurations with proper security

Your full-stack travel chat assistant is ready for automated deployment to Azure Container Apps! 🚀
