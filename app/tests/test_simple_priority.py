#!/usr/bin/env python3
"""
Test script to verify LLM provider priority order
Priority: Ollama (Local) → OpenAI → Anthropic → Google
"""

from services.llm_service import LLMService

def test_provider_priority():
    print("🔍 Testing LLM Provider Priority Order")
    print("=" * 50)
    
    service = LLMService()
    
    print("1. Testing provider list order...")
    providers = service.list_providers()
    print(f"   Available providers: {providers}")
    
    # Check if ollama is first (when available)
    if providers and providers[0] == 'ollama':
        print("   ✅ ollama is first in priority order")
    elif 'ollama' in providers:
        print("   ❌ ollama should be first, but it's not")
    else:
        print("   ⚠️ ollama not available")
    
    print("2. Testing default provider selection...")
    try:
        default_provider = service.get_provider()
        print(f"   Default provider: {default_provider.provider_name}")
        if default_provider.provider_name == 'ollama':
            print("   ✅ Default provider is ollama")
        else:
            print(f"   ⚠️ Default provider is {default_provider.provider_name} (ollama might not be available)")
    except Exception as e:
        print(f"   ❌ Error getting default provider: {e}")
    
    print("3. Testing generate_response without specifying provider...")
    try:
        result = service.generate_response("Say hello")
        if result['success']:
            print(f"   Response provider: {result['provider']}")
            if result['provider'] == 'ollama':
                print("   ✅ Used ollama as expected")
            else:
                print(f"   ⚠️ Used {result['provider']} (ollama might not be available)")
        else:
            print(f"   ❌ Failed to generate response: {result['error']}")
    except Exception as e:
        print(f"   ❌ Error in generate_response: {e}")
    
    print("4. Testing explicit OpenAI provider...")
    try:
        result = service.generate_response("Say hello", provider_name="openai")
        if result['success']:
            print(f"   ✅ OpenAI provider working: {result['provider']}")
        else:
            print(f"   ⚠️ OpenAI error (might be expected): {result['error']}")
    except Exception as e:
        print(f"   ⚠️ OpenAI error (might be expected): {e}")
    
    print("=" * 50)
    print("🎯 Provider Priority Test Complete")

if __name__ == "__main__":
    test_provider_priority()
