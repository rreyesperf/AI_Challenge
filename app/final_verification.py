#!/usr/bin/env python3
"""
Final verification test for the simplified Ollama-first priority system
"""

from services.llm_service import LLMService

def final_verification():
    print("🎯 Final Verification: Simplified Ollama-First Priority")
    print("=" * 60)
    
    service = LLMService()
    
    # Test 1: Verify priority order
    print("1. Verifying Priority Order:")
    providers = service.list_providers()
    print(f"   Available: {providers}")
    
    expected = ['ollama', 'openai', 'anthropic', 'google']
    filtered_expected = [p for p in expected if p in providers]
    
    if providers == filtered_expected:
        print("   ✅ CORRECT: Providers in exact priority order")
    else:
        print(f"   ❌ WRONG: Expected {filtered_expected}, got {providers}")
    
    # Test 2: Verify default selection
    print("\n2. Verifying Default Provider Selection:")
    try:
        default = service.get_provider()
        print(f"   Default: {default.provider_name}")
        
        if providers and default.provider_name == providers[0]:
            print("   ✅ CORRECT: Default is first available provider")
        else:
            print("   ❌ WRONG: Default should be first available")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 3: Verify fallback behavior
    print("\n3. Verifying Fallback Behavior:")
    try:
        result = service.chat_completion([
            {"role": "user", "content": "Hello, are you working?"}
        ])
        
        if result.get('success'):
            print(f"   ✅ SUCCESS: Response from {result['provider']}")
            if providers and result['provider'] == providers[0]:
                print("   ✅ CORRECT: Used first available provider")
            else:
                print(f"   ⚠️ INFO: Used {result['provider']} (first might be unavailable)")
        else:
            print(f"   ❌ FAILED: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 4: Configuration summary
    print("\n4. Configuration Summary:")
    print("   Local LLM = Ollama server at localhost:11434")
    print("   Priority: Ollama → OpenAI → Anthropic → Google") 
    print("   No LM Studio (removed)")
    print("   No separate LocalLLMProvider (removed)")
    
    print("\n" + "=" * 60)
    print("🎉 VERIFICATION COMPLETE")
    
    if providers and providers[0] == 'ollama':
        print("✅ SUCCESS: Ollama-first priority correctly implemented!")
        return True
    else:
        print("⚠️ WARNING: Check if Ollama server is running at localhost:11434")
        return False

if __name__ == "__main__":
    final_verification()
