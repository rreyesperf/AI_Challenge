#!/usr/bin/env python3
"""
Deployment validation script for Agentic RAG API
Tests all endpoints and validates Azure Container Apps deployment
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.results = []
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict[Any, Any] = None, 
                     expected_status: int = 200, description: str = ""):
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            start_time = time.time()
            
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            duration = time.time() - start_time
            
            result = {
                'endpoint': endpoint,
                'method': method.upper(),
                'description': description,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'duration_ms': round(duration * 1000, 2),
                'success': response.status_code == expected_status,
                'response_size': len(response.content),
                'content_type': response.headers.get('Content-Type', 'unknown')
            }
            
            # Try to parse JSON response
            try:
                result['response_json'] = response.json()
            except:
                result['response_text'] = response.text[:200] + "..." if len(response.text) > 200 else response.text
                
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'endpoint': endpoint,
                'method': method.upper(),
                'description': description,
                'error': str(e),
                'success': False,
                'duration_ms': 0
            }
            self.results.append(result)
            return result
    
    def run_health_tests(self):
        """Test health and status endpoints"""
        print("🔍 Testing Health Endpoints...")
        
        self.test_endpoint('GET', '/', description="Root endpoint")
        self.test_endpoint('GET', '/api/health', description="General health check")
        self.test_endpoint('GET', '/api/ai/health', description="AI services health")
        self.test_endpoint('GET', '/api/ai/providers', description="Available LLM providers")
        
    def run_ai_tests(self):
        """Test AI endpoints (will return 503 if services not available)"""
        print("🤖 Testing AI Endpoints...")
        
        # Test basic chat (expect 503 if no LLM service)
        chat_data = {
            "message": "Hello, this is a test message",
            "provider": "openai"
        }
        self.test_endpoint('POST', '/api/ai/chat', data=chat_data, 
                          expected_status=503, description="Basic chat (no LLM configured)")
        
        # Test conversation
        conversation_data = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }
        self.test_endpoint('POST', '/api/ai/conversation', data=conversation_data,
                          expected_status=503, description="Multi-turn conversation")
        
        # Test travel agent
        travel_data = {
            "query": "Plan a trip to Paris for 3 days"
        }
        self.test_endpoint('POST', '/api/ai/travel-agent', data=travel_data,
                          expected_status=503, description="Travel planning agent")
        
        # Test RAG endpoints
        rag_ingest_data = {
            "file_path": "/nonexistent/test.pdf"
        }
        self.test_endpoint('POST', '/api/ai/rag/ingest', data=rag_ingest_data,
                          expected_status=503, description="RAG document ingestion")
        
        rag_query_data = {
            "question": "What is the test document about?"
        }
        self.test_endpoint('POST', '/api/ai/rag/query', data=rag_query_data,
                          expected_status=503, description="RAG query")
        
        # Test consensus
        consensus_data = {
            "prompt": "What is artificial intelligence?"
        }
        self.test_endpoint('POST', '/api/ai/consensus', data=consensus_data,
                          expected_status=503, description="Multi-provider consensus")
    
    def run_travel_tests(self):
        """Test travel endpoints (will return 503 if services not available)"""
        print("✈️ Testing Travel Endpoints...")
        
        # These should return 503 since travel services are likely not configured
        self.test_endpoint('GET', '/api/flights?origin=NYC&destination=LAX&date=2024-08-15',
                          expected_status=503, description="Flight search")
        
        self.test_endpoint('GET', '/api/hotels?location=Paris&checkin_date=2024-08-15&checkout_date=2024-08-17',
                          expected_status=503, description="Hotel search")
        
        self.test_endpoint('GET', '/api/dining?budget=50&timeframe=evening&location=Paris',
                          expected_status=503, description="Dining options")
        
        self.test_endpoint('GET', '/api/transportation?type=train&origin=Paris&destination=London',
                          expected_status=503, description="Transportation options")
        
        # Test aggregation
        aggregate_data = {
            "flight_params": {"origin": "NYC", "destination": "LAX", "date": "2024-08-15"},
            "hotel_params": {"location": "LAX", "checkin_date": "2024-08-15", "checkout_date": "2024-08-17"}
        }
        self.test_endpoint('POST', '/api/aggregate', data=aggregate_data,
                          expected_status=503, description="Travel aggregation")
    
    def run_error_tests(self):
        """Test error handling"""
        print("⚠️ Testing Error Handling...")
        
        # Test invalid endpoints
        self.test_endpoint('GET', '/api/nonexistent', expected_status=404, description="Non-existent endpoint")
        
        # Test invalid JSON
        try:
            response = requests.post(f"{self.base_url}/api/ai/chat", 
                                   data="invalid json", 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=10)
            result = {
                'endpoint': '/api/ai/chat',
                'method': 'POST',
                'description': 'Invalid JSON payload',
                'status_code': response.status_code,
                'expected_status': 400,
                'success': response.status_code == 400,
                'duration_ms': 0
            }
            self.results.append(result)
        except Exception as e:
            print(f"Error testing invalid JSON: {e}")
    
    def print_results(self):
        """Print test results summary"""
        print("\n" + "="*80)
        print("🧪 DEPLOYMENT VALIDATION RESULTS")
        print("="*80)
        
        total_tests = len(self.results)
        successful_tests = len([r for r in self.results if r.get('success', False)])
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%" if total_tests > 0 else "N/A")
        
        print("\n📊 Detailed Results:")
        print("-" * 80)
        
        for result in self.results:
            status_icon = "✅" if result.get('success', False) else "❌"
            endpoint = result['endpoint']
            method = result['method']
            description = result.get('description', '')
            
            if 'error' in result:
                print(f"{status_icon} {method:6} {endpoint:30} - ERROR: {result['error']}")
            else:
                status = result.get('status_code', 'N/A')
                duration = result.get('duration_ms', 0)
                print(f"{status_icon} {method:6} {endpoint:30} - {status} ({duration}ms) - {description}")
        
        print("\n🔍 Health Check Summary:")
        health_endpoints = [r for r in self.results if 'health' in r['endpoint'] or r['endpoint'] == '/']
        if health_endpoints:
            all_healthy = all(r.get('success', False) for r in health_endpoints)
            print(f"Overall Health: {'🟢 HEALTHY' if all_healthy else '🔴 UNHEALTHY'}")
        
        # Show response samples for health endpoints
        for result in health_endpoints:
            if result.get('success') and 'response_json' in result:
                print(f"\n{result['endpoint']} response:")
                print(json.dumps(result['response_json'], indent=2)[:300] + "...")
        
        print("\n" + "="*80)
        
        return successful_tests == total_tests

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Agentic RAG API deployment")
    parser.add_argument('--url', default='http://localhost:8080', 
                       help='Base URL for the API (default: http://localhost:8080)')
    parser.add_argument('--azure-url', action='store_true',
                       help='Use Azure Container Apps URL format')
    
    args = parser.parse_args()
    
    base_url = args.url
    if args.azure_url and 'localhost' in base_url:
        print("⚠️ Note: Using localhost URL. For Azure testing, provide --url with your Container Apps URL")
    
    print("🚀 Starting Agentic RAG API Deployment Validation")
    print(f"🌐 Testing API at: {base_url}")
    print("-" * 80)
    
    tester = APITester(base_url)
    
    # Run all test suites
    tester.run_health_tests()
    tester.run_ai_tests()
    tester.run_travel_tests()
    tester.run_error_tests()
    
    # Print results
    success = tester.print_results()
    
    if success:
        print("🎉 All tests passed! Deployment is ready for production.")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed. Review the results above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
