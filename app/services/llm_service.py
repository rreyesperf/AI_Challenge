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
    import requests
    REQUESTS_AVAILABLE = True
except ImportError as ie:
    REQUESTS_AVAILABLE = False
    logger.error(f"Requests package import error: {ie}")
    print("Warning: Requests package not available - local LLM services disabled")

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
        # Local LLM Configuration
        OLLAMA_BASE_URL = "http://localhost:11434"
        LOCAL_LLM_BASE_URL = "http://localhost:8000"
        LOCAL_LLM_API_KEY = None
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
    
    def __init__(self, model: str = "gpt-3.5-turbo", **kwargs):
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

class OllamaProvider(LLMProvider):
    """Ollama Local LLM Provider"""
    
    def __init__(self, model: str = "llama2", base_url: str = None, **kwargs):
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests package is not installed. Install with: pip install requests")
        
        super().__init__("ollama", model, **kwargs)
        self.base_url = base_url or getattr(Config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        
        # Test connection to Ollama
        self._test_connection()
    
    def _test_connection(self):
        """Test if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info(f"Ollama connection successful at {self.base_url}")
            else:
                logger.warning(f"Ollama responded with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not connect to Ollama at {self.base_url}: {e}")
            # Don't raise here - allow the provider to be created but warn
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get('temperature', Config.TEMPERATURE),
                    "num_predict": kwargs.get('max_tokens', Config.MAX_TOKENS)
                }
            }
            
            if system_message:
                payload["system"] = system_message
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # Longer timeout for local generation
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get('temperature', Config.TEMPERATURE),
                    "num_predict": kwargs.get('max_tokens', Config.MAX_TOKENS)
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("message", {}).get("content", "")
            
        except Exception as e:
            logger.error(f"Ollama chat API error: {e}")
            raise

class LocalLLMProvider(LLMProvider):
    """Generic Local LLM Provider for OpenAI-compatible APIs"""
    
    def __init__(self, model: str = "local-model", base_url: str = None, api_key: str = None, **kwargs):
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests package is not installed. Install with: pip install requests")
        
        super().__init__("local_llm", model, **kwargs)
        self.base_url = base_url or getattr(Config, 'LOCAL_LLM_BASE_URL', 'http://localhost:8000')
        self.api_key = api_key or getattr(Config, 'LOCAL_LLM_API_KEY', None)
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test if local LLM server is running"""
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(f"{self.base_url}/v1/models", headers=headers, timeout=5)
            if response.status_code == 200:
                logger.info(f"Local LLM connection successful at {self.base_url}")
            else:
                logger.warning(f"Local LLM responded with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not connect to local LLM at {self.base_url}: {e}")
    
    def generate(self, prompt: str, system_message: str = None, **kwargs) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": kwargs.get('max_tokens', Config.MAX_TOKENS),
                "temperature": kwargs.get('temperature', Config.TEMPERATURE),
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Local LLM API error: {e}")
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
        
        # Ollama Provider
        if REQUESTS_AVAILABLE:
            try:
                # Dynamically discover available Ollama models
                available_models = []
                try:
                    ollama_url = getattr(Config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
                    response = requests.get(f"{ollama_url}/api/tags", timeout=5)
                    if response.status_code == 200:
                        models_data = response.json()
                        # Keep the full model name including version tag (e.g., 'llama3:8b')
                        available_models = [model.get('name', '') for model in models_data.get('models', [])]
                        available_models = [m for m in available_models if m]  # Filter out empty names
                        logger.info(f"Discovered Ollama models: {available_models}")
                except Exception as e:
                    logger.warning(f"Could not discover Ollama models: {e}")
                
                # If no models discovered, try common ones as fallback
                if not available_models:
                    available_models = ['llama2', 'llama3', 'codellama', 'mistral', 'neural-chat']
                    logger.info("Using fallback model list for Ollama")
                
                # Try to initialize providers for available models
                for model in available_models:
                    try:
                        provider = OllamaProvider(model=model)
                        self.providers[f'ollama_{model}'] = provider
                        logger.info(f"Ollama provider initialized successfully for model: {model}")
                        
                        # Use the first successfully initialized model as the default 'ollama' provider
                        if 'ollama' not in self.providers:
                            self.providers['ollama'] = provider
                        
                        break  # Stop after first successful initialization
                    except Exception as e:
                        logger.debug(f"Failed to initialize Ollama provider for {model}: {e}")
                        continue
                
                if not any(key.startswith('ollama') for key in self.providers.keys()):
                    logger.warning("No Ollama providers could be initialized")
                
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama provider: {e}")
        
        # Local LLM Provider (OpenAI-compatible)
        if REQUESTS_AVAILABLE and hasattr(Config, 'LOCAL_LLM_BASE_URL'):
            try:
                self.providers['local_llm'] = LocalLLMProvider()
                logger.info("Local LLM provider initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Local LLM provider: {e}")
        
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
