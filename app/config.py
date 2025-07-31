import os

class Config:
    DEBUG = False
    APP_INSIGHTS_INSTRUMENTATION_KEY = os.environ.get('APP_INSIGHTS_INSTRUMENTATION_KEY')
    
    # LLM API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    # Local LLM Configuration
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    LOCAL_LLM_BASE_URL = os.environ.get('LOCAL_LLM_BASE_URL', 'http://localhost:11434')  # Updated for LM Studio default
    LOCAL_LLM_API_KEY = os.environ.get('LOCAL_LLM_API_KEY')  # Optional for local servers
    
    # Vector Database Configuration
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    CHROMA_PERSIST_DIRECTORY = os.environ.get('CHROMA_PERSIST_DIRECTORY', './data/chroma')
    
    # Default LLM Settings
    DEFAULT_LLM_PROVIDER = os.environ.get('DEFAULT_LLM_PROVIDER', 'local_llm')
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'local-model')
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '2000'))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))
    
    # RAG Settings
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', '200'))
    TOP_K_RESULTS = int(os.environ.get('TOP_K_RESULTS', '5'))
    SIMILARITY_THRESHOLD = float(os.environ.get('SIMILARITY_THRESHOLD', '0.7'))
    
    # Other configuration settings...
