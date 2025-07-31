#!/usr/bin/env python3
"""
Test the complete API endpoint to ensure priority is working end-to-end
"""

import requests
import json
import time

def test_api_endpoint():
    """Test the /api/ai/chat endpoint to verify priority behavior"""
    print("Testing /api/ai/chat endpoint priority behavior")
    print("=" * 60)
    
    # API endpoint
    url = "http://127.0.0.1:5000/api/ai/chat"
    
    # Test payload
    payload = {
        "message": "Hello, this is a priority test. Please tell me which LLM provider you are.",
        "conversation_history": []
    }
    
    # Test 1: No provider specified (should use priority order)
    print("Test 1: No provider specified (should use Ollama first)")
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"Provider used: {result.get('provider', 'Not specified')}")
            print(f"Model used: {result.get('model', 'Not specified')}")
            print(f"Response: {result.get('response', '')[:100]}...")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print("\n" + "-" * 60)
    
    # Test 2: Explicitly request Ollama
    print("Test 2: Explicitly request Ollama provider")
    payload_ollama = payload.copy()
    payload_ollama["provider"] = "ollama"
    
    try:
        response = requests.post(url, json=payload_ollama, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"Provider used: {result.get('provider', 'Not specified')}")
            print(f"Model used: {result.get('model', 'Not specified')}")
            print(f"Response: {result.get('response', '')[:100]}...")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print("\n" + "-" * 60)
    
    # Test 3: Request unavailable provider (should fallback)
    print("Test 3: Request OpenAI (should fallback to Ollama)")
    payload_openai = payload.copy()
    payload_openai["provider"] = "openai"
    
    try:
        response = requests.post(url, json=payload_openai, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"Provider used: {result.get('provider', 'Not specified')}")
            print(f"Model used: {result.get('model', 'Not specified')}")
            print(f"Success: {result.get('success', False)}")
            if not result.get('success'):
                print(f"Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("Backend Status: RUNNING")
            print(f"Enhanced Chat Available: {health_data.get('services', {}).get('enhanced_chat', False)}")
            print(f"LLM Service Available: {health_data.get('services', {}).get('llm_service', False)}")
            return True
        else:
            print(f"Backend Status: ERROR ({response.status_code})")
            return False
    except requests.exceptions.RequestException:
        print("Backend Status: NOT RUNNING")
        return False

def main():
    print("API Priority Test Suite")
    print("=" * 60)
    
    # Check if backend is running
    if not check_backend_status():
        print("\nPlease start the backend first:")
        print("cd \"c:\\Users\\reyes\\OneDrive\\Documentos\\AI_Challenge-main\\app\"")
        print("python app.py")
        return
    
    print("\n" + "=" * 60)
    
    # Run API tests
    test_api_endpoint()

if __name__ == "__main__":
    main()
