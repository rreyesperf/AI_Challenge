"""
Advanced Agentic LLM Integration Service
Supports multiple LLM providers and agentic workflows
"""

import logging
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

try:
    from services.llm_service import llm_service
    LLM_SERVICE_AVAILABLE = True
except ImportError:
    LLM_SERVICE_AVAILABLE = False
    print("Warning: LLM service not available")
    llm_service = None

try:
    from services.rag_service import rag_service
    RAG_SERVICE_AVAILABLE = True
except ImportError:
    RAG_SERVICE_AVAILABLE = False
    print("Warning: RAG service not available")
    rag_service = None

try:
    from config import Config
except ImportError:
    class Config:
        pass
    print("Warning: Could not import config")

logger = logging.getLogger(__name__)

class AgenticWorkflow:
    """Handles agentic workflows with multiple LLM calls"""
    
    def __init__(self):
        self.llm_service = llm_service
        self.rag_service = rag_service
    
    def travel_planning_agent(self, user_query: str, travel_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Travel planning agent that can analyze and recommend travel options"""
        
        # Step 1: Analyze user intent
        intent_analysis_prompt = f"""
        Analyze the following travel query and extract key information:
        
        Query: "{user_query}"
        
        Please identify:
        1. Travel type (business, leisure, family, etc.)
        2. Budget range (if mentioned)
        3. Dates or timeframe
        4. Destination preferences
        5. Special requirements
        6. Priority factors (cost, comfort, time, etc.)
        
        Respond in JSON format with these categories.
        """
        
        intent_response = self.llm_service.generate_response(
            prompt=intent_analysis_prompt,
            system_message="You are a travel planning expert. Analyze queries and extract structured information."
        )
        
        # Step 2: If travel data is available, analyze it
        analysis_results = {}
        if travel_data:
            analysis_prompt = f"""
            Based on the user's travel requirements and the following available options, 
            provide a detailed analysis and recommendations:
            
            User Query: {user_query}
            
            Available Options:
            {json.dumps(travel_data, indent=2)}
            
            Please provide:
            1. Top 3 recommendations with reasons
            2. Pros and cons of each option
            3. Cost-benefit analysis
            4. Alternative suggestions
            """
            
            analysis_response = self.llm_service.generate_response(
                prompt=analysis_prompt,
                provider_name=None,  # Use default provider with proper fallback logic
                system_message="You are a travel advisor. Provide detailed, practical recommendations."
            )
            
            analysis_results = {
                "recommendations": analysis_response.get("response"),
                "provider_used": analysis_response.get("provider")
            }
        
        return {
            "user_query": user_query,
            "intent_analysis": intent_response.get("response") if intent_response.get("success") else "Failed to analyze intent",
            "travel_analysis": analysis_results,
            "timestamp": datetime.now().isoformat()
        }
    
    def document_qa_agent(self, question: str, **kwargs) -> Dict[str, Any]:
        """Document Q&A agent using RAG"""
        return self.rag_service.query(question, **kwargs)
    
    def multi_provider_consensus(self, prompt: str, providers: List[str] = None) -> Dict[str, Any]:
        """Get responses from multiple providers for consensus"""
        providers = providers or ["ollama", "openai", "anthropic", "google"]
        available_providers = self.llm_service.list_providers()
        
        # Filter to only available providers
        providers = [p for p in providers if p in available_providers]
        
        if not providers:
            return {
                "success": False,
                "error": "No specified providers are available"
            }
        
        responses = {}
        for provider in providers:
            response = self.llm_service.generate_response(
                prompt=prompt,
                provider_name=provider
            )
            responses[provider] = response
        
        # Generate consensus analysis
        consensus_prompt = f"""
        Multiple AI models were asked the same question and provided different responses.
        Please analyze these responses and provide a consensus answer that incorporates
        the best aspects of each response.
        
        Question: {prompt}
        
        Responses:
        {json.dumps({k: v.get('response', 'Error') for k, v in responses.items()}, indent=2)}
        
        Please provide a balanced, comprehensive answer that considers all perspectives.
        """
        
        consensus_response = self.llm_service.generate_response(
            prompt=consensus_prompt,
            system_message="You are an expert at synthesizing multiple perspectives into coherent insights."
        )
        
        return {
            "success": True,
            "question": prompt,
            "individual_responses": responses,
            "consensus": consensus_response.get("response"),
            "providers_used": providers
        }

# Initialize the agentic workflow
agentic_workflow = AgenticWorkflow()

# Service functions for use in routes.py
def get_agentic_workflow():
    """Get the agentic workflow instance"""
    return agentic_workflow

def chat_service(message: str, provider: str = None, system_message: str = None, 
                max_tokens: int = None, temperature: float = None) -> Dict[str, Any]:
    """Basic chat service function"""
    if not LLM_SERVICE_AVAILABLE:
        return {'error': 'LLM service not available'}
    
    try:
        # Set defaults from config if available (only if no provider specified)
        if hasattr(Config, 'MAX_TOKENS'):
            max_tokens = max_tokens or Config.MAX_TOKENS
        if hasattr(Config, 'TEMPERATURE'):
            temperature = temperature or Config.TEMPERATURE
            
        # IMPORTANT: Let LLM service handle provider priority automatically
        # Do NOT use Config.DEFAULT_LLM_PROVIDER as it bypasses the priority system
        response = llm_service.generate_response(
            prompt=message,
            provider_name=provider,  # This will be None to use priority fallback
            system_message=system_message,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response
    except Exception as e:
        logger.error(f"Error in chat service: {e}")
        return {'error': str(e)}

def chat_conversation_service(messages: List[Dict], provider: str = None, 
                             max_tokens: int = None, temperature: float = None) -> Dict[str, Any]:
    """Multi-turn conversation service function"""
    if not LLM_SERVICE_AVAILABLE:
        return {'error': 'LLM service not available'}
    
    try:
        # Set defaults from config if available (only for non-provider settings)
        if hasattr(Config, 'MAX_TOKENS'):
            max_tokens = max_tokens or Config.MAX_TOKENS
        if hasattr(Config, 'TEMPERATURE'):
            temperature = temperature or Config.TEMPERATURE
            
        # IMPORTANT: Let LLM service handle provider priority automatically
        # Do NOT use Config.DEFAULT_LLM_PROVIDER as it bypasses the priority system
        response = llm_service.chat_completion(
            messages=messages,
            provider_name=provider,  # This will be None to use priority fallback
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response
    except Exception as e:
        logger.error(f"Error in conversation service: {e}")
        return {'error': str(e)}

def travel_planning_service(query: str, travel_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Travel planning service function"""
    try:
        result = agentic_workflow.travel_planning_agent(query, travel_data)
        return result
    except Exception as e:
        logger.error(f"Error in travel planning service: {e}")
        return {'error': str(e)}

def ingest_document_service(file_path: str) -> Dict[str, Any]:
    """Document ingestion service function"""
    if not RAG_SERVICE_AVAILABLE:
        return {'error': 'RAG service not available'}
    
    try:
        result = rag_service.ingest_document(file_path)
        return result
    except Exception as e:
        logger.error(f"Error in document ingestion service: {e}")
        return {'error': str(e)}

def rag_query_service(question: str, top_k: int = None, provider: str = None) -> Dict[str, Any]:
    """RAG query service function"""
    try:
        # Set defaults from config if available
        if hasattr(Config, 'TOP_K_RESULTS'):
            top_k = top_k or Config.TOP_K_RESULTS
        if hasattr(Config, 'DEFAULT_LLM_PROVIDER'):
            provider = provider or Config.DEFAULT_LLM_PROVIDER
            
        result = agentic_workflow.document_qa_agent(
            question=question,
            top_k=top_k,
            provider=provider
        )
        return result
    except Exception as e:
        logger.error(f"Error in RAG query service: {e}")
        return {'error': str(e)}

def delete_document_service(document_hash: str) -> Dict[str, Any]:
    """Delete document service function"""
    if not RAG_SERVICE_AVAILABLE:
        return {'error': 'RAG service not available'}
    
    try:
        result = rag_service.delete_document(document_hash)
        return result
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return {'error': str(e)}

def multi_provider_consensus_service(prompt: str, providers: List[str] = None) -> Dict[str, Any]:
    """Multi-provider consensus service function"""
    try:
        providers = providers or ['ollama', 'openai', 'anthropic', 'google']
        result = agentic_workflow.multi_provider_consensus(prompt, providers)
        return result
    except Exception as e:
        logger.error(f"Error in consensus service: {e}")
        return {'error': str(e)}

def list_providers_service() -> Dict[str, Any]:
    """List available LLM providers service function"""
    if not LLM_SERVICE_AVAILABLE:
        return {'error': 'LLM service not available'}
    
    try:
        providers = llm_service.list_providers()
        default_provider = getattr(Config, 'DEFAULT_LLM_PROVIDER', 'ollama')
        return {
            "available_providers": providers,
            "default_provider": default_provider
        }
    except Exception as e:
        logger.error(f"Error listing providers: {e}")
        return {'error': str(e)}

# Internal service functions for travel data (converted from routes)
def internal_dining_service(params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal dining service function"""
    try:
        from services.dining import find_dining_options
        result = find_dining_options(**params)
        return result
    except Exception as e:
        logger.error(f"Error in dining service: {e}")
        return {"error": str(e)}

def internal_flights_service(params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal flights service function"""
    try:
        from services.flights import find_flights_by_criteria
        result = find_flights_by_criteria(**params)
        return result
    except Exception as e:
        logger.error(f"Error in flights service: {e}")
        return {"flights": [], "errors": [str(e)]}

def internal_hotels_service(params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal hotels service function"""
    try:
        from services.hotels import find_hotels_by_criteria
        result = find_hotels_by_criteria(**params)
        return result
    except Exception as e:
        logger.error(f"Error in hotels service: {e}")
        return {"hotels": [], "errors": [str(e)]}

def internal_transportation_service(params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal transportation service function"""
    try:
        from services.transportation import find_transportation_options
        result = find_transportation_options(**params)
        return result
    except Exception as e:
        logger.error(f"Error in transportation service: {e}")
        return {"transportation": [], "errors": [str(e)]}

def internal_aggregation_service(dining_params: Dict = None, flight_params: Dict = None, 
                                hotel_params: Dict = None, transportation_params: Dict = None) -> Dict[str, Any]:
    """Internal aggregation service function"""
    try:
        from services.aggregation import aggregate_results
        result = aggregate_results(
            dining_params or {}, 
            flight_params or {}, 
            hotel_params or {}, 
            transportation_params or {}
        )
        return result
    except Exception as e:
        logger.error(f"Error in aggregation service: {e}")
        return {'error': str(e)}

# Enhanced Conversational Travel Assistant
class TravelConversationManager:
    """Manages multi-turn travel planning conversations"""
    
    def __init__(self):
        self.llm_service = llm_service
        self.required_params = {
            'flights': ['origin', 'destination', 'departureDate', 'returnDate'],
            'hotels': ['country', 'state', 'city', 'arrivalDate', 'chekoutDate'],
            'dining': ['location'],
            'transportation': ['location', 'pickup', 'dropOff', 'pickUpDate', 'dropOffDate', 'pickupTime', 'dropOffTime']
        }
    
    def detect_travel_intent(self, message: str) -> Dict[str, Any]:
        """Detect if the message has travel-related intent"""
        intent_prompt = f"""
        Analyze the following message to determine if it's travel-related and what specific travel services might be needed.
        
        Message: "{message}"
        
        Please respond in JSON format with:
        {{
            "is_travel_related": true/false,
            "services_needed": ["flights", "hotels", "dining", "transportation"],
            "confidence": 0.0-1.0,
            "extracted_info": {{
                "destination": "location if mentioned",
                "dates": "dates if mentioned",
                "travelers": "number if mentioned",
                "budget": "budget if mentioned",
                "preferences": "any preferences mentioned"
            }}
        }}
        """
        
        response = self.llm_service.generate_response(
            prompt=intent_prompt,
            system_message="You are a travel intent detection expert. Analyze messages and respond with precise JSON."
        )
        
        try:
            # Try to parse JSON response
            import json
            intent_data = json.loads(response.get('response', '{}'))
            return intent_data
        except:
            # Fallback to keyword-based detection
            travel_keywords = ['travel', 'trip', 'vacation', 'flight', 'hotel', 'restaurant', 'transport', 'book', 'plan']
            is_travel = any(keyword in message.lower() for keyword in travel_keywords)
            return {
                "is_travel_related": is_travel,
                "services_needed": [],
                "confidence": 0.5 if is_travel else 0.1,
                "extracted_info": {}
            }
    
    def collect_travel_parameters(self, intent_data: Dict, user_message: str) -> Dict[str, Any]:
        """Intelligently collect missing travel parameters through conversation"""
        services_needed = intent_data.get('services_needed', [])
        extracted_info = intent_data.get('extracted_info', {})
        
        # Determine what information is missing
        missing_info = []
        collection_prompt_parts = []
        
        if 'flights' in services_needed:
            if not extracted_info.get('origin'):
                missing_info.append('departure location')
            if not extracted_info.get('destination'):
                missing_info.append('destination')
            if not extracted_info.get('dates'):
                missing_info.append('travel dates')
        
        if 'hotels' in services_needed:
            if not extracted_info.get('destination'):
                missing_info.append('destination city')
            if not extracted_info.get('dates'):
                missing_info.append('check-in and check-out dates')
        
        if 'dining' in services_needed:
            if not extracted_info.get('destination'):
                missing_info.append('dining location')
        
        if 'transportation' in services_needed:
            if not extracted_info.get('destination'):
                missing_info.append('transportation location and details')
        
        if missing_info:
            # Ask for missing information naturally
            info_request_prompt = f"""
            The user wants help with travel planning. Based on their message: "{user_message}"
            
            They seem to need help with: {', '.join(services_needed)}
            
            Missing information needed: {', '.join(missing_info)}
            
            Create a friendly, conversational response that:
            1. Acknowledges their travel request
            2. Asks for the missing information in a natural way
            3. Provides examples or suggestions to help them
            4. Keeps it concise but helpful
            
            Don't ask for all missing information at once - prioritize the most important 2-3 items.
            """
            
            response = self.llm_service.generate_response(
                prompt=info_request_prompt,
                system_message="You are a helpful travel assistant. Be conversational, friendly, and efficient."
            )
            
            return {
                "needs_more_info": True,
                "response": response.get('response'),
                "missing_info": missing_info,
                "services_needed": services_needed
            }
        
        return {
            "needs_more_info": False,
            "ready_for_search": True,
            "services_needed": services_needed,
            "extracted_info": extracted_info
        }
    
    def execute_travel_search(self, services_needed: List[str], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute travel searches and aggregate results"""
        results = {}
        
        try:
            # Prepare parameters for each service
            if 'dining' in services_needed:
                dining_params = {'location': parameters.get('destination', parameters.get('location', ''))}
                results['dining'] = internal_dining_service(dining_params)
            
            if 'flights' in services_needed:
                flight_params = {
                    'origin': parameters.get('origin', ''),
                    'destination': parameters.get('destination', ''),
                    'departureDate': parameters.get('departure_date', ''),
                    'returnDate': parameters.get('return_date', '')
                }
                results['flights'] = internal_flights_service(flight_params)
            
            if 'hotels' in services_needed:
                hotel_params = {
                    'city': parameters.get('destination', ''),
                    'country': parameters.get('country', 'USA'),
                    'state': parameters.get('state', ''),
                    'arrivalDate': parameters.get('arrival_date', ''),
                    'chekoutDate': parameters.get('checkout_date', '')
                }
                results['hotels'] = internal_hotels_service(hotel_params)
            
            if 'transportation' in services_needed:
                transport_params = {
                    'location': parameters.get('destination', ''),
                    'pickup': parameters.get('pickup', ''),
                    'dropOff': parameters.get('dropoff', ''),
                    'pickUpDate': parameters.get('pickup_date', ''),
                    'dropOffDate': parameters.get('dropoff_date', ''),
                    'pickupTime': parameters.get('pickup_time', ''),
                    'dropOffTime': parameters.get('dropoff_time', '')
                }
                results['transportation'] = internal_transportation_service(transport_params)
            
            # Aggregate results
            aggregated = internal_aggregation_service(
                dining_params=results.get('dining'),
                flight_params=results.get('flights'),
                hotel_params=results.get('hotels'),
                transportation_params=results.get('transportation')
            )
            
            return {
                "success": True,
                "results": aggregated,
                "services_searched": services_needed
            }
            
        except Exception as e:
            logger.error(f"Error executing travel search: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def format_travel_results(self, search_results: Dict[str, Any], user_query: str) -> str:
        """Format travel search results into readable text"""
        if not search_results.get('success'):
            return f"I apologize, but I encountered an error while searching for travel options: {search_results.get('error', 'Unknown error')}"
        
        results = search_results.get('results', {})
        
        format_prompt = f"""
        Format the following travel search results into a helpful, readable response for the user.
        
        User's original request: "{user_query}"
        
        Search Results:
        {json.dumps(results, indent=2)}
        
        Please create a response that:
        1. Acknowledges their request
        2. Summarizes the key findings
        3. Highlights the best options with reasons
        4. Presents information in a clear, organized way
        5. Includes practical details (prices, times, locations)
        6. Offers helpful suggestions or next steps
        
        Make it conversational and helpful, not just a data dump.
        """
        
        response = self.llm_service.generate_response(
            prompt=format_prompt,
            system_message="You are a travel advisor. Present search results in a clear, helpful, and engaging way."
        )
        
        return response.get('response', 'Here are your travel search results.')

# Initialize travel conversation manager
travel_conversation_manager = TravelConversationManager()

def enhanced_chat_service(message: str, conversation_history: List[Dict] = None, **kwargs) -> Dict[str, Any]:
    """Enhanced chat service with travel conversation capabilities"""
    if not LLM_SERVICE_AVAILABLE:
        return {'error': 'LLM service not available'}
    
    try:
        # Detect travel intent
        intent_data = travel_conversation_manager.detect_travel_intent(message)
        
        if intent_data.get('is_travel_related', False) and intent_data.get('confidence', 0) > 0.6:
            # Handle travel conversation
            collection_result = travel_conversation_manager.collect_travel_parameters(intent_data, message)
            
            if collection_result.get('needs_more_info'):
                # Need more information from user
                return {
                    "success": True,
                    "response": collection_result.get('response'),
                    "conversation_type": "travel_planning",
                    "status": "collecting_info",
                    "provider": "travel_assistant"
                }
            
            elif collection_result.get('ready_for_search'):
                # Execute travel search
                search_results = travel_conversation_manager.execute_travel_search(
                    collection_result.get('services_needed', []),
                    intent_data.get('extracted_info', {})
                )
                
                # Format results
                formatted_response = travel_conversation_manager.format_travel_results(search_results, message)
                
                return {
                    "success": True,
                    "response": formatted_response,
                    "conversation_type": "travel_planning",
                    "status": "search_completed",
                    "provider": "travel_assistant",
                    "search_results": search_results
                }
        
        # Regular chat - not travel related
        return chat_service(message, **kwargs)
        
    except Exception as e:
        logger.error(f"Error in enhanced chat service: {e}")
        return {'error': str(e)}

def health_check_service() -> Dict[str, Any]:
    """Health check service function"""
    try:
        if LLM_SERVICE_AVAILABLE:
            providers = llm_service.list_providers()
            return {
                "status": "healthy",
                "available_providers": len(providers),
                "providers": providers,
                "llm_service_available": True,
                "rag_service_available": RAG_SERVICE_AVAILABLE,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "partial",
                "llm_service_available": False,
                "rag_service_available": RAG_SERVICE_AVAILABLE,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "llm_service_available": LLM_SERVICE_AVAILABLE,
            "rag_service_available": RAG_SERVICE_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }