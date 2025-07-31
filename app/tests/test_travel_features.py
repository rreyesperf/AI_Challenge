#!/usr/bin/env python3
"""
Test enhanced travel conversation capabilities
"""

import requests
import json
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_travel_conversations():
    base_url = "http://localhost:5000"
    
    print("Testing Enhanced Travel Conversation Features")
    print("=" * 60)
    
    # Test 1: Travel intent
    print("1. Testing travel intent...")
    try:
        response = requests.post(
            f"{base_url}/api/ai/chat",
            json={"message": "I need help planning a business trip to Tokyo"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Conversation type: {data.get('conversation_type', 'regular')}")
            preview = data.get('response', '')[:100] + "..." if len(data.get('response', '')) > 100 else data.get('response', '')
            print(f"   Response: {preview}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Non-travel conversation
    print("2. Testing non-travel conversation...")
    try:
        response = requests.post(
            f"{base_url}/api/ai/chat",
            json={"message": "What's 2+2?"},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Provider: {data.get('provider', 'unknown')}")
            preview = data.get('response', '')[:50] + "..." if len(data.get('response', '')) > 50 else data.get('response', '')
            print(f"   Response: {preview}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
    
    print("Enhanced Travel Conversation Testing Complete!")

if __name__ == "__main__":
    # Give the server a moment
    time.sleep(1)
    test_travel_conversations()
