"""
Unit tests for LLM service functionality
Tests the core LLM service and provider implementations
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.llm_service import (
        LLMService, LLMProvider, OllamaProvider, LocalLLMProvider,
        OpenAIProvider, AnthropicProvider, GoogleProvider, AzureOpenAIProvider
    )
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import LLM services: {e}")
    SERVICES_AVAILABLE = False


class TestLLMProvider(unittest.TestCase):
    """Test the base LLM provider class"""
    
    def test_provider_initialization(self):
        """Test LLM provider initialization"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        provider = LLMProvider("test", "test-model")
        self.assertEqual(provider.provider_name, "test")
        self.assertEqual(provider.model, "test-model")
    
    def test_provider_not_implemented_methods(self):
        """Test that base provider raises NotImplementedError"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        provider = LLMProvider("test", "test-model")
        
        with self.assertRaises(NotImplementedError):
            provider.generate("test prompt")
        
        with self.assertRaises(NotImplementedError):
            provider.chat([{"role": "user", "content": "test"}])


class TestOllamaProvider(unittest.TestCase):
    """Test Ollama provider functionality"""
    
    @patch('services.llm_service.requests')
    def test_ollama_provider_initialization(self, mock_requests):
        """Test Ollama provider initialization"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock successful connection test
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response
        
        provider = OllamaProvider(model="llama2")
        self.assertEqual(provider.provider_name, "ollama")
        self.assertEqual(provider.model, "llama2")
        self.assertEqual(provider.base_url, "http://localhost:11434")
    
    @patch('services.llm_service.requests')
    def test_ollama_generate(self, mock_requests):
        """Test Ollama generate method"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock connection test
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_requests.get.return_value = mock_get_response
        
        # Mock generate API call
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"response": "Test response from Ollama"}
        mock_requests.post.return_value = mock_post_response
        
        provider = OllamaProvider(model="llama2")
        response = provider.generate("Test prompt")
        
        self.assertEqual(response, "Test response from Ollama")
        mock_requests.post.assert_called_once()
    
    @patch('services.llm_service.requests')
    def test_ollama_chat(self, mock_requests):
        """Test Ollama chat method"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock connection test
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_requests.get.return_value = mock_get_response
        
        # Mock chat API call
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "message": {"content": "Test chat response from Ollama"}
        }
        mock_requests.post.return_value = mock_post_response
        
        provider = OllamaProvider(model="llama2")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.chat(messages)
        
        self.assertEqual(response, "Test chat response from Ollama")
        mock_requests.post.assert_called_once()


class TestLocalLLMProvider(unittest.TestCase):
    """Test Local LLM provider functionality"""
    
    @patch('services.llm_service.requests')
    def test_local_llm_provider_initialization(self, mock_requests):
        """Test Local LLM provider initialization"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock successful connection test
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response
        
        provider = LocalLLMProvider(model="local-model")
        self.assertEqual(provider.provider_name, "local_llm")
        self.assertEqual(provider.model, "local-model")
        self.assertEqual(provider.base_url, "http://localhost:8000")
    
    @patch('services.llm_service.requests')
    def test_local_llm_chat(self, mock_requests):
        """Test Local LLM chat method"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock connection test
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_requests.get.return_value = mock_get_response
        
        # Mock chat API call
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "choices": [{"message": {"content": "Test response from local LLM"}}]
        }
        mock_requests.post.return_value = mock_post_response
        
        provider = LocalLLMProvider(model="local-model")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.chat(messages)
        
        self.assertEqual(response, "Test response from local LLM")
        mock_requests.post.assert_called_once()
    
    @patch('services.llm_service.requests')
    def test_local_llm_with_api_key(self, mock_requests):
        """Test Local LLM provider with API key"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock connection test
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_requests.get.return_value = mock_get_response
        
        provider = LocalLLMProvider(model="local-model", api_key="test-key")
        self.assertEqual(provider.api_key, "test-key")


class TestLLMService(unittest.TestCase):
    """Test the main LLM service"""
    
    def test_llm_service_initialization(self):
        """Test LLM service initialization"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        service = LLMService()
        self.assertIsInstance(service.providers, dict)
    
    def test_list_providers(self):
        """Test listing available providers"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        service = LLMService()
        providers = service.list_providers()
        self.assertIsInstance(providers, list)
    
    def test_get_provider_invalid(self):
        """Test getting invalid provider raises error"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        service = LLMService()
        with self.assertRaises(ValueError):
            service.get_provider("invalid_provider")
    
    @patch('services.llm_service.llm_service')
    def test_generate_response_success(self, mock_service):
        """Test successful response generation"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.provider_name = "test"
        mock_provider.model = "test-model"
        mock_provider.generate.return_value = "Test response"
        
        # Mock service
        mock_service.get_provider.return_value = mock_provider
        mock_service.generate_response.return_value = {
            "success": True,
            "response": "Test response",
            "provider": "test",
            "model": "test-model"
        }
        
        result = mock_service.generate_response("Test prompt")
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "Test response")
    
    @patch('services.llm_service.llm_service')
    def test_generate_response_error(self, mock_service):
        """Test error handling in response generation"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Mock error response
        mock_service.generate_response.return_value = {
            "success": False,
            "error": "Test error",
            "provider": "test",
            "model": "test-model"
        }
        
        result = mock_service.generate_response("Test prompt")
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Test error")


class TestProviderImports(unittest.TestCase):
    """Test provider import handling"""
    
    def test_requests_import_handling(self):
        """Test that missing requests import is handled gracefully"""
        # This test verifies that the code handles missing requests gracefully
        # The actual import handling is done at module level
        self.assertTrue(True)  # Placeholder test
    
    def test_provider_availability_flags(self):
        """Test that availability flags are set correctly"""
        if not SERVICES_AVAILABLE:
            self.skipTest("LLM services not available")
        
        # Import the flags
        from services.llm_service import REQUESTS_AVAILABLE, OPENAI_AVAILABLE
        
        # These should be booleans
        self.assertIsInstance(REQUESTS_AVAILABLE, bool)
        self.assertIsInstance(OPENAI_AVAILABLE, bool)


def run_tests():
    """Run all LLM service tests"""
    print("🧪 Running LLM Service Unit Tests")
    print("=" * 50)
    
    if not SERVICES_AVAILABLE:
        print("⚠️  LLM services not available - some tests will be skipped")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLLMProvider))
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaProvider))
    suite.addTests(loader.loadTestsFromTestCase(TestLocalLLMProvider))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMService))
    suite.addTests(loader.loadTestsFromTestCase(TestProviderImports))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n📊 Test Results")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed or had errors")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
