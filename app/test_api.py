"""
Example usage script for the Agentic RAG API
This script demonstrates how to use the various endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    
    response = requests.get(f"{BASE_URL}/api/ai/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed! Available providers: {data['available_providers']}")
        print(f"   Providers: {', '.join(data['providers'])}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_providers_list():
    """Test listing available providers"""
    print("\n📋 Testing providers list...")
    
    response = requests.get(f"{BASE_URL}/api/ai/providers")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total_count']} providers:")
        for provider in data['available_providers']:
            print(f"   - {provider}")
        return data['available_providers']
    else:
        print(f"❌ Failed to get providers: {response.status_code}")
        return []

def test_basic_chat(providers):
    """Test basic chat functionality"""
    print("\n💬 Testing basic chat...")
    
    test_message = "Hello! Can you tell me about the benefits of AI in travel planning?"
    
    # Test with the first available provider
    provider = providers[0] if providers else None
    
    payload = {
        "message": test_message,
        "provider": provider,
        "system_message": "You are a helpful travel AI assistant."
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/chat", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Chat successful with provider: {data.get('provider')}")
            print(f"   Response preview: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat failed: {data.get('error')}")
    else:
        print(f"❌ Chat request failed: {response.status_code}")
        print(f"   Response: {response.text}")
    
    return False

def test_travel_agent():
    """Test the travel planning agent"""
    print("\n🧳 Testing travel planning agent...")
    
    travel_query = "I need help planning a romantic weekend getaway to Paris for 2 people with a budget of $2000"
    
    payload = {
        "query": travel_query,
        "flight_params": {
            "origin": "NYC",
            "destination": "CDG", 
            "date": "2024-08-15"
        },
        "hotel_params": {
            "location": "Paris",
            "checkin_date": "2024-08-15",
            "checkout_date": "2024-08-17"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/travel-agent", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Travel agent response received!")
        print(f"   Intent Analysis: {data.get('intent_analysis', 'N/A')[:100]}...")
        if data.get('travel_analysis'):
            print("   Travel analysis completed successfully")
        return True
    else:
        print(f"❌ Travel agent failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_conversation():
    """Test multi-turn conversation"""
    print("\n🗣️ Testing conversation...")
    
    messages = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "I'm planning a trip to Japan. What should I know?"},
        {"role": "assistant", "content": "Japan is a wonderful destination! Here are some key things to know: 1) The best time to visit is spring or fall, 2) Learn basic Japanese phrases, 3) Get a JR Pass for transportation. What specific aspects would you like to know more about?"},
        {"role": "user", "content": "Tell me more about transportation options."}
    ]
    
    payload = {
        "messages": messages
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/conversation", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Conversation successful!")
            print(f"   Response preview: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Conversation failed: {data.get('error')}")
    else:
        print(f"❌ Conversation request failed: {response.status_code}")
    
    return False

def test_consensus(providers):
    """Test multi-provider consensus"""
    print("\n🤝 Testing multi-provider consensus...")
    
    if len(providers) < 2:
        print("⚠️ Need at least 2 providers for consensus testing, skipping...")
        return False
    
    prompt = "What are the most important factors to consider when choosing a travel destination?"
    
    payload = {
        "prompt": prompt,
        "providers": providers[:2]  # Use first 2 providers
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/consensus", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Consensus analysis completed!")
            print(f"   Providers used: {', '.join(data['providers_used'])}")
            print(f"   Consensus preview: {data['consensus'][:100]}...")
            return True
        else:
            print(f"❌ Consensus failed: {data.get('error')}")
    else:
        print(f"❌ Consensus request failed: {response.status_code}")
    
    return False

def create_sample_document():
    """Create a sample document for RAG testing"""
    sample_content = """
    Travel Guide: Best Practices for International Travel
    
    Planning Your Trip:
    1. Research your destination thoroughly
    2. Check visa and passport requirements
    3. Get travel insurance
    4. Notify your bank of travel plans
    5. Make copies of important documents
    
    Packing Tips:
    - Pack light and smart
    - Bring versatile clothing
    - Pack essentials in carry-on
    - Don't forget chargers and adapters
    
    Safety Considerations:
    - Research local customs and laws
    - Keep emergency contacts handy
    - Stay aware of your surroundings
    - Use reputable transportation
    
    Cultural Etiquette:
    - Learn basic phrases in the local language
    - Respect local customs and dress codes
    - Be mindful of tipping practices
    - Show respect for religious sites
    """
    
    # Create a temporary text file
    file_path = "sample_travel_guide.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    return file_path

def test_rag_workflow():
    """Test the complete RAG workflow"""
    print("\n📚 Testing RAG workflow...")
    
    # Create sample document
    doc_path = create_sample_document()
    print(f"   Created sample document: {doc_path}")
    
    # Test document ingestion
    print("   📥 Testing document ingestion...")
    ingest_payload = {"file_path": doc_path}
    ingest_response = requests.post(f"{BASE_URL}/api/ai/rag/ingest", json=ingest_payload)
    
    if ingest_response.status_code == 200:
        ingest_data = ingest_response.json()
        if ingest_data.get('success'):
            print(f"   ✅ Document ingested! Chunks: {ingest_data['chunk_count']}")
            document_hash = ingest_data['document_hash']
        else:
            print(f"   ❌ Ingestion failed: {ingest_data.get('message')}")
            return False
    else:
        print(f"   ❌ Ingestion request failed: {ingest_response.status_code}")
        return False
    
    # Wait a moment for processing
    time.sleep(1)
    
    # Test document querying
    print("   🔍 Testing document querying...")
    query_payload = {
        "question": "What are the most important safety considerations for international travel?"
    }
    query_response = requests.post(f"{BASE_URL}/api/ai/rag/query", json=query_payload)
    
    if query_response.status_code == 200:
        query_data = query_response.json()
        if query_data.get('success'):
            print("   ✅ RAG query successful!")
            print(f"      Answer preview: {query_data['answer'][:100]}...")
            print(f"      Sources used: {query_data['chunks_used']}")
        else:
            print(f"   ❌ RAG query failed: {query_data.get('message')}")
            return False
    else:
        print(f"   ❌ RAG query request failed: {query_response.status_code}")
        return False
    
    # Test document deletion
    print("   🗑️ Testing document deletion...")
    delete_payload = {"document_hash": document_hash}
    delete_response = requests.delete(f"{BASE_URL}/api/ai/rag/delete", json=delete_payload)
    
    if delete_response.status_code == 200:
        delete_data = delete_response.json()
        if delete_data.get('success'):
            print("   ✅ Document deleted successfully!")
        else:
            print(f"   ⚠️ Deletion warning: {delete_data.get('message')}")
    else:
        print(f"   ❌ Deletion request failed: {delete_response.status_code}")
    
    # Clean up file
    try:
        import os
        os.remove(doc_path)
        print(f"   🧹 Cleaned up sample file")
    except Exception as e:
        print(f"   ⚠️ Could not clean up file: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Agentic RAG API Tests")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("\n❌ Health check failed. Make sure the API server is running!")
        return
    
    # Get available providers
    providers = test_providers_list()
    
    if not providers:
        print("\n❌ No providers available. Check your API keys in the environment!")
        return
    
    # Run tests
    tests_passed = 0
    total_tests = 0
    
    # Basic chat test
    total_tests += 1
    if test_basic_chat(providers):
        tests_passed += 1
    
    # Conversation test
    total_tests += 1
    if test_conversation():
        tests_passed += 1
    
    # Travel agent test
    total_tests += 1
    if test_travel_agent():
        tests_passed += 1
    
    # Consensus test (only if multiple providers)
    if len(providers) >= 2:
        total_tests += 1
        if test_consensus(providers):
            tests_passed += 1
    
    # RAG workflow test
    total_tests += 1
    if test_rag_workflow():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your Agentic RAG API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the error messages above for details.")
    
    print("\n📖 See AGENTIC_API_DOCS.md for complete API documentation.")

if __name__ == "__main__":
    main()
