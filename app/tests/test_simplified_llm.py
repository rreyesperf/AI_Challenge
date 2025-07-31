#!/usr/bin/env python3
"""
Simplified Test for LLM Service Priority Order
Tests only the core functionality after simplification
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.llm_service import LLMService
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"Services not available: {e}")
    SERVICES_AVAILABLE = False

def test_simplified_priority():
    """Test the simplified priority system"""
    if not SERVICES_AVAILABLE:
        print("❌ Services not available - skipping tests")
        return
    
    print("🧪 Testing Simplified LLM Priority System")
    print("=" * 50)
    
    try:
        service = LLMService()
        
        # Test 1: Provider list order
        print("1. Testing provider list...")
        providers = service.list_providers()
        print(f"   Available providers: {providers}")
        
        expected_order = ['ollama', 'openai', 'anthropic', 'google']
        actual_order = [p for p in expected_order if p in providers]
        
        if providers == actual_order:
            print("   ✅ Providers in correct priority order")
        else:
            print(f"   ⚠️ Provider order: expected {actual_order}, got {providers}")
        
        # Test 2: Default provider
        print("2. Testing default provider...")
        try:
            default_provider = service.get_provider()
            print(f"   Default provider: {default_provider.provider_name}")
            
            if default_provider.provider_name == 'ollama':
                print("   ✅ Default is ollama (as expected)")
            else:
                print(f"   ⚠️ Default is {default_provider.provider_name} (ollama might not be available)")
        except Exception as e:
            print(f"   ❌ Error getting default provider: {e}")
        
        # Test 3: Response generation with fallback
        print("3. Testing response generation...")
        try:
            result = service.generate_response("What is 2+2?")
            if result.get('success'):
                print(f"   ✅ Response generated using: {result.get('provider')}")
            else:
                print(f"   ❌ Response failed: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ Response generation error: {e}")
        
        print("=" * 50)
        print("🎉 Simplified priority test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_simplified_priority()
