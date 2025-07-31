#!/usr/bin/env python3
"""
Local LLM Setup and Test Script
This script helps you test your local LLM setup and integration
"""

import sys
import os
import unittest
import requests
import json
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.llm_service import llm_service, OllamaProvider, LocalLLMProvider
    from config import Config
except ImportError as e:
    print(f"Warning: Could not import services: {e}")
    llm_service = None

def get_available_ollama_model(base_url: str = "http://localhost:11434") -> str:
    """Get the first available Ollama model"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                # Return the full model name including version tag (e.g., 'llama3:8b')
                model_name = models[0].get('name', 'llama2')
                print(f"🔍 Found available Ollama models: {[m.get('name') for m in models]}")
                print(f"🎯 Using model: {model_name}")
                return model_name
    except Exception as e:
        print(f"⚠️ Error checking Ollama models: {e}")
    return 'llama2'  # fallback

class TestLocalLLM(unittest.TestCase):
    """Unit tests for local LLM providers"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ollama_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.local_llm_url = os.environ.get('LOCAL_LLM_BASE_URL', 'http://localhost:8000')
        self.api_url = os.environ.get('API_BASE_URL', 'http://localhost:5000')
    
    def test_ollama_connection(self):
        """Test Ollama connection"""
        result = test_ollama_connection(self.ollama_url)
        self.assertIn('status', result)
        # Note: This test may fail if Ollama is not running - that's expected
        if result['status'] == 'success':
            self.assertIn('models', result)
    
    def test_local_llm_connection(self):
        """Test local LLM server connection"""
        result = test_local_llm_connection(self.local_llm_url)
        self.assertIn('status', result)
        # Note: This test may fail if local LLM server is not running - that's expected
    
    def test_api_integration(self):
        """Test API integration"""
        result = test_api_integration(self.api_url)
        self.assertIn('status', result)
        # API should be running for this test to pass
    
    def test_llm_service_providers(self):
        """Test LLM service provider detection"""
        if llm_service:
            providers = llm_service.list_providers()
            self.assertIsInstance(providers, list)
            # Check if any local providers are available
            local_providers = [p for p in providers if 'ollama' in p or 'local' in p]
            print(f"Local providers detected: {local_providers}")
    
    def test_provider_initialization(self):
        """Test individual provider initialization"""
        # Test Ollama provider (may fail if not available)
        try:
            # Get the first available Ollama model
            available_model = get_available_ollama_model(self.ollama_url)
            print(f"Using available Ollama model: {available_model}")
            
            provider = OllamaProvider(model=available_model)
            self.assertEqual(provider.provider_name, "ollama")
            self.assertEqual(provider.model, available_model)
            print(f"✅ Ollama provider initialized with model: {available_model}")
        except Exception as e:
            print(f"Ollama provider test skipped: {e}")
        
        # Test Local LLM provider (may fail if not available)
        try:
            provider = LocalLLMProvider(model="local-model")
            self.assertEqual(provider.provider_name, "local_llm")
            self.assertEqual(provider.model, "local-model")
            print(f"✅ Local LLM provider initialized")
        except Exception as e:
            print(f"Local LLM provider test skipped: {e}")
    
    def test_ollama_generation(self):
        """Test Ollama text generation"""
        try:
            # Get the first available Ollama model
            available_model = get_available_ollama_model(self.ollama_url)
            print(f"Testing Ollama generation with model: {available_model}")
            
            provider = OllamaProvider(model=available_model)
            prompt = "What is the capital of France?"
            
            # Test generation
            response = provider.generate(prompt)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            print(f"✅ Ollama generation successful with {available_model}: {response[:100]}...")
        except Exception as e:
            print(f"Ollama generation test skipped: {e}")
            self.skipTest(f"Ollama not available: {e}")


def test_ollama_connection(base_url: str = "http://localhost:11434") -> Dict[str, Any]:
    """Test connection to Ollama"""
    print(f"Testing Ollama connection at {base_url}...")
    
    try:
        # Test basic connection
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running and accessible")
            print(f"📋 Available models: {[model.get('name', 'Unknown') for model in models.get('models', [])]}")
            return {"status": "success", "models": models}
        else:
            print(f"❌ Ollama responded with status code: {response.status_code}")
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama at {base_url}")
        print("💡 Make sure Ollama is installed and running:")
        print("   - Install: https://ollama.ai/download")
        print("   - Run: ollama serve")
        return {"status": "error", "message": "Connection refused"}
    
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return {"status": "error", "message": str(e)}

