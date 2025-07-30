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
                provider_name="openai_gpt4",  # Use more capable model for complex analysis
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
        providers = providers or ["openai", "anthropic", "google"]
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
        # Set defaults from config if available
        if hasattr(Config, 'DEFAULT_LLM_PROVIDER'):
            provider = provider or Config.DEFAULT_LLM_PROVIDER
        if hasattr(Config, 'MAX_TOKENS'):
            max_tokens = max_tokens or Config.MAX_TOKENS
        if hasattr(Config, 'TEMPERATURE'):
            temperature = temperature or Config.TEMPERATURE
            
        response = llm_service.generate_response(
            prompt=message,
            provider_name=provider,
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
        # Set defaults from config if available
        if hasattr(Config, 'DEFAULT_LLM_PROVIDER'):
            provider = provider or Config.DEFAULT_LLM_PROVIDER
        if hasattr(Config, 'MAX_TOKENS'):
            max_tokens = max_tokens or Config.MAX_TOKENS
        if hasattr(Config, 'TEMPERATURE'):
            temperature = temperature or Config.TEMPERATURE
            
        response = llm_service.chat_completion(
            messages=messages,
            provider_name=provider,
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
        providers = providers or ['openai', 'anthropic', 'google']
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
        default_provider = getattr(Config, 'DEFAULT_LLM_PROVIDER', 'openai')
        return {
            "available_providers": providers,
            "default_provider": default_provider
        }
    except Exception as e:
        logger.error(f"Error listing providers: {e}")
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