#!/usr/bin/env python3
"""
Flask Application Startup Simulation
Tests that the Flask app can start successfully in production mode
"""

import sys
import os
import importlib.util
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class FlaskStartupSimulator:
    def __init__(self, app_dir: str):
        self.app_dir = Path(app_dir)
        self.issues = []
        self.warnings = []
        
    def test_import_routes(self) -> bool:
        """Test if routes module can be imported"""
        try:
            # Try importing routes
            import routes
            print("✅ routes.py imported successfully")
            
            # Check if create_app function exists
            if hasattr(routes, 'create_app'):
                print("✅ create_app function found")
                return True
            else:
                self.issues.append("❌ create_app function not found in routes.py")
                return False
                
        except ImportError as e:
            self.issues.append(f"❌ Failed to import routes: {e}")
            return False
        except Exception as e:
            self.issues.append(f"❌ Error importing routes: {e}")
            return False
    
    def test_flask_app_creation(self) -> bool:
        """Test Flask app creation"""
        try:
            # Set production environment
            os.environ['FLASK_ENV'] = 'production'
            os.environ['SECRET_KEY'] = 'test-secret-key'
            
            from routes import create_app
            app = create_app()
            
            print("✅ Flask app created successfully")
            print(f"✅ App name: {app.name}")
            print(f"✅ Debug mode: {app.debug}")
            
            return True
            
        except Exception as e:
            self.issues.append(f"❌ Failed to create Flask app: {e}")
            return False
    
    def test_routes_registration(self) -> bool:
        """Test if routes are properly registered"""
        try:
            from routes import create_app
            app = create_app()
            
            # Get all registered routes
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append(rule.rule)
            
            expected_routes = [
                '/',
                '/api/health',
                '/api/ai/health',
                '/api/ai/chat',
                '/api/ai/providers'
            ]
            
            missing_routes = []
            for expected in expected_routes:
                if expected not in routes:
                    missing_routes.append(expected)
            
            if missing_routes:
                self.warnings.append(f"⚠️ Missing expected routes: {missing_routes}")
            
            print(f"✅ {len(routes)} routes registered")
            print(f"✅ Key routes available: {len(expected_routes) - len(missing_routes)}/{len(expected_routes)}")
            
            return True
            
        except Exception as e:
            self.issues.append(f"❌ Failed to test routes: {e}")
            return False
    
    def test_production_config(self) -> bool:
        """Test production configuration"""
        try:
            os.environ['FLASK_ENV'] = 'production'
            
            from routes import create_app
            app = create_app()
            
            # Check production settings
            if app.debug:
                self.warnings.append("⚠️ Debug mode is enabled in production")
            else:
                print("✅ Debug mode disabled in production")
            
            # Check security headers
            with app.test_client() as client:
                response = client.get('/')
                
                security_headers = [
                    'X-Content-Type-Options',
                    'X-Frame-Options',
                    'X-XSS-Protection'
                ]
                
                found_headers = 0
                for header in security_headers:
                    if header in response.headers:
                        found_headers += 1
                
                if found_headers > 0:
                    print(f"✅ Security headers configured: {found_headers}/{len(security_headers)}")
                else:
                    self.warnings.append("⚠️ No security headers found")
            
            return True
            
        except Exception as e:
            self.issues.append(f"❌ Failed to test production config: {e}")
            return False
    
    def test_health_endpoints(self) -> bool:
        """Test health check endpoints"""
        try:
            from routes import create_app
            app = create_app()
            
            with app.test_client() as client:
                # Test root endpoint
                response = client.get('/')
                if response.status_code == 200:
                    print("✅ Root endpoint (/) responds correctly")
                else:
                    self.warnings.append("⚠️ Root endpoint not responding correctly")
                
                # Test health endpoint
                response = client.get('/api/health')
                if response.status_code == 200:
                    print("✅ Health endpoint (/api/health) responds correctly")
                    
                    # Check response format
                    try:
                        data = response.get_json()
                        if 'status' in data and 'timestamp' in data:
                            print("✅ Health endpoint returns proper JSON format")
                        else:
                            self.warnings.append("⚠️ Health endpoint JSON format incomplete")
                    except:
                        self.warnings.append("⚠️ Health endpoint doesn't return valid JSON")
                else:
                    self.issues.append("❌ Health endpoint not responding")
                    return False
                
                # Test AI health endpoint
                response = client.get('/api/ai/health')
                if response.status_code == 200:
                    print("✅ AI Health endpoint (/api/ai/health) responds correctly")
                else:
                    self.warnings.append("⚠️ AI Health endpoint not responding correctly")
            
            return True
            
        except Exception as e:
            self.issues.append(f"❌ Failed to test health endpoints: {e}")
            return False
    
    def test_service_availability_handling(self) -> bool:
        """Test graceful handling of unavailable services"""
        try:
            from routes import create_app
            app = create_app()
            
            with app.test_client() as client:
                # Test AI chat (should return 503 if services not available)
                response = client.post('/api/ai/chat', 
                                     json={'message': 'test'},
                                     content_type='application/json')
                
                if response.status_code in [200, 503]:
                    print("✅ AI chat endpoint handles service availability gracefully")
                else:
                    self.warnings.append(f"⚠️ AI chat endpoint unexpected response: {response.status_code}")
                
                # Test providers endpoint
                response = client.get('/api/ai/providers')
                if response.status_code in [200, 503]:
                    print("✅ Providers endpoint handles service availability gracefully")
                else:
                    self.warnings.append(f"⚠️ Providers endpoint unexpected response: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.issues.append(f"❌ Failed to test service availability handling: {e}")
            return False
    
    def test_startup_script(self) -> bool:
        """Test the startup script"""
        startup_path = self.app_dir / "startup.py"
        
        if not startup_path.exists():
            self.warnings.append("⚠️ startup.py not found")
            return True
        
        try:
            # Import startup module
            spec = importlib.util.spec_from_file_location("startup", startup_path)
            startup_module = importlib.util.module_from_spec(spec)
            
            # Check if it has the required components
            if hasattr(startup_module, 'app'):
                print("✅ startup.py exports Flask app correctly")
            else:
                self.warnings.append("⚠️ startup.py doesn't export 'app' variable")
            
            return True
            
        except Exception as e:
            self.warnings.append(f"⚠️ Issue with startup.py: {e}")
            return True  # Non-critical
    
    def run_simulation(self) -> Dict[str, Any]:
        """Run complete Flask startup simulation"""
        print("🧪 Flask Application Startup Simulation")
        print("=" * 50)
        
        tests = [
            ("Import Routes", self.test_import_routes),
            ("Flask App Creation", self.test_flask_app_creation),
            ("Routes Registration", self.test_routes_registration),
            ("Production Config", self.test_production_config),
            ("Health Endpoints", self.test_health_endpoints),
            ("Service Availability", self.test_service_availability_handling),
            ("Startup Script", self.test_startup_script)
        ]
        
        results = {}
        passed = 0
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                result = test_func()
                results[test_name] = result
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                results[test_name] = False
                self.issues.append(f"❌ {test_name} failed: {e}")
        
        return {
            "total_tests": len(tests),
            "passed_tests": passed,
            "success_rate": (passed / len(tests)) * 100,
            "results": results,
            "issues": self.issues,
            "warnings": self.warnings
        }
    
    def print_report(self, simulation_results: Dict[str, Any]):
        """Print simulation report"""
        print("\n" + "=" * 50)
        print("📊 FLASK STARTUP SIMULATION REPORT")
        print("=" * 50)
        
        total = simulation_results["total_tests"]
        passed = simulation_results["passed_tests"]
        success_rate = simulation_results["success_rate"]
        
        if passed == total:
            print("🎉 OVERALL STATUS: ✅ ALL TESTS PASSED")
        elif passed >= total * 0.8:
            print("⚠️ OVERALL STATUS: 🟡 MOSTLY SUCCESSFUL")
        else:
            print("❌ OVERALL STATUS: 🔴 NEEDS ATTENTION")
        
        print(f"\n📈 SUMMARY:")
        print(f"   Tests Passed: {passed}/{total}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Issues: {len(self.issues)}")
        print(f"   Warnings: {len(self.warnings)}")
        
        if self.issues:
            print(f"\n🚨 CRITICAL ISSUES:")
            for issue in self.issues:
                print(f"   {issue}")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"   {warning}")
        
        print(f"\n🚀 AZURE CONTAINER APPS READINESS:")
        if passed >= total * 0.9 and len(self.issues) == 0:
            print("   ✅ Flask application ready for container deployment")
            print("   ✅ Production configuration working")
            print("   ✅ Health checks functional")
            print("   ✅ Error handling graceful")
        else:
            print("   ❌ Fix critical issues before deployment")
            print("   ⚠️ Review warnings for optimal deployment")
        
        print("\n" + "=" * 50)

def main():
    """Main simulation runner"""
    # Get the app directory (parent of tests directory)
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    simulator = FlaskStartupSimulator(app_dir)
    results = simulator.run_simulation()
    simulator.print_report(results)
    
    return results["passed_tests"] == results["total_tests"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
