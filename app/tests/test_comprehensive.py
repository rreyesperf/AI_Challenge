#!/usr/bin/env python3
"""
Comprehensive test runner for the enhanced conversational travel assistant
"""

import sys
import os
import subprocess
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_file(test_file):
    """Run a test file and capture its output"""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("PASSED")
            print(result.stdout)
            return True
        else:
            print("FAILED")
            print(f"Return code: {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("TIMEOUT - Test took too long")
        return False
    except Exception as e:
        print(f"ERROR - {e}")
        return False

def test_imports():
    """Test that all key imports work"""
    print("\nTesting Imports...")
    try:
        from services.llm_service import llm_service
        from services.lmintegration import enhanced_chat_service, chat_service
        from routes import create_app
        print("SUCCESS: All imports successful")
        return True
    except Exception as e:
        print(f"FAILED: Import failed: {e}")
        return False

def test_code_compilation():
    """Test that code compiles correctly"""
    print("\nTesting Code Compilation...")
    try:
        import py_compile
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        files_to_check = [
            os.path.join(parent_dir, 'services', 'lmintegration.py'),
            os.path.join(parent_dir, 'routes.py'),
            os.path.join(parent_dir, 'app.py')
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                py_compile.compile(file_path, doraise=True)
                print(f"SUCCESS: {os.path.basename(file_path)} compiles correctly")
            else:
                print(f"WARNING: {file_path} not found")
        
        return True
    except Exception as e:
        print(f"FAILED: Compilation failed: {e}")
        return False

def main():
    """Main test runner"""
    print("Enhanced Conversational Travel Assistant - Comprehensive Test Suite")
    print("="*80)
    
    # Track test results
    results = []
    
    # Test 1: Code compilation and imports
    print("\nPhase 1: Code Quality Checks")
    results.append(("Code Compilation", test_code_compilation()))
    results.append(("Import Tests", test_imports()))
    
    # Test 2: Core functionality (non-API tests)
    print("\nPhase 2: Core Functionality Tests")
    core_tests = [
        "test_llm_direct.py",
        "test_chat_services.py"
    ]
    
    for test in core_tests:
        if os.path.exists(test):
            results.append((test, run_test_file(test)))
        else:
            print(f"WARNING: Test file {test} not found")
            results.append((test, False))
    
    # Test 3: API tests (requires running server)
    print("\nPhase 3: API Integration Tests")
    print("INFO: These tests require the Flask server to be running on localhost:5000")
    print("INFO: Start server with: python ../app.py")
    
    # Check if server is running
    import requests
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=2)
        if response.status_code == 200:
            print("SUCCESS: Server is running - proceeding with API tests")
            
            api_tests = [
                "test_api_endpoints.py",
                "test_travel_features.py"
            ]
            
            for test in api_tests:
                if os.path.exists(test):
                    results.append((test, run_test_file(test)))
                else:
                    print(f"WARNING: Test file {test} not found")
                    results.append((test, False))
        else:
            print("WARNING: Server responded but not healthy - skipping API tests")
    except Exception:
        print("WARNING: Server not running - skipping API tests")
        print("   To run API tests, start server with: python ../app.py")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name:<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\nALL TESTS PASSED! The enhanced conversational travel assistant is working correctly!")
        return 0
    else:
        print(f"\n{failed} test(s) failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
