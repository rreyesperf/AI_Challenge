#!/usr/bin/env python3
"""
Test enhanced chat service specifically
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.lmintegration import enhanced_chat_service, chat_service

def test_chat_services():
    print("Testing Chat Services")
    print("=" * 40)
    
    # Test basic chat service
    print("1. Testing basic chat service...")
    try:
        result = chat_service("Hello, how are you?")
        print(f"   Success: {result.get('success')}")
        print(f"   Provider: {result.get('provider')}")
        print(f"   Response: '{result.get('response', '')}'")
        print(f"   Error: {result.get('error', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n2. Testing enhanced chat service (regular chat)...")
    try:
        result = enhanced_chat_service("Hello, how are you?")
        print(f"   Success: {result.get('success')}")
        print(f"   Provider: {result.get('provider')}")
        print(f"   Response: '{result.get('response', '')}'")
        print(f"   Error: {result.get('error', 'None')}")
        print(f"   Conversation type: {result.get('conversation_type', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n3. Testing enhanced chat service (travel query)...")
    try:
        result = enhanced_chat_service("I want to plan a trip to Paris for 2 people")
        print(f"   Success: {result.get('success')}")
        print(f"   Provider: {result.get('provider')}")
        print(f"   Response: '{result.get('response', '')[:100]}{'...' if len(result.get('response', '')) > 100 else ''}")
        print(f"   Error: {result.get('error', 'None')}")
        print(f"   Conversation type: {result.get('conversation_type', 'None')}")
        print(f"   Status: {result.get('status', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_services()
