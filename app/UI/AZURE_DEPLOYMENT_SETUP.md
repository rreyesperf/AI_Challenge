# Azure Container Apps Deployment Setup Guide

This guide walks you through setting up automated deployment of the React UI to Azure Container Apps using GitHub Actions.

## 🔧 Prerequisites

- Azure subscription with appropriate permissions
- GitHub repository with the React UI code
- Azure CLI installed locally (for initial setup)

## 🚀 Step 1: Create Azure Resources

### 1.1 Create Resource Group
```bash
az group create \
  --name travel-chat-rg \
  --location eastus
```

### 1.2 Create Azure Container Registry (ACR)
```bash
az acr create \
  --resource-group travel-chat-rg \
  --name travelchatui \
  --sku Basic \
  --admin-enabled true
```

### 1.3 Get ACR Credentials
```bash
az acr credential show --name travelchatui --resource-group travel-chat-rg
```
Save the username and password for GitHub secrets.

### 1.4 Create Container Apps Environment
```bash
az containerapp env create \
  --name travel-chat-env \
  --resource-group travel-chat-rg \
  --location eastus
```

### 1.5 Create Container App
```bash
az containerapp create \
  --name travel-chat-ui-app \
  --resource-group travel-chat-rg \
  --environment travel-chat-env \
  --image travelchatui.azurecr.io/travel-chat-ui:latest \
  --target-port 8080 \
  --ingress external \
  --registry-server travelchatui.azurecr.io \
  --registry-username $(az acr credential show --name travelchatui --query username -o tsv) \
  --registry-password $(az acr credential show --name travelchatui --query passwords[0].value -o tsv) \
  --env-vars REACT_APP_API_URL=https://your-backend-api.azurecontainerapps.io \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 1 \
  --max-replicas 3
```

## 🔐 Step 2: Configure GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

### Required Secrets:

1. **ACR_USERNAME**
   ```
   Value: Output from az acr credential show command (username)
   ```

2. **ACR_PASSWORD**
   ```
   Value: Output from az acr credential show command (password)
   ```

3. **AZURE_CREDENTIALS**
   Create a service principal:
   ```bash
   az ad sp create-for-rbac \
     --name "travel-chat-ui-deploy" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/travel-chat-rg \
     --sdk-auth
   ```
   Use the entire JSON output as the secret value.

4. **REACT_APP_API_URL**
   ```
   Value: https://your-backend-api.azurecontainerapps.io
   ```

### Optional Environment Configuration:

5. **AZURE_CONTAINER_REGISTRY** (if different from default)
   ```
   Value: youracr.azurecr.io
   ```

6. **RESOURCE_GROUP_NAME** (if different from default)
   ```
   Value: your-resource-group-name
   ```

7. **CONTAINER_APP_NAME** (if different from default)
   ```
   Value: your-container-app-name
   ```

## 📝 Step 3: Update Workflow Configuration

Edit `.github/workflows/deploy-ui.yml` and update these variables if needed:

```yaml
env:
  AZURE_CONTAINER_REGISTRY: travelchatui.azurecr.io  # Your ACR name
  IMAGE_NAME: travel-chat-ui
  CONTAINER_APP_NAME: travel-chat-ui-app  # Your Container App name
  RESOURCE_GROUP_NAME: travel-chat-rg  # Your resource group name
```

## 🔄 Step 4: Deployment Process

### Automatic Deployment
The workflow automatically triggers on:
- Push to `main` or `production` branches (when UI files change)
- Pull requests to `main` or `production` branches
- Manual dispatch from GitHub Actions tab

### Manual Deployment
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Deploy React UI to Azure Container Apps"
4. Click "Run workflow"
5. Choose environment (production/staging)

## 🔍 Step 5: Monitoring and Validation

### Health Check Endpoints
- **Application**: `https://your-app-url.azurecontainerapps.io/`
- **Health Check**: `https://your-app-url.azurecontainerapps.io/health`

### Azure CLI Monitoring
```bash
# Check container app status
az containerapp show \
  --name travel-chat-ui-app \
  --resource-group travel-chat-rg

# View logs
az containerapp logs show \
  --name travel-chat-ui-app \
  --resource-group travel-chat-rg \
  --follow

# Check revisions
az containerapp revision list \
  --name travel-chat-ui-app \
  --resource-group travel-chat-rg
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check Node.js version compatibility
   - Verify package.json and dependencies
   - Review test failures in GitHub Actions logs

2. **Docker Build Failures**
   - Check Dockerfile syntax
   - Verify .dockerignore excludes unnecessary files
   - Check if all required build args are provided

3. **Deployment Failures**
   - Verify Azure credentials are correct
   - Check if Container Registry permissions are set
   - Ensure Container App configuration is valid

4. **Runtime Issues**
   - Check environment variables are set correctly
   - Verify API URL is accessible from Container Apps
   - Review application logs in Azure

### Debug Commands:
```bash
# Test Docker build locally
docker build -t travel-chat-ui:test ./UI

# Test container locally
docker run -p 8080:8080 travel-chat-ui:test

# Check ACR repositories
az acr repository list --name travelchatui

# Check Container App logs
az containerapp logs show --name travel-chat-ui-app --resource-group travel-chat-rg
```

## 🔄 Rollback Process

If deployment fails or issues are found:

1. **Automatic Rollback**: The workflow includes basic failure detection
2. **Manual Rollback**: 
   ```bash
   # List revisions
   az containerapp revision list --name travel-chat-ui-app --resource-group travel-chat-rg
   
   # Activate previous revision
   az containerapp revision activate \
     --revision <previous-revision-name> \
     --resource-group travel-chat-rg
   ```

## 📊 Performance Optimization

### Container Apps Configuration:
- **CPU**: 0.5 cores (adjust based on traffic)
- **Memory**: 1Gi (adjust based on application needs)
- **Replicas**: 1-3 (auto-scaling based on load)

### Nginx Optimizations:
- Gzip compression enabled
- Static asset caching (1 year)
- Security headers configured
- Health check endpoint optimized

## 🔒 Security Considerations

1. **Secrets Management**: All sensitive data stored in GitHub Secrets
2. **Container Security**: Non-root user configuration
3. **Network Security**: HTTPS-only access through Azure Container Apps
4. **Image Security**: Multi-stage builds to minimize attack surface
5. **Access Control**: Least privilege principle for service principals

## 📈 Scaling and Performance

The Container App is configured to auto-scale based on:
- HTTP requests per second
- CPU utilization
- Memory usage

Scale settings can be adjusted:
```bash
az containerapp update \
  --name travel-chat-ui-app \
  --resource-group travel-chat-rg \
  --min-replicas 2 \
  --max-replicas 10
```
