from flask import Flask, request, jsonify
import logging

# Import the enhanced services
try:
    from services.lmintegration import (
        enhanced_chat_service, 
        health_check_service,
        list_providers_service,
        LLM_SERVICE_AVAILABLE
    )
    ENHANCED_SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Enhanced services not available: {e}")
    ENHANCED_SERVICES_AVAILABLE = False

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application with minimal endpoints"""
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Security headers
    @app.after_request
    def after_request(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint"""
        return jsonify({
            "message": "Agentic RAG API with Enhanced Conversational Travel Assistant",
            "version": "2.0",
            "status": "running",
            "available_endpoints": [
                "/api/ai/chat",
                "/api/health", 
                "/api/ai/health"
            ]
        })

    # Main chat endpoint - the only public AI endpoint
    @app.route('/api/ai/chat', methods=['POST'])
    def enhanced_ai_chat():
        """Enhanced conversational chat endpoint with travel planning capabilities"""
        if not ENHANCED_SERVICES_AVAILABLE or not LLM_SERVICE_AVAILABLE:
            return jsonify({'error': 'Enhanced chat service not available. Install required packages.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({'error': 'Invalid request. Missing "message" field.'}), 400

            user_message = data['message']
            conversation_history = data.get('conversation_history', [])
            provider = data.get('provider')
            system_message = data.get('system_message')
            max_tokens = data.get('max_tokens')
            temperature = data.get('temperature')

            # Use enhanced chat service
            response = enhanced_chat_service(
                message=user_message,
                conversation_history=conversation_history,
                provider_name=provider,
                system_message=system_message,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return jsonify(response)

        except Exception as e:
            logger.error(f"Error in enhanced AI chat endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    # Health check endpoints (kept for monitoring)
    @app.route('/api/health', methods=['GET'])
    def health():
        """General health check endpoint"""
        return jsonify({
            "status": "healthy",
            "timestamp": "2025-01-01T00:00:00",
            "services": {
                "enhanced_chat": ENHANCED_SERVICES_AVAILABLE,
                "llm_service": LLM_SERVICE_AVAILABLE
            }
        })

    @app.route('/api/ai/health', methods=['GET'])
    def ai_health():
        """AI-specific health check endpoint"""
        if not ENHANCED_SERVICES_AVAILABLE:
            return jsonify({
                "status": "unhealthy",
                "error": "Enhanced services not available"
            }), 503
        
        try:
            health_data = health_check_service()
            return jsonify(health_data)
        except Exception as e:
            logger.error(f"Error in AI health check: {e}")
            return jsonify({'error': str(e)}), 500

    # Optional: Providers endpoint for debugging (can be removed in production)
    @app.route('/api/ai/providers', methods=['GET'])
    def ai_providers():
        """List available AI providers"""
        if not ENHANCED_SERVICES_AVAILABLE:
            return jsonify({'error': 'Enhanced services not available'}), 503
        
        try:
            providers_data = list_providers_service()
            return jsonify(providers_data)
        except Exception as e:
            logger.error(f"Error listing providers: {e}")
            return jsonify({'error': str(e)}), 500

    return app

# For compatibility with existing startup scripts
def register_ai_routes(app):
    """Compatibility function - routes are now registered in create_app"""
    pass

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
