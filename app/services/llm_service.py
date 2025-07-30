"""
Multi-LLM Service for Agentic RAG API
Supports OpenAI, Anthropic, Google Gemini, and Azure OpenAI
"""

import logging
from typing import Dict, List, Optional, Union, Any

logger = logging.getLogger(__name__)

# Graceful imports with fallbacks
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError as ie:
    OPENAI_AVAILABLE = False
    logger.error(f"OpenAI package import error: {ie}")
    print("Warning: OpenAI package not available")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError as ie:
    ANTHROPIC_AVAILABLE = False
    logger.error(f"Anthropic package import error: {ie}")
    print("Warning: Anthropic package not available")

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError as ie:
    GOOGLE_AVAILABLE = False
    logger.error(f"Google Generative AI package import error: {ie}")
    print("Warning: Google Generative AI package not available")

try:
    from config import Config
except ImportError:
    # Fallback config if import fails
    class Config:
        OPENAI_API_KEY = None
        ANTHROPIC_API_KEY = None
        GOOGLE_API_KEY = None
        AZURE_OPENAI_ENDPOINT = None
        AZURE_OPENAI_API_KEY = None
        AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
        DEFAULT_LLM_PROVIDER = "openai"
        MAX_TOKENS = 2000
        TEMPERATURE = 0.7
    print("Warning: Could not import config, using fallback settings")


class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, provider_name: str, model: str, **kwargs):
        self.provider_name = provider_name
        self.model = model
        self.config = kwargs
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        raise NotImplementedError
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider"""
    
    def __init__(self, model: str = "GPT-4.1", **kwargs):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed. Install with: pip install openai")
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in configuration")
            
        super().__init__("openai", model, **kwargs)
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE)
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

class AnthropicProvider(LLMProvider):
    """Anthropic Claude LLM Provider"""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package is not installed. Install with: pip install anthropic")
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in configuration")
            
        super().__init__("anthropic", model, **kwargs)
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE),
                system=system_message or "You are a helpful assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Convert messages format for Anthropic
        system_message = None
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE),
                system=system_message or "You are a helpful assistant.",
                messages=user_messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

class GoogleProvider(LLMProvider):
    """Google Gemini LLM Provider"""
    
    def __init__(self, model: str = "gemini-pro", **kwargs):
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google Generative AI package is not installed. Install with: pip install google-generativeai")
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in configuration")
            
        super().__init__("google", model, **kwargs)
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model_instance = genai.GenerativeModel(model)
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        try:
            full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt
            response = self.model_instance.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                    temperature=kwargs.get('temperature', Config.TEMPERATURE)
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Google API error: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Convert messages to single prompt for Gemini
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        full_prompt = "\n\n".join(prompt_parts)
        return self.generate(full_prompt, **kwargs)

class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI LLM Provider"""
    
    def __init__(self, model: str = "gpt-35-turbo", **kwargs):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed. Install with: pip install openai")
        
        # Validate required Azure OpenAI configuration
        if not all([Config.AZURE_OPENAI_ENDPOINT, Config.AZURE_OPENAI_API_KEY]):
            raise ValueError("Azure OpenAI requires both AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY")
        
        super().__init__("azure_openai", model, **kwargs)
        
        # Initialize Azure OpenAI client using the standard openai package
        self.client = openai.AzureOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION
        )
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,  # This should be the deployment name in Azure
                messages=messages,
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS),
                temperature=kwargs.get('temperature', Config.TEMPERATURE)
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Azure OpenAI API error: {e}")
            raise

class LLMService:
    """Main LLM Service that manages multiple providers"""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available LLM providers based on configuration"""
        # OpenAI Provider
        if OPENAI_AVAILABLE and hasattr(Config, 'OPENAI_API_KEY') and Config.OPENAI_API_KEY:
            try:
                self.providers['openai'] = OpenAIProvider()
                self.providers['openai_gpt4'] = OpenAIProvider(model="gpt-4")
                logger.info("OpenAI providers initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI provider: {e}")
        
        # Anthropic Provider
        if ANTHROPIC_AVAILABLE and hasattr(Config, 'ANTHROPIC_API_KEY') and Config.ANTHROPIC_API_KEY:
            try:
                self.providers['anthropic'] = AnthropicProvider()
                self.providers['claude_opus'] = AnthropicProvider(model="claude-3-opus-20240229")
                logger.info("Anthropic providers initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic provider: {e}")
        
        # Google Provider
        if GOOGLE_AVAILABLE and hasattr(Config, 'GOOGLE_API_KEY') and Config.GOOGLE_API_KEY:
            try:
                self.providers['google'] = GoogleProvider()
                self.providers['gemini_pro'] = GoogleProvider(model="gemini-pro")
                logger.info("Google providers initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Google provider: {e}")
        
        # Azure OpenAI Provider
        if (OPENAI_AVAILABLE and 
            hasattr(Config, 'AZURE_OPENAI_API_KEY') and Config.AZURE_OPENAI_API_KEY and
            hasattr(Config, 'AZURE_OPENAI_ENDPOINT') and Config.AZURE_OPENAI_ENDPOINT):
            try:
                self.providers['azure_openai'] = AzureOpenAIProvider()
                logger.info("Azure OpenAI provider initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Azure OpenAI provider: {e}")
        
        if not self.providers:
            logger.warning("No LLM providers could be initialized. Check your API keys and package installations.")
            # Don't raise an error - let the app start but warn users
    
    def get_provider(self, provider_name: str = None) -> LLMProvider:
        """Get a specific provider or the default one"""
        if provider_name is None:
            provider_name = Config.DEFAULT_LLM_PROVIDER
        
        if provider_name not in self.providers:
            available = list(self.providers.keys())
            raise ValueError(f"Provider '{provider_name}' not available. Available providers: {available}")
        
        return self.providers[provider_name]
    
    def generate_response(self, prompt: str, provider_name: str = None, system_message: str = None, **kwargs) -> Dict[str, Any]:
        """Generate a response using the specified provider"""
        provider = self.get_provider(provider_name)
        
        try:
            response = provider.generate(prompt, system_message, **kwargs)
            return {
                "success": True,
                "response": response,
                "provider": provider.provider_name,
                "model": provider.model
            }
        except Exception as e:
            logger.error(f"Error generating response with {provider.provider_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider.provider_name,
                "model": provider.model
            }
    
    def chat_completion(self, messages: List[Dict[str, str]], provider_name: str = None, **kwargs) -> Dict[str, Any]:
        """Chat completion using the specified provider"""
        provider = self.get_provider(provider_name)
        
        try:
            response = provider.chat(messages, **kwargs)
            return {
                "success": True,
                "response": response,
                "provider": provider.provider_name,
                "model": provider.model
            }
        except Exception as e:
            logger.error(f"Error in chat completion with {provider.provider_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider.provider_name,
                "model": provider.model
            }
    
    def list_providers(self) -> List[str]:
        """List all available providers"""
        return list(self.providers.keys())

# Initialize the global LLM service
llm_service = LLMService()
