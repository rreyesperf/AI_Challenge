#!/usr/bin/env python3
"""
Test script for Enhanced Conversational Travel Assistant
Tests the new single-endpoint chat system with travel planning capabilities
"""

import requests
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_chat_api():
    """Test the enhanced chat API with various scenarios"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Enhanced Conversational Travel Assistant")
    print("=" * 60)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Regular Chat",
            "message": "Hello, how are you?",
            "expected_type": "regular_chat"
        },
        {
            "name": "Travel Intent Detection",
            "message": "I want to plan a trip to Paris",
            "expected_type": "travel_planning"
        },
        {
            "name": "Specific Travel Request",
            "message": "I need flights from New York to London on March 15th returning March 22nd",
            "expected_type": "travel_planning"
        },
        {
            "name": "Vacation Planning",
            "message": "Help me plan a vacation to Japan for 2 people, budget $5000",
            "expected_type": "travel_planning"
        }
    ]
    
    print("1. Testing chat endpoint availability...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("   ✅ API is running")
        else:
            print("   ❌ API not responding properly")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to API. Make sure the server is running.")
        print("   💡 Run: python app.py")
        return False
    
    print("\n2. Testing enhanced chat scenarios...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['name']}")
        print(f"   Message: \"{test_case['message']}\"")
        
        try:
            response = requests.post(
                f"{base_url}/api/ai/chat",
                json={"message": test_case['message']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                if 'response' in data:
                    print(f"   ✅ Got response from: {data.get('provider', 'unknown')}")
                    
                    # Check if travel conversation was detected
                    if data.get('conversation_type') == 'travel_planning':
                        print(f"   🧳 Travel conversation detected!")
                        print(f"   Status: {data.get('status', 'unknown')}")
                    
                    # Show response preview
                    response_text = data['response'][:100] + "..." if len(data['response']) > 100 else data['response']
                    print(f"   Response: {response_text}")
                    
                else:
                    print(f"   ⚠️ Unexpected response format: {data}")
            else:
                print(f"   ❌ Request failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n3. Testing providers endpoint...")
    try:
        response = requests.get(f"{base_url}/api/ai/providers")
        if response.status_code == 200:
            data = response.json()
            providers = data.get('available_providers', [])
            print(f"   ✅ Available providers: {providers}")
            print(f"   Default provider: {data.get('default_provider', 'unknown')}")
        else:
            print(f"   ⚠️ Providers endpoint issue: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error checking providers: {e}")
    
    print("\n4. Testing endpoint restrictions...")
    
    # Test that old endpoints are no longer available
    old_endpoints = [
        "/api/flights",
        "/api/hotels", 
        "/api/dining",
        "/api/transportation",
        "/api/aggregate",
        "/api/ai/travel-agent",
        "/api/ai/conversation"
    ]
    
    available_endpoints = []
    unavailable_endpoints = []
    
    for endpoint in old_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code != 404:
                available_endpoints.append(endpoint)
            else:
                unavailable_endpoints.append(endpoint)
        except:
            unavailable_endpoints.append(endpoint)
    
    if available_endpoints:
        print(f"   ⚠️ Old endpoints still available: {available_endpoints}")
    else:
        print(f"   ✅ All old endpoints properly removed")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced Chat Test Complete!")
    
    return True

def test_direct_import():
    """Test direct import of enhanced services"""
    print("\n🔧 Testing Direct Service Import...")
    
    try:
        from services.lmintegration import enhanced_chat_service, travel_conversation_manager
        
        print("   ✅ Enhanced services imported successfully")
        
        # Test travel intent detection
        intent = travel_conversation_manager.detect_travel_intent("I want to go to Paris")
        print(f"   ✅ Travel intent detection working: {intent.get('is_travel_related', False)}")
        
        # Test basic chat
        response = enhanced_chat_service("Hello, how are you?")
        if response.get('success') or 'response' in response:
            print("   ✅ Enhanced chat service working")
        else:
            print(f"   ⚠️ Chat service response: {response}")
            
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Enhanced Conversational Travel Assistant - Test Suite")
    print("=" * 70)
    
    # Test direct imports first
    if test_direct_import():
        print("\n📡 Testing API endpoints...")
        test_enhanced_chat_api()
    else:
        print("❌ Direct import test failed - check your implementation")
    
    print("\n💡 Usage Tips:")
    print("   • Only /api/ai/chat is now publicly available")
    print("   • Try messages like 'plan a trip to Paris' to trigger travel assistant")
    print("   • All old travel endpoints are now internal services")
    print("   • Health endpoints remain available for monitoring")
