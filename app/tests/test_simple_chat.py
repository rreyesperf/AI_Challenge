#!/usr/bin/env python3
"""
Simple test for enhanced chat functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple():
    print("🧪 Simple Enhanced Chat Test")
    print("=" * 40)
    
    try:
        # Test 1: Import
        print("1. Testing imports...")
        from services.lmintegration import enhanced_chat_service
        print("   ✅ Enhanced chat service imported")
        
        # Test 2: Simple chat
        print("2. Testing basic chat...")
        response = enhanced_chat_service("Hello")
        print(f"   Response type: {type(response)}")
        print(f"   Keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
        
        if isinstance(response, dict) and 'response' in response:
            print("   ✅ Chat working")
            print(f"   Provider: {response.get('provider', 'unknown')}")
        else:
            print(f"   ⚠️ Unexpected response: {response}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple()
