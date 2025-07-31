#!/usr/bin/env python3
"""
Direct test of LLM service to debug empty responses
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_service import llm_service

def test_llm_directly():
    print("Testing LLM Service Directly")
    print("=" * 40)
    
    # Check available providers
    print("Available providers:", llm_service.list_providers())
    
    # Test simple query
    print("\nTesting simple query...")
    try:
        result = llm_service.generate_response("Hello, please respond with a brief greeting.")
        print(f"Success: {result.get('success')}")
        print(f"Provider: {result.get('provider')}")
        print(f"Model: {result.get('model')}")
        print(f"Response: '{result.get('response', '')}'")
        print(f"Error: {result.get('error', 'None')}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_directly()
