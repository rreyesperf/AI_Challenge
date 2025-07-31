#!/usr/bin/env python3
"""
Test the API endpoints using Python requests
"""

import requests
import json
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_api():
    base_url = "http://localhost:5000"
    
    print("Testing Enhanced API Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: Regular chat
    print("2. Testing regular chat...")
    try:
        response = requests.post(
            f"{base_url}/api/ai/chat",
            json={"message": "Hello, how are you?"},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Provider: {data.get('provider', 'unknown')}")
            preview = data.get('response', '')[:100] + "..." if len(data.get('response', '')) > 100 else data.get('response', '')
            print(f"   Response: {preview}")
        else:
            print(f"   Error: {response.text}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Travel planning
    print("3. Testing travel planning...")
    try:
        response = requests.post(
            f"{base_url}/api/ai/chat",
            json={"message": "I want to plan a trip to Paris for 2 people"},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Conversation type: {data.get('conversation_type', 'regular')}")
            print(f"   Status: {data.get('status', 'unknown')}")
            preview = data.get('response', '')[:150] + "..." if len(data.get('response', '')) > 150 else data.get('response', '')
            print(f"   Response: {preview}")
        else:
            print(f"   Error: {response.text}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Check old endpoints are gone
    print("4. Testing that old endpoints are unavailable...")
    old_endpoints = ["/api/flights", "/api/hotels", "/api/aggregate"]
    for endpoint in old_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 404:
                print(f"   [OK] {endpoint} properly unavailable")
            else:
                print(f"   [WARN] {endpoint} still available (status: {response.status_code})")
        except Exception as e:
            print(f"   [OK] {endpoint} properly unavailable")
    
    print("API Testing Complete!")

if __name__ == "__main__":
    # Give the server a moment to start
    time.sleep(2)
    test_api()
