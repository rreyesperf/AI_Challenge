#!/usr/bin/env python3
"""
Test to specifically check if chat_service respects priority
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.lmintegration import chat_service, enhanced_chat_service

def test_chat_service_priority():
    """Test that chat_service uses correct priority"""
    print("🧪 Testing chat_service priority behavior")
    print("=" * 50)
    
    # Test with no provider specified
    print("Testing with no provider specified:")
    response = chat_service("Hello, what's the weather like?")
    print(f"Response: {response}")
    
    # Test with provider=None explicitly
    print("\nTesting with provider=None explicitly:")
    response = chat_service("Hello again", provider=None)
    print(f"Response: {response}")
    
    # Test enhanced chat service
    print("\nTesting enhanced_chat_service:")
    response = enhanced_chat_service("Hello from enhanced service")
    print(f"Response: {response}")

if __name__ == "__main__":
    test_chat_service_priority()
