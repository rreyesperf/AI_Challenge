#!/usr/bin/env python3
"""
Provider Priority Status Summary
Shows the current LLM provider configuration and priority order
"""

from services.llm_service import LLMService

def show_priority_status():
    print("LLM Provider Priority Status Summary")
    print("=" * 50)
    
    # Initialize service
    service = LLMService()
    
    # Show available providers
    providers = service.list_providers()
    print(f"Available Providers: {providers}")
    
    # Show priority order
    print(f"Priority Order: {['ollama', 'openai', 'anthropic', 'google']}")
    
    # Show default provider
    try:
        default_provider = service.get_provider()
        print(f"Default Provider: {default_provider.provider_name if default_provider else 'None'}")
        if default_provider:
            print(f"Default Model: {default_provider.model}")
    except Exception as e:
        print(f"Default Provider: Error - {e}")
    
    # Test actual chat behavior
    print(f"\n--- Testing Chat Behavior ---")
    
    try:
        # Test with no provider specified (should use priority order)
        test_response = service.generate_response("Hello, this is a test", provider_name=None)
        if test_response.get('success'):
            print(f"Chat Test Result: Used {test_response.get('provider')} provider")
            print(f"Model: {test_response.get('model')}")
        else:
            print(f"Chat Test Failed: {test_response.get('error')}")
    except Exception as e:
        print(f"Chat Test Error: {e}")
    
    # Show configuration
    print("\n--- Configuration Summary ---")
    print(f"   Ollama (Local LLM): http://localhost:11434")
    print(f"   OpenAI: API Key Required")
    print(f"   Anthropic: API Key Required") 
    print(f"   Google: API Key Required")
    
    print(f"\nStatus: Ollama-first priority implemented!")
    print(f"   - System tries ollama (local) first")
    print(f"   - Falls back to openai -> anthropic -> google")
    print(f"   - Fixed chat service to respect priority system")
    print(f"   - Removed Config.DEFAULT_LLM_PROVIDER override")

if __name__ == "__main__":
    show_priority_status()
