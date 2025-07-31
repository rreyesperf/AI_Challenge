#!/usr/bin/env python3
"""
Test script to verify LLM provider priority
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import llm_service

def test_provider_priority():
    """Test that providers are listed and used in the correct priority order"""
    
    print("🔍 Testing LLM Provider Priority Order")
    print("=" * 50)
    
    # Test 1: List providers and check order
    print("1. Testing provider list order...")
    providers = llm_service.list_providers()
    print(f"   Available providers: {providers}")
    
    # Check if local_llm is first
    if providers and providers[0] == 'local_llm':
        print("   ✅ local_llm is first in priority order")
    else:
        print(f"   ❌ Expected local_llm first, got: {providers[0] if providers else 'None'}")
    
    # Test 2: Check default provider selection
    print("\n2. Testing default provider selection...")
    try:
        provider = llm_service.get_provider(None)  # Use default
        print(f"   Default provider: {provider.provider_name}")
        
        if provider.provider_name == 'local_llm':
            print("   ✅ Default provider is local_llm")
        else:
            print(f"   ❌ Expected local_llm, got: {provider.provider_name}")
    except Exception as e:
        print(f"   ❌ Error getting default provider: {e}")
    
    # Test 3: Test generate_response with no provider specified
    print("\n3. Testing generate_response without specifying provider...")
    try:
        response = llm_service.generate_response(
            prompt="Hello, what is 2+2?",
            provider_name=None  # Use default
        )
        
        if response.get('success'):
            provider_used = response.get('provider')
            print(f"   Response provider: {provider_used}")
            
            if provider_used == 'local_llm':
                print("   ✅ generate_response used local_llm by default")
            else:
                print(f"   ❌ Expected local_llm, got: {provider_used}")
        else:
            print(f"   ❌ Response failed: {response.get('error')}")
    except Exception as e:
        print(f"   ❌ Error in generate_response: {e}")
    
    # Test 4: Test with OpenAI explicitly
    print("\n4. Testing explicit OpenAI provider...")
    try:
        response = llm_service.generate_response(
            prompt="Hello, what is 3+3?",
            provider_name="openai"  # Explicit OpenAI
        )
        
        if response.get('success'):
            provider_used = response.get('provider')
            print(f"   Response provider: {provider_used}")
            
            if provider_used == 'openai':
                print("   ✅ Explicit OpenAI provider working")
            else:
                print(f"   ❌ Expected openai, got: {provider_used}")
        else:
            print(f"   ⚠️ OpenAI response failed (might be expected): {response.get('error')}")
    except Exception as e:
        print(f"   ⚠️ OpenAI error (might be expected): {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Provider Priority Test Complete")

if __name__ == "__main__":
    test_provider_priority()
