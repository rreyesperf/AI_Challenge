#!/usr/bin/env python3
"""
Test Runner for Travel Booking Application
Runs all tests in the tests directory
"""

import sys
import os
import importlib.util
from pathlib import Path
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestRunner:
    def __init__(self):
        self.tests_dir = Path(__file__).parent
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.results = {}
        
    def discover_tests(self):
        """Discover all test files in the tests directory"""
        test_files = []
        for file_path in self.tests_dir.glob("test_*.py"):
            if file_path.name != "__init__.py" and file_path.name != "run_tests.py":
                test_files.append(file_path)
        return sorted(test_files)
    
    def run_test_file(self, test_file_path):
        """Run a single test file"""
        test_name = test_file_path.stem
        print(f"\n🧪 Running {test_name}...")
        print("-" * 50)
        
        try:
            # Load the test module
            spec = importlib.util.spec_from_file_location(test_name, test_file_path)
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            
            # Look for main functions to run
            test_functions = []
            for attr_name in dir(test_module):
                attr = getattr(test_module, attr_name)
                if (callable(attr) and 
                    (attr_name.startswith('test_') or 
                     attr_name == 'main' or 
                     attr_name in ['test_aggregation', 'test_aggregation_final'])):
                    
                    # Skip functions that require parameters (like test_package)
                    import inspect
                    try:
                        sig = inspect.signature(attr)
                        required_params = [p for p in sig.parameters.values() 
                                         if p.default == inspect.Parameter.empty]
                        if len(required_params) > 0:
                            print(f"   Skipping {attr_name} (requires parameters)")
                            continue
                    except:
                        pass
                    
                    test_functions.append((attr_name, attr))
            
            if not test_functions:
                # Try to run the module directly if no test functions found
                print(f"   No test functions found, attempting to run module directly...")
                try:
                    # This will run the if __name__ == "__main__" block
                    with open(test_file_path, 'r', encoding='utf-8') as f:
                        exec(f.read())
                    self.passed += 1
                    self.results[test_name] = "PASSED"
                    print(f"✅ {test_name} completed successfully")
                except Exception as e:
                    self.failed += 1
                    self.results[test_name] = f"FAILED: {str(e)}"
                    print(f"❌ {test_name} failed: {e}")
                return
            
            # Run each test function
            for func_name, func in test_functions:
                try:
                    print(f"   Running {func_name}...")
                    result = func()
                    if result is False:
                        self.failed += 1
                        self.results[f"{test_name}.{func_name}"] = "FAILED"
                        print(f"   ❌ {func_name} failed")
                    else:
                        self.passed += 1
                        self.results[f"{test_name}.{func_name}"] = "PASSED"
                        print(f"   ✅ {func_name} passed")
                except Exception as e:
                    self.failed += 1
                    self.results[f"{test_name}.{func_name}"] = f"FAILED: {str(e)}"
                    print(f"   ❌ {func_name} failed with exception: {e}")
                    if "--verbose" in sys.argv:
                        traceback.print_exc()
            
        except Exception as e:
            self.failed += 1
            self.results[test_name] = f"FAILED TO LOAD: {str(e)}"
            print(f"❌ Failed to load {test_name}: {e}")
            if "--verbose" in sys.argv:
                traceback.print_exc()
    
    def run_all_tests(self):
        """Run all discovered tests"""
        print("🚀 Travel Booking Application Test Suite")
        print("=" * 60)
        
        test_files = self.discover_tests()
        
        if not test_files:
            print("❌ No test files found in tests directory")
            return False
        
        print(f"📋 Found {len(test_files)} test files:")
        for test_file in test_files:
            print(f"   - {test_file.name}")
        
        print("\n" + "=" * 60)
        
        # Run each test file
        for test_file in test_files:
            self.run_test_file(test_file)
        
        # Print summary
        self.print_summary()
        
        return self.failed == 0
    
    def print_summary(self):
        """Print test results summary"""
        total = self.passed + self.failed + self.skipped
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️ SOME TESTS FAILED")
        
        print(f"\n📈 Statistics:")
        print(f"   Total Tests: {total}")
        print(f"   Passed: {self.passed} ✅")
        print(f"   Failed: {self.failed} ❌") 
        print(f"   Skipped: {self.skipped} ⏭️")
        print(f"   Success Rate: {(self.passed/total*100) if total > 0 else 0:.1f}%")
        
        if self.results:
            print(f"\n📋 Detailed Results:")
            for test_name, result in self.results.items():
                status_icon = "✅" if result == "PASSED" else "❌"
                print(f"   {status_icon} {test_name}: {result}")
        
        print("\n" + "=" * 60)

def main():
    """Main test runner function"""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if "--exit-code" in sys.argv:
        sys.exit(0 if success else 1)
    
    return success

if __name__ == "__main__":
    main()
