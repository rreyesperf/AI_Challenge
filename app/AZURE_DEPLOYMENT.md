# Azure Container Apps Configuration for Agentic RAG API

## Environment Variables for Azure Container Apps

Configure these environment variables in your Azure Container Apps environment:

### Required Environment Variables:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# At least one LLM provider API key is required:
OPENAI_API_KEY=your-openai-api-key
# OR/AND
ANTHROPIC_API_KEY=your-anthropic-api-key
# OR/AND  
GOOGLE_API_KEY=your-google-api-key
# OR/AND
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure Application Insights (Optional but recommended)
APP_INSIGHTS_INSTRUMENTATION_KEY=your-app-insights-key

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=/app/data/chroma

# LLM Configuration (Optional - has defaults)
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-3.5-turbo
MAX_TOKENS=2000
TEMPERATURE=0.7

# RAG Configuration (Optional - has defaults)  
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7

# Azure API Management Integration (Optional)
APIM_SUBSCRIPTION_KEY=your-apim-subscription-key
APIM_BASE_URL=https://your-apim.azure-api.net

# Rate Limiting (Optional)
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=100

# Logging (Optional)
LOG_LEVEL=INFO
```

## Azure Container Apps Configuration

### Container Configuration:
```yaml
properties:
  configuration:
    ingress:
      external: true
      targetPort: 8080
      transport: http
      traffic:
      - weight: 100
        latestRevision: true
  template:
    containers:
    - image: your-registry.azurecr.io/agentic-rag-api:latest
      name: agentic-rag-api
      resources:
        cpu: 1.0
        memory: 2Gi
      env:
      - name: FLASK_ENV
        value: "production"
      - name: SECRET_KEY
        secretRef: secret-key
      - name: OPENAI_API_KEY
        secretRef: openai-api-key
      # ... other environment variables
    scale:
      minReplicas: 1
      maxReplicas: 10
      rules:
      - name: http-rule
        http:
          metadata:
            concurrentRequests: "100"
```

## Azure API Management Integration

### API Definition for APIM:

1. **Base URL**: Use your Container Apps URL (e.g., `https://your-app.domain.azurecontainerapps.io`)

2. **API Operations**:
   - GET `/api/health` - Health check
   - GET `/api/ai/health` - AI services health
   - GET `/api/ai/providers` - List LLM providers
   - POST `/api/ai/chat` - Basic chat
   - POST `/api/ai/conversation` - Multi-turn conversation  
   - POST `/api/ai/travel-agent` - Travel planning agent
   - POST `/api/ai/rag/ingest` - Document ingestion
   - POST `/api/ai/rag/query` - RAG query
   - DELETE `/api/ai/rag/delete` - Delete document
   - POST `/api/ai/consensus` - Multi-provider consensus

3. **APIM Policies** (apply at API level):
```xml
<policies>
    <inbound>
        <base />
        <rate-limit calls="1000" renewal-period="60" />
        <quota calls="10000" renewal-period="3600" />
        <cors>
            <allowed-origins>
                <origin>*</origin>
            </allowed-origins>
            <allowed-methods>
                <method>GET</method>
                <method>POST</method>
                <method>DELETE</method>
                <method>OPTIONS</method>
            </allowed-methods>
            <allowed-headers>
                <header>*</header>
            </allowed-headers>
        </cors>
        <set-header name="X-Forwarded-Proto" exists-action="override">
            <value>https</value>
        </set-header>
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
        <set-header name="X-Powered-By" exists-action="delete" />
        <set-header name="Server" exists-action="delete" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

## SSL/TLS Configuration

Azure Container Apps automatically handles SSL termination at the ingress level. Your container runs on HTTP port 8080, but external traffic comes in via HTTPS on port 443. No additional SSL configuration is needed in your application.

## Deployment Steps

1. **Build and push Docker image**:
   ```bash
   docker build -t your-registry.azurecr.io/agentic-rag-api:latest .
   docker push your-registry.azurecr.io/agentic-rag-api:latest
   ```

2. **Create Azure Container Apps environment**:
   ```bash
   az containerapp env create \
     --name myapp-env \
     --resource-group myapp-rg \
     --location eastus2
   ```

3. **Deploy Container App**:
   ```bash
   az containerapp create \
     --name agentic-rag-api \
     --resource-group myapp-rg \
     --environment myapp-env \
     --image your-registry.azurecr.io/agentic-rag-api:latest \
     --target-port 8080 \
     --ingress external \
     --cpu 1.0 \
     --memory 2Gi \
     --min-replicas 1 \
     --max-replicas 10 \
     --env-vars FLASK_ENV=production
   ```

4. **Configure secrets** (for API keys):
   ```bash
   az containerapp secret set \
     --name agentic-rag-api \
     --resource-group myapp-rg \
     --secrets openai-api-key=your-openai-key secret-key=your-secret-key
   ```

## Monitoring and Logging

- **Application Insights**: Automatically integrated if `APP_INSIGHTS_INSTRUMENTATION_KEY` is provided
- **Container Apps Logs**: Available through Azure Monitor
- **Health Checks**: Built-in health endpoint at `/api/health`
- **Metrics**: Container CPU, memory, and request metrics available in Azure Portal

## Security Considerations

- All API keys stored as Azure Container Apps secrets
- HTTPS enforced at ingress level
- Security headers automatically applied
- Rate limiting configured in Azure API Management
- Non-root container user for enhanced security
- Minimal container image with only required dependencies

## Scaling Configuration

The app is configured to scale from 1 to 10 replicas based on HTTP concurrent requests. Adjust based on your expected load:

- **Light usage**: 1-3 replicas, 0.5 CPU, 1Gi memory
- **Medium usage**: 1-5 replicas, 1.0 CPU, 2Gi memory  
- **Heavy usage**: 2-10 replicas, 2.0 CPU, 4Gi memory
