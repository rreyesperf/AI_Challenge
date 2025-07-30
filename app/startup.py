#!/usr/bin/env python3
"""
Production-ready startup script for the Agentic RAG API
Handles both local development and Azure Container Apps deployment
"""

import os
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def setup_logging():
    """Configure logging based on environment"""
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = os.environ.get('LOG_FORMAT', '%(asctime)s %(levelname)s %(name)s %(message)s')
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def create_data_directories():
    """Create necessary data directories"""
    data_dir = Path('/app/data')
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        
    chroma_dir = data_dir / 'chroma'
    if not chroma_dir.exists():
        chroma_dir.mkdir(parents=True, exist_ok=True)
        
    # Set permissions for non-root user
    try:
        os.chmod(str(data_dir), 0o755)
        os.chmod(str(chroma_dir), 0o755)
    except Exception as e:
        print(f"Warning: Could not set directory permissions: {e}")

def main():
    """Main application entry point"""
    # Setup logging first
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create necessary directories
    create_data_directories()
    
    # Import and create Flask app
    try:
        from routes import create_app
        app = create_app()
        
        # Log startup information
        flask_env = os.environ.get('FLASK_ENV', 'development')
        port = int(os.environ.get('PORT', 8080))
        host = os.environ.get('HOST', '0.0.0.0')
        
        logger.info(f"Starting Agentic RAG API in {flask_env} mode")
        logger.info(f"Listening on {host}:{port}")
        
        # Check for available services
        try:
            from services.llm_service import LLM_SERVICE_AVAILABLE
            logger.info(f"LLM Service Available: {LLM_SERVICE_AVAILABLE}")
        except ImportError:
            logger.warning("LLM Service not available")
            
        try:
            from services.rag_service import RAG_SERVICE_AVAILABLE  
            logger.info(f"RAG Service Available: {RAG_SERVICE_AVAILABLE}")
        except ImportError:
            logger.warning("RAG Service not available")
        
        # Start the application
        if flask_env == 'development':
            # Development mode - use Flask dev server
            app.run(host=host, port=port, debug=True)
        else:
            # Production mode - this should be handled by Gunicorn
            logger.info("Production mode detected. This script should be run via Gunicorn.")
            logger.info("Use: gunicorn --bind 0.0.0.0:8080 startup:app")
            return app
            
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

# For Gunicorn
app = None
if __name__ != '__main__':
    setup_logging()
    create_data_directories()
    from routes import create_app
    app = create_app()
else:
    main()
