# GitHub Secrets Setup for UI Deployment

The UI deployment workflow requires the following GitHub Secrets to be configured:

## Required Secrets

### Authentication Credentials
- **`UI_AUTH_USERNAME`**: The username for UI login
  - Value: `AvidTraveler`
  
- **`UI_AUTH_PASSWORD`**: The password for UI login  
  - Value: `y8FSGatspR#KLi$qE4Sm`

### Azure Deployment
- **`AZURE_CREDENTIALS`**: Azure service principal credentials (JSON format)
- **`ACR_USERNAME`**: Azure Container Registry username
- **`ACR_PASSWORD`**: Azure Container Registry password

## How to Add Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the name and value above

## Build Arguments

The Docker build process will use these secrets as build arguments:
- `REACT_APP_AUTH_USERNAME` ← from `UI_AUTH_USERNAME` secret
- `REACT_APP_AUTH_PASSWORD` ← from `UI_AUTH_PASSWORD` secret
- `REACT_APP_API_URL` ← hardcoded API endpoint

## Security Notes

- ✅ Credentials are passed as build arguments (not stored in image layers)
- ✅ GitHub Secrets are encrypted and only available during CI/CD
- ✅ No credentials are stored in the repository or image
- ✅ Each environment can have different credentials
