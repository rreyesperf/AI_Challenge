from flask import Flask, request, jsonify, Blueprint
import logging
import os

# Graceful imports for services
try:
    from services.flights import find_flights_by_criteria
    FLIGHTS_AVAILABLE = True
except ImportError:
    FLIGHTS_AVAILABLE = False
    print("Warning: flights service not available")

try:
    from services.transportation import find_transportation_options
    TRANSPORTATION_AVAILABLE = True
except ImportError:
    TRANSPORTATION_AVAILABLE = False
    print("Warning: transportation service not available")

try:
    from services.hotels import find_hotels_by_criteria
    HOTELS_AVAILABLE = True
except ImportError:
    HOTELS_AVAILABLE = False
    print("Warning: hotels service not available")

try:
    from services.aggregation import aggregate_results
    AGGREGATION_AVAILABLE = True
except ImportError:
    AGGREGATION_AVAILABLE = False
    print("Warning: aggregation service not available")

try:
    from services.dining import find_dining_options
    DINING_AVAILABLE = True
except ImportError:
    DINING_AVAILABLE = False
    print("Warning: dining service not available")

try:
    from services.llm_service import llm_service
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM service not available - AI endpoints disabled")

try:
    from services.rag_service import rag_service
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Warning: RAG service not available - document processing disabled")

try:
    from services.lmintegration import agentic_workflow
    AGENTIC_AVAILABLE = True
except ImportError:
    AGENTIC_AVAILABLE = False
    print("Warning: agentic workflow not available - advanced AI features disabled")

logger = logging.getLogger(__name__)

def create_app():
    """Application factory for Flask"""
    app = Flask(__name__)
    
    # Load configuration (try production config first for Azure deployment)
    try:
        # Try production config first
        if os.environ.get('FLASK_ENV') == 'production':
            app.config.from_object('production_config.Config')
        else:
            app.config.from_object('config.Config')
    except Exception:
        # Fallback configuration if config file has issues
        app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        print("Warning: Could not load config.py, using default settings")
    
    # Setup logging based on environment
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=os.environ.get('LOG_FORMAT', '%(asctime)s %(levelname)s %(name)s %(message)s')
    )
    
    # Add security headers for production
    @app.after_request
    def add_security_headers(response):
        if os.environ.get('FLASK_ENV') == 'production':
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Register routes
    register_travel_routes(app)
    register_ai_routes(app)
    register_health_routes(app)
    
    return app

