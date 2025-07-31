"""
Production configuration for Azure Container Apps deployment
"""
import os
from typing import Optional

class Config:
    """Base configuration with secure defaults for Azure Container Apps"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # Azure Application Insights
    APP_INSIGHTS_INSTRUMENTATION_KEY = os.environ.get('APP_INSIGHTS_INSTRUMENTATION_KEY')
    
    # LLM API Keys - Configure at least one
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIRECTORY = os.environ.get('CHROMA_PERSIST_DIRECTORY', '/app/data/chroma')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    
    # LLM Configuration
    DEFAULT_LLM_PROVIDER = os.environ.get('DEFAULT_LLM_PROVIDER', 'openai')
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '2000'))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))
    
    # RAG Configuration
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', '200'))
    TOP_K_RESULTS = int(os.environ.get('TOP_K_RESULTS', '5'))
    SIMILARITY_THRESHOLD = float(os.environ.get('SIMILARITY_THRESHOLD', '0.7'))
    
    # Azure API Management Integration
    APIM_SUBSCRIPTION_KEY = os.environ.get('APIM_SUBSCRIPTION_KEY')
    APIM_BASE_URL = os.environ.get('APIM_BASE_URL')
    
    # Rate Limiting (for Azure API Management)
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.environ.get('RATE_LIMIT_REQUESTS_PER_MINUTE', '100'))
    
    # Security Headers for production
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'"
    }
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
    
    # Health Check Configuration
    HEALTH_CHECK_ENABLED = True
    HEALTH_CHECK_INTERVAL = int(os.environ.get('HEALTH_CHECK_INTERVAL', '30'))
    
    @classmethod
    def get_provider_config(cls, provider_name: str) -> dict:
        """Get configuration for a specific LLM provider"""
        configs = {
            'openai': {
                'api_key': cls.OPENAI_API_KEY,
                'model': cls.DEFAULT_MODEL,
                'available': cls.OPENAI_API_KEY is not None
            },
            'azure_openai': {
                'api_key': cls.AZURE_OPENAI_API_KEY,
                'endpoint': cls.AZURE_OPENAI_ENDPOINT,
                'api_version': cls.AZURE_OPENAI_API_VERSION,
                'available': all([cls.AZURE_OPENAI_API_KEY, cls.AZURE_OPENAI_ENDPOINT])
            },
            'anthropic': {
                'api_key': cls.ANTHROPIC_API_KEY,
                'available': cls.ANTHROPIC_API_KEY is not None
            },
            'google': {
                'api_key': cls.GOOGLE_API_KEY,
                'available': cls.GOOGLE_API_KEY is not None
            }
        }
        return configs.get(provider_name, {})
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available LLM providers based on configuration"""
        providers = []
        for provider in ['openai', 'azure_openai', 'anthropic', 'google']:
            config = cls.get_provider_config(provider)
            if config.get('available', False):
                providers.append(provider)
        return providers

class ProductionConfig(Config):
    """Production specific configuration"""
    DEBUG = False
    TESTING = False
    
    # Force HTTPS in production
    PREFERRED_URL_SCHEME = 'https'
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Development specific configuration"""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing specific configuration"""
    TESTING = True
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig  # Default to production for Azure
}

# Export the appropriate configuration based on environment
CONFIG_NAME = os.environ.get('FLASK_ENV', 'production')
Config = config.get(CONFIG_NAME, ProductionConfig)
