# Test Suite for Travel Booking Application

This directory contains all tests for the travel booking application.

## Structure

- `__init__.py` - Makes this directory a Python package
- `run_tests.py` - Main test runner that executes all tests
- `test_*.py` - Individual test files for different components

## Test Files

### Core Application Tests
- `test_flask_startup.py` - Tests Flask application startup and configuration
- `test_api.py` - API endpoint integration tests (requires running server)
- `test_installation.py` - Package installation verification

### Service Tests  
- `test_aggregation_comprehensive.py` - Comprehensive aggregation service tests
- `test_aggregation_final.py` - Final aggregation service validation
- `test_flights_standalone.py` - Standalone flights service tests
- `test_hotels_standalone.py` - Standalone hotels service tests
- `test_transportation_standalone.py` - Standalone transportation service tests

### LLM Service Tests
- `test_llm_service.py` - Unit tests for LLM service and providers (mocked)
- `test_local_llm_api.py` - API integration tests for local LLM endpoints
- `test_local_llm.py` - Setup and integration tests for local LLM services

### Integration Tests
- `test_with_context.py` - Tests services within Flask app context
- `test_final.py` - Final integration test for all services

## Running Tests

### Run All Core Tests (Recommended)
```bash
# From the tests directory - runs only working tests
python run_core_tests.py

# With exit codes for CI/CD
python run_core_tests.py --exit-code
```

### Run All Tests (Including API Tests)
```bash
# From the tests directory - includes API tests that require server
python run_tests.py

# With verbose output
python run_tests.py --verbose
```

### Run Individual Tests
```bash
# From the tests directory
python test_with_context.py
python test_final.py
python test_flask_startup.py

# Local LLM specific tests
python test_llm_service.py                # Unit tests for LLM service
python test_local_llm.py                  # Local LLM setup and integration
python test_local_llm.py --unit-tests     # Unit tests only
python test_local_llm_api.py              # API integration tests
```

### Run from Parent Directory
```bash
# From the app directory
python -m tests.run_tests
python -m tests.test_with_context
```

## Test Categories

### ✅ **Working Tests (100% Success Rate)**
- `test_aggregation_comprehensive.py` - Full aggregation testing
- `test_aggregation_final.py` - Final aggregation validation  
- `test_flask_startup.py` - Flask application startup
- `test_installation.py` - Package installation check
- `test_with_context.py` - Services with Flask context
- `test_final.py` - Final integration test
- `test_flights_standalone.py` - Standalone flights service tests
- `test_hotels_standalone.py` - Standalone hotels service tests
- `test_transportation_standalone.py` - Standalone transportation service tests

### ⚠️ **Tests Requiring Server**
- `test_api.py` - Requires Flask server running on localhost:5000

### 🔧 **Tests with Minor Issues (Fixed)**
- All standalone service tests now have proper test functions
- Import issues resolved
- Encoding issues fixed
- Parameter mismatches corrected

## Expected Test Results

When all services are working properly, you should see:
- **Aggregation Tests**: ✅ All passing - validates service integration
- **Flask Startup**: ✅ All passing - validates application configuration
- **Installation Tests**: ✅ Core packages working, optional LLM packages may be missing
- **Integration Tests**: ✅ All services return expected response formats

## Notes

- Tests use parent directory imports to access application code
- Some tests require Flask app context for services like dining
- LLM service errors are expected when API keys are not configured
- Missing optional packages (Anthropic, Google AI) are expected in development

## Troubleshooting

### Import Errors
If you see import errors, ensure you're running tests from the correct directory and that the parent directory contains the application code.

### Flask Context Errors
Some services require Flask app context. Use `test_with_context.py` as a reference for proper context setup.

### Missing Dependencies
Run `test_installation.py` to check which packages are installed and which are missing.
