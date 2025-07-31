#!/usr/bin/env python3
"""
Test to validate LLM provider priority order
This test will mock multiple providers and verify the priority order is followed
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_service import LLMService, OllamaProvider, OpenAIProvider

class TestLLMProviderPriority(unittest.TestCase):
    """Test LLM provider priority order"""
    
    def setUp(self):
        """Set up test environment"""
        self.service = LLMService()
    
    @patch('services.llm_service.OPENAI_AVAILABLE', True)
    @patch('services.llm_service.REQUESTS_AVAILABLE', True)
    @patch('services.llm_service.Config')
    def test_priority_order_with_multiple_providers(self, mock_config):
        """Test that Ollama is prioritized over OpenAI when both are available"""
        
        # Mock config with both Ollama and OpenAI available
        mock_config.OPENAI_API_KEY = "test-openai-key"
        mock_config.OLLAMA_BASE_URL = "http://localhost:11434"
        mock_config.MAX_TOKENS = 2000
        mock_config.TEMPERATURE = 0.7
        
        # Mock successful Ollama connection
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "models": [{"name": "llama3"}]
            }
            mock_get.return_value = mock_response
            
            # Mock OpenAI client creation
            with patch('openai.OpenAI') as mock_openai_client:
                mock_openai_client.return_value = MagicMock()
                
                # Reinitialize service with mocked providers
                service = LLMService()
                
                # Verify both providers are available
                providers = service.list_providers()
                self.assertIn('ollama', providers)
                self.assertIn('openai', providers)
                
                # Verify Ollama comes first in priority order
                self.assertEqual(providers[0], 'ollama')
                self.assertEqual(providers[1], 'openai')
                
                # Test get_provider returns Ollama by default
                default_provider = service.get_provider()
                self.assertEqual(default_provider.provider_name, 'ollama')
                
                print("✅ Priority test passed: Ollama is prioritized over OpenAI")
    
    @patch('services.llm_service.OPENAI_AVAILABLE', True)
    @patch('services.llm_service.REQUESTS_AVAILABLE', True)
    @patch('services.llm_service.Config')
    def test_fallback_when_ollama_fails(self, mock_config):
        """Test that system falls back to OpenAI when Ollama fails"""
        
        # Mock config
        mock_config.OPENAI_API_KEY = "test-openai-key"
        mock_config.OLLAMA_BASE_URL = "http://localhost:11434"
        mock_config.MAX_TOKENS = 2000
        mock_config.TEMPERATURE = 0.7
        
        # Mock Ollama connection failure
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection refused")
            
            # Mock OpenAI client creation
            with patch('openai.OpenAI') as mock_openai_client:
                mock_openai_client.return_value = MagicMock()
                
                # Reinitialize service
                service = LLMService()
                
                # Verify OpenAI is available but Ollama is not
                providers = service.list_providers()
                self.assertNotIn('ollama', providers)
                self.assertIn('openai', providers)
                
                # Test get_provider returns OpenAI as fallback
                default_provider = service.get_provider()
                self.assertEqual(default_provider.provider_name, 'openai')
                
                print("✅ Fallback test passed: OpenAI used when Ollama unavailable")

    def test_current_service_priority(self):
        """Test the current service configuration"""
        providers = self.service.list_providers()
        print(f"📋 Current available providers: {providers}")
        
        if providers:
            default_provider = self.service.get_provider()
            print(f"⭐ Current default provider: {default_provider.provider_name}")
            
            # Verify the first provider is highest priority
            expected_priority = ['ollama', 'openai', 'anthropic', 'google']
            if providers:
                for expected in expected_priority:
                    if expected in providers:
                        self.assertEqual(providers[0], expected)
                        print(f"✅ Priority verified: {expected} is first available provider")
                        break
        else:
            print("⚠️ No providers available in current configuration")

def main():
    """Run the priority validation tests"""
    print("🧪 Testing LLM Provider Priority Order")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
    
    # Also run a direct check
    print("\n" + "=" * 50)
    print("🔍 Direct Service Check")
    print("=" * 50)
    
    service = LLMService()
    providers = service.list_providers()
    print(f"Available providers: {providers}")
    
    if providers:
        default_provider = service.get_provider()
        print(f"Default provider: {default_provider.provider_name}")
        print(f"Model: {default_provider.model}")

if __name__ == "__main__":
    main()
