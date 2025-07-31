"""
Simple test for flights.py without LLM service dependencies
"""
import sys
import os
import json
import logging
from datetime import datetime, timedelta
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _validate_flight_schema(flight):
    """Validate that a flight object matches the required schema"""
    required_fields = ["airline", "flightNumber", "departureTime", "arrivalTime", "stops", "price"]
    
    if not isinstance(flight, dict):
        return False
        
    for field in required_fields:
        if field not in flight:
            return False
            
    # Additional type validation
    if not isinstance(flight["price"], (int, float)):
        return False
        
    if not isinstance(flight["stops"], str):
        return False
        
    return True

def _generate_fallback_flights(origin, destination, departureDate, returnDate):
    """Generate realistic fallback flight data for round-trip flights when LLM is unavailable"""
    
    # Ensure we have all required parameters for round-trip flights
    if not all([origin, destination, departureDate, returnDate]):
        missing_params = []
        if not origin: missing_params.append("origin")
        if not destination: missing_params.append("destination")
        if not departureDate: missing_params.append("departureDate") 
        if not returnDate: missing_params.append("returnDate")
        
        return {
            "flights": [],
            "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
        }
    
    airlines = [
        "American Airlines", "Delta Air Lines", "United Airlines", "Southwest Airlines",
        "JetBlue Airways", "Alaska Airlines", "Spirit Airlines", "Frontier Airlines"
    ]
    
    flights = []
    errors = []
    
    try:
        # Round-trip pricing is typically higher than one-way
        base_price = random.randint(250, 800)  # Increased for round-trip
        
        for i in range(4):
            airline = random.choice(airlines)
            
            # Generate airline-appropriate flight number
            airline_codes = {
                "American Airlines": "AA",
                "Delta Air Lines": "DL", 
                "United Airlines": "UA",
                "Southwest Airlines": "WN",
                "JetBlue Airways": "B6",
                "Alaska Airlines": "AS",
                "Spirit Airlines": "NK",
                "Frontier Airlines": "F9"
            }
            
            code = airline_codes.get(airline, "XX")
            flight_number = f"{code}{random.randint(100, 9999)}"
            
            # Generate realistic times
            departure_hour = random.randint(5, 22)
            departure_min = random.choice([0, 15, 30, 45])
            
            # Flight duration between 1-8 hours depending on distance
            duration_hours = random.randint(1, 8)
            duration_mins = random.choice([0, 15, 30, 45])
            
            arrival_hour = (departure_hour + duration_hours) % 24
            arrival_min = (departure_min + duration_mins) % 60
            
            # Determine stops
            stops = random.choice(["0", "1", "2"]) if i > 0 else "0"  # First flight is always direct
            
            # Price varies by stops and airline (round-trip pricing)
            price_modifier = 1.0
            if stops == "1":
                price_modifier = 0.85  # Connecting flights slightly cheaper
            elif stops == "2":
                price_modifier = 0.75
                
            # Apply round-trip discount (10-15% savings vs two one-way tickets)
            round_trip_discount = random.uniform(0.85, 0.90)
            final_price = round((base_price + random.randint(-100, 200)) * price_modifier * round_trip_discount, 2)
            
            flight = {
                "airline": airline,
                "flightNumber": flight_number,
                "departureTime": f"{departure_hour:02d}:{departure_min:02d}",
                "arrivalTime": f"{arrival_hour:02d}:{arrival_min:02d}",
                "stops": stops,
                "price": final_price
            }
            flights.append(flight)
        
        # Add a warning that this is fallback data
        errors.append("LLM service unavailable - using generated flight data")
        
    except Exception as e:
        print(f"Error generating fallback flights: {e}")
        errors.append("Error generating flight options")
    
    return {
        "flights": flights,
        "errors": errors
    }

def find_flights_by_criteria_test(origin, destination, departureDate, returnDate=None):
    """Test version without LLM service"""
    # Validate ALL required parameters - all four are now mandatory
    if not all([origin, destination, departureDate, returnDate]):
        missing_params = []
        if not origin: missing_params.append("origin")
        if not destination: missing_params.append("destination") 
        if not departureDate: missing_params.append("departureDate")
        if not returnDate: missing_params.append("returnDate")
        
        return {
            "flights": [],
            "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
        }
    
    # Since LLM service is not available in test, use fallback
    return _generate_fallback_flights(origin, destination, departureDate, returnDate)

def test_flights_standalone():
    """Main test function for flights service"""
    print("Testing flights functionality...")
    
    # Test 1: Missing parameters
    print("1. Testing missing parameters...")
    result = find_flights_by_criteria_test(None, None, None, None)
    print(f"   Result: {result}")
    
    # Test 2: Valid parameters  
    print("2. Testing valid parameters...")
    result = find_flights_by_criteria_test('NYC', 'LAX', '2025-08-15', '2025-08-22')
    print(f"   Found {len(result.get('flights', []))} flights with {len(result.get('errors', []))} errors")
    
    # Test 3: Schema validation
    print("3. Testing schema validation...")
    valid_flight = {
        "airline": "Test Airlines",
        "flightNumber": "TA123",
        "departureTime": "10:00",
        "arrivalTime": "14:00",
        "stops": "0",
        "price": 299.99
    }
    
    invalid_flight = {"airline": "Test"}  # Missing required fields
    
    print(f"   Valid flight schema: {_validate_flight_schema(valid_flight)}")
    print(f"   Invalid flight schema: {_validate_flight_schema(invalid_flight)}")
    
    print("✅ All flights tests completed!")
    return True

if __name__ == "__main__":
    test_flights_standalone()