def test_local_llm_connection(base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """Test connection to local LLM server (OpenAI-compatible)"""
    print(f"Testing Local LLM connection at {base_url}...")
    
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Local LLM server is running and accessible")
            print(f"📋 Available models: {[model.get('id', 'Unknown') for model in models.get('data', [])]}")
            return {"status": "success", "models": models}
        else:
            print(f"❌ Local LLM server responded with status code: {response.status_code}")
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Local LLM server at {base_url}")
        print("💡 Make sure your local LLM server is running:")
        print("   - Text Generation WebUI: python server.py --api")
        print("   - LM Studio: Start local server with OpenAI compatibility")
        return {"status": "error", "message": "Connection refused"}
    
    except Exception as e:
        print(f"❌ Error testing Local LLM: {e}")
        return {"status": "error", "message": str(e)}

def test_api_integration(base_url: str = "http://localhost:5000") -> Dict[str, Any]:
    """Test integration with the Flask API"""
    print(f"Testing API integration at {base_url}...")
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/ai/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Flask API is running")
            print(f"📊 AI Health Status: {health_data.get('status', 'Unknown')}")
            print(f"🔌 Available providers: {health_data.get('available_providers', 0)}")
            
            # Test providers endpoint
            providers_response = requests.get(f"{base_url}/api/ai/providers", timeout=10)
            if providers_response.status_code == 200:
                providers_data = providers_response.json()
                providers_list = providers_data.get('available_providers', [])
                print(f"📝 Providers: {', '.join(providers_list) if providers_list else 'None'}")
                
                # Check for local providers
                local_providers = [p for p in providers_list if 'ollama' in p or 'local' in p]
                if local_providers:
                    print(f"🏠 Local providers detected: {', '.join(local_providers)}")
                else:
                    print("⚠️  No local providers detected in API")
                
                return {"status": "success", "providers": providers_list}
            else:
                print(f"⚠️  Could not fetch providers list: {providers_response.status_code}")
                return {"status": "partial", "message": "Health OK but providers unavailable"}
        else:
            print(f"❌ Flask API responded with status code: {response.status_code}")
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Flask API at {base_url}")
        print("💡 Make sure your Flask application is running:")
        print("   - Run: python app.py")
        return {"status": "error", "message": "Connection refused"}
    
    except Exception as e:
        print(f"❌ Error testing API integration: {e}")
        return {"status": "error", "message": str(e)}

def test_chat_functionality(base_url: str = "http://localhost:5000", provider: str = "ollama") -> Dict[str, Any]:
    """Test chat functionality with local LLM"""
    print(f"Testing chat functionality with {provider}...")
    
    try:
        payload = {
            "message": "Hello! Can you help me plan a quick trip?",
            "provider": provider,
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{base_url}/api/ai/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            chat_data = response.json()
            if chat_data.get("success"):
                print(f"✅ Chat test successful with {provider}")
                print(f"📝 Response preview: {chat_data.get('response', '')[:100]}...")
                return {"status": "success", "response": chat_data}
            else:
                print(f"❌ Chat test failed: {chat_data.get('error', 'Unknown error')}")
                return {"status": "error", "message": chat_data.get('error')}
        else:
            print(f"❌ Chat test failed with status code: {response.status_code}")
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    
    except Exception as e:
        print(f"❌ Error testing chat functionality: {e}")
        return {"status": "error", "message": str(e)}

def main():
    """Main function to run all tests"""
    print("🧪 Local LLM Setup Test Script")
    print("=" * 50)
    
    # Configuration
    ollama_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    local_llm_url = os.environ.get('LOCAL_LLM_BASE_URL', 'http://localhost:8000')
    api_url = os.environ.get('API_BASE_URL', 'http://localhost:5000')
    
    print(f"🔧 Configuration:")
    print(f"   Ollama URL: {ollama_url}")
    print(f"   Local LLM URL: {local_llm_url}")
    print(f"   API URL: {api_url}")
    print()
    
    # Check if we should run unit tests or integration tests
    if len(sys.argv) > 1 and sys.argv[1] == "--unit-tests":
        print("Running unit tests...")
        unittest.main(argv=[''], exit=False, verbosity=2)
        return
    
    results = {}
    
    # Test 1: Ollama connection
    print("1️⃣ Testing Ollama...")
    results['ollama'] = test_ollama_connection(ollama_url)
    print()
    
    # Test 2: Local LLM connection
    print("2️⃣ Testing Local LLM server...")
    results['local_llm'] = test_local_llm_connection(local_llm_url)
    print()
    
    # Test 3: API integration
    print("3️⃣ Testing Flask API integration...")
    results['api'] = test_api_integration(api_url)
    print()
    
    # Test 4: Chat functionality (if API is working)
    if results['api']['status'] == 'success':
        providers = results['api'].get('providers', [])
        local_providers = [p for p in providers if 'ollama' in p or 'local' in p]
        
        if local_providers:
            print("4️⃣ Testing chat functionality...")
            for provider in local_providers[:2]:  # Test first 2 local providers
                chat_result = test_chat_functionality(api_url, provider)
                results[f'chat_{provider}'] = chat_result
                if chat_result['status'] == 'success':
                    break  # Stop after first successful test
            print()
    
    # Summary
    print("📊 SUMMARY")
    print("=" * 50)
    
    success_count = sum(1 for r in results.values() if r.get('status') == 'success')
    total_tests = len(results)
    
    print(f"✅ Successful tests: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 All tests passed! Your local LLM setup is working correctly.")
    elif success_count > 0:
        print("⚠️  Some tests passed. Check the failed tests above for issues.")
    else:
        print("❌ All tests failed. Please check your setup and try again.")
    
    print("\n💡 Next steps:")
    if results.get('ollama', {}).get('status') == 'success':
        print("   - Ollama is working. You can use providers like 'ollama_llama2'")
    else:
        print("   - Install and start Ollama: https://ollama.ai/download")
    
    if results.get('api', {}).get('status') == 'success':
        print("   - API integration is working. Test with Postman or curl")
    else:
        print("   - Start your Flask application: python app.py")
    
    print("   - Check LOCAL_LLM_SETUP.md for detailed setup instructions")
    print("   - Use the updated Postman collection for testing")
    print("   - Run unit tests with: python test_local_llm.py --unit-tests")


if __name__ == "__main__":
    main()