def register_travel_routes(app):
    """Register travel-related routes"""
    
    @app.route('/api/dining', methods=['GET'])
    def get_dining_options():
        if not DINING_AVAILABLE:
            return jsonify({"error": "Dining service not available"}), 503
            
        budget = request.args.get('budget')
        timeframe = request.args.get('timeframe')
        address = request.args.get('address')  # Changed from 'location' to match dining service

        if not all([budget, timeframe, address]):
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            dining_options = find_dining_options(budget, timeframe, address)
            return jsonify(dining_options)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/flights', methods=['GET'])
    def get_flights():
        if not FLIGHTS_AVAILABLE:
            return jsonify({"flights": [], "errors": ["Flights service not available"]}), 503
            
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        departureDate = request.args.get('departureDate')
        returnDate = request.args.get('returnDate')  # Now REQUIRED

        # All four parameters are now mandatory
        if not all([origin, destination, departureDate, returnDate]):
            missing_params = []
            if not origin: missing_params.append("origin")
            if not destination: missing_params.append("destination")
            if not departureDate: missing_params.append("departureDate")
            if not returnDate: missing_params.append("returnDate")
            
            return jsonify({
                "flights": [], 
                "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
            }), 400

        try:
            result = find_flights_by_criteria(origin, destination, departureDate, returnDate)
            
            # The service now always returns the correct format with flights and errors arrays
            # Check if there are errors that should return a 400 status code
            if result.get("errors") and any("Missing required parameters" in error for error in result["errors"]):
                return jsonify(result), 400
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"flights": [], "errors": [str(e)]}), 500

    @app.route('/api/transportation', methods=['GET'])
    def get_transportation():
        if not TRANSPORTATION_AVAILABLE:
            return jsonify({"transportation": [], "errors": ["Transportation service not available"]}), 503
            
        location = request.args.get('location')
        pickup = request.args.get('pickup')
        dropOff = request.args.get('dropOff')
        pickUpDate = request.args.get('pickUpDate')
        dropOffDate = request.args.get('dropOffDate')
        pickupTime = request.args.get('pickupTime')
        dropOffTime = request.args.get('dropOffTime')

        # All seven parameters are now mandatory
        if not all([location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime]):
            missing_params = []
            if not location: missing_params.append("location")
            if not pickup: missing_params.append("pickup")
            if not dropOff: missing_params.append("dropOff")
            if not pickUpDate: missing_params.append("pickUpDate")
            if not dropOffDate: missing_params.append("dropOffDate")
            if not pickupTime: missing_params.append("pickupTime")
            if not dropOffTime: missing_params.append("dropOffTime")
            
            return jsonify({
                "transportation": [], 
                "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
            }), 400

        try:
            result = find_transportation_options(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime)
            
            # The service now always returns the correct format with transportation and errors arrays
            # Check if there are errors that should return a 400 status code
            if result.get("errors") and any("Missing required parameters" in error for error in result["errors"]):
                return jsonify(result), 400
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"transportation": [], "errors": [str(e)]}), 500

    @app.route('/api/hotels', methods=['GET'])
    def get_hotels():
        if not HOTELS_AVAILABLE:
            return jsonify({"hotels": [], "errors": ["Hotels service not available"]}), 503
            
        country = request.args.get('country')
        state = request.args.get('state')
        city = request.args.get('city')
        arrivalDate = request.args.get('arrivalDate')
        chekoutDate = request.args.get('chekoutDate')

        # All five parameters are now mandatory
        if not all([country, state, city, arrivalDate, chekoutDate]):
            missing_params = []
            if not country: missing_params.append("country")
            if not state: missing_params.append("state")
            if not city: missing_params.append("city")
            if not arrivalDate: missing_params.append("arrivalDate")
            if not chekoutDate: missing_params.append("chekoutDate")
            
            return jsonify({
                "hotels": [], 
                "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
            }), 400

        try:
            result = find_hotels_by_criteria(country, state, city, arrivalDate, chekoutDate)
            
            # The service now always returns the correct format with hotels and errors arrays
            # Check if there are errors that should return a 400 status code
            if result.get("errors") and any("Missing required parameters" in error for error in result["errors"]):
                return jsonify(result), 400
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"hotels": [], "errors": [str(e)]}), 500

    @app.route('/api/aggregate', methods=['POST'])
    def aggregate():
        """Aggregates results from all services based on POSTed parameters."""
        if not AGGREGATION_AVAILABLE:
            return jsonify({"error": "Aggregation service not available"}), 503
            
        try:
            data = request.get_json()

            dining_params = data.get('dining_params', {})
            flight_params = data.get('flight_params', {})
            hotel_params = data.get('hotel_params', {})
            transportation_params = data.get('transportation_params', {})

            aggregated_data = aggregate_results(dining_params, flight_params, hotel_params, transportation_params)
            return jsonify(aggregated_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def register_ai_routes(app):
    """Register AI/LLM related routes"""
    
    @app.route('/api/ai/chat', methods=['POST'])
    def ai_chat():
        """Enhanced chat endpoint with provider selection"""
        if not LLM_AVAILABLE:
            return jsonify({'error': 'LLM service not available. Install required packages.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({'error': 'Invalid request. Missing "message" field.'}), 400

            user_message = data['message']
            provider = data.get('provider')
            system_message = data.get('system_message')
            max_tokens = data.get('max_tokens')
            temperature = data.get('temperature')

            response = llm_service.generate_response(
                prompt=user_message,
                provider_name=provider,
                system_message=system_message,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return jsonify(response)

        except Exception as e:
            logger.error(f"Error in AI chat endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/conversation', methods=['POST'])
    def ai_conversation():
        """Multi-turn conversation endpoint"""
        if not LLM_AVAILABLE:
            return jsonify({'error': 'LLM service not available. Install required packages.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'messages' not in data:
                return jsonify({'error': 'Invalid request. Missing "messages" field.'}), 400

            messages = data['messages']
            provider = data.get('provider')
            max_tokens = data.get('max_tokens')
            temperature = data.get('temperature')

            response = llm_service.chat_completion(
                messages=messages,
                provider_name=provider,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return jsonify(response)

        except Exception as e:
            logger.error(f"Error in AI conversation endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/travel-agent', methods=['POST'])
    def ai_travel_agent():
        """Intelligent travel planning agent"""
        if not (LLM_AVAILABLE and AGENTIC_AVAILABLE):
            return jsonify({'error': 'AI travel agent not available. Missing required services.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({'error': 'Invalid request. Missing "query" field.'}), 400

            user_query = data['query']
            travel_data = {}
            
            # Get travel data by calling existing endpoints if needed and available
            if any(word in user_query.lower() for word in ['flight', 'fly', 'airline']) and FLIGHTS_AVAILABLE:
                flight_params = data.get('flight_params', {})
                if flight_params:
                    try:
                        travel_data['flights'] = find_flights_by_criteria(**flight_params)
                    except Exception as e:
                        logger.warning(f"Could not fetch flight data: {e}")
            
            if any(word in user_query.lower() for word in ['hotel', 'stay', 'accommodation']) and HOTELS_AVAILABLE:
                hotel_params = data.get('hotel_params', {})
                if hotel_params:
                    try:
                        travel_data['hotels'] = find_hotels_by_criteria(**hotel_params)
                    except Exception as e:
                        logger.warning(f"Could not fetch hotel data: {e}")
            
            if any(word in user_query.lower() for word in ['restaurant', 'food', 'dining', 'eat']) and DINING_AVAILABLE:
                dining_params = data.get('dining_params', {})
                if dining_params:
                    try:
                        travel_data['dining'] = find_dining_options(**dining_params)
                    except Exception as e:
                        logger.warning(f"Could not fetch dining data: {e}")
            
            if any(word in user_query.lower() for word in ['transport', 'bus', 'train', 'car']) and TRANSPORTATION_AVAILABLE:
                transport_params = data.get('transportation_params', {})
                if transport_params:
                    try:
                        travel_data['transportation'] = find_transportation_options(**transport_params)
                    except Exception as e:
                        logger.warning(f"Could not fetch transportation data: {e}")
            
            result = agentic_workflow.travel_planning_agent(user_query, travel_data)
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error in travel agent endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/rag/ingest', methods=['POST'])
    def ai_rag_ingest():
        """Document ingestion for RAG"""
        if not RAG_AVAILABLE:
            return jsonify({'error': 'RAG service not available. Install required packages.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'file_path' not in data:
                return jsonify({'error': 'Invalid request. Missing "file_path" field.'}), 400

            file_path = data['file_path']
            result = rag_service.ingest_document(file_path)
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error in RAG ingestion endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/rag/query', methods=['POST'])
    def ai_rag_query():
        """RAG-powered question answering"""
        if not (RAG_AVAILABLE and AGENTIC_AVAILABLE):
            return jsonify({'error': 'RAG query not available. Missing required services.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'question' not in data:
                return jsonify({'error': 'Invalid request. Missing "question" field.'}), 400

            question = data['question']
            top_k = data.get('top_k')
            provider = data.get('provider')
            
            result = agentic_workflow.document_qa_agent(
                question=question,
                top_k=top_k,
                provider=provider
            )
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error in RAG query endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/rag/delete', methods=['DELETE'])
    def ai_rag_delete():
        """Delete document from RAG system"""
        if not RAG_AVAILABLE:
            return jsonify({'error': 'RAG service not available. Install required packages.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'document_hash' not in data:
                return jsonify({'error': 'Invalid request. Missing "document_hash" field.'}), 400

            document_hash = data['document_hash']
            result = rag_service.delete_document(document_hash)
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error in RAG delete endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/consensus', methods=['POST'])
    def ai_consensus():
        """Multi-provider consensus endpoint"""
        if not (LLM_AVAILABLE and AGENTIC_AVAILABLE):
            return jsonify({'error': 'Consensus service not available. Missing required services.'}), 503
            
        try:
            data = request.get_json()
            if not data or 'prompt' not in data:
                return jsonify({'error': 'Invalid request. Missing "prompt" field.'}), 400

            prompt = data['prompt']
            providers = data.get('providers', ['local_llm', 'openai', 'anthropic', 'google'])
            
            result = agentic_workflow.multi_provider_consensus(prompt, providers)
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error in consensus endpoint: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ai/providers', methods=['GET'])
    def ai_providers():
        """List available LLM providers"""
        if not LLM_AVAILABLE:
            return jsonify({'error': 'LLM service not available. Install required packages.'}), 503
            
        try:
            providers = llm_service.list_providers()
            return jsonify({
                "available_providers": providers,
                "total_count": len(providers)
            })
        except Exception as e:
            logger.error(f"Error listing providers: {e}")
            return jsonify({'error': str(e)}), 500

def register_health_routes(app):
    """Register health check and status routes"""
    
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint"""
        return jsonify({
            "message": "Agentic RAG API",
            "status": "running",
            "endpoints": {
                "health": "/api/health",
                "ai_health": "/api/ai/health",
                "providers": "/api/ai/providers"
            }
        })

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """General health check"""
        from datetime import datetime
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "flights": FLIGHTS_AVAILABLE,
                "hotels": HOTELS_AVAILABLE,
                "dining": DINING_AVAILABLE,
                "transportation": TRANSPORTATION_AVAILABLE,
                "aggregation": AGGREGATION_AVAILABLE,
                "llm": LLM_AVAILABLE,
                "rag": RAG_AVAILABLE,
                "agentic": AGENTIC_AVAILABLE
            }
        })

    @app.route('/api/ai/health', methods=['GET'])
    def ai_health():
        """AI service health check"""
        try:
            from datetime import datetime
            
            if LLM_AVAILABLE:
                providers = llm_service.list_providers()
                provider_count = len(providers)
                provider_list = providers
            else:
                provider_count = 0
                provider_list = []
                
            return jsonify({
                "status": "healthy" if LLM_AVAILABLE else "limited",
                "available_providers": provider_count,
                "providers": provider_list,
                "rag_enabled": RAG_AVAILABLE,
                "agentic_enabled": AGENTIC_AVAILABLE,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error in AI health check: {e}")
            return jsonify({
                "status": "unhealthy", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500

# Create the Flask app instance
app = create_app()
# Entry point to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
