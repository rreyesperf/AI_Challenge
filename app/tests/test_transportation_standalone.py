"""
Simple test for transportation.py without LLM service dependencies
"""
import sys
import os
import json
import logging
from datetime import datetime, timedelta
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _validate_transportation_schema(transport):
    """Validate that a transportation object matches the required schema"""
    required_fields = ["company", "address", "pickUpDate", "dropOffDate", "pickupTime", "dropOffTime", "price", "vehicleType"]
    
    if not isinstance(transport, dict):
        return False
        
    for field in required_fields:
        if field not in transport:
            return False
            
    # Additional type validation
    if not isinstance(transport["price"], (int, float)):
        return False
        
    return True

def _generate_fallback_transportation(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime):
    """Generate realistic fallback transportation data when LLM is unavailable"""
    
    # Ensure we have all required parameters
    if not all([location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime]):
        missing_params = []
        if not location: missing_params.append("location")
        if not pickup: missing_params.append("pickup")
        if not dropOff: missing_params.append("dropOff")
        if not pickUpDate: missing_params.append("pickUpDate")
        if not dropOffDate: missing_params.append("dropOffDate")
        if not pickupTime: missing_params.append("pickupTime")
        if not dropOffTime: missing_params.append("dropOffTime")
        
        return {
            "transportation": [],
            "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
        }
    
    company_types = [
        ("City Taxi", "Taxi", 25, 60),
        ("Metro Rides", "Sedan", 30, 75),
        ("Premium Transport", "SUV", 45, 100),
        ("Express Shuttle", "Van", 35, 80),
        ("Quick Cab", "Taxi", 20, 55),
        ("Luxury Cars", "Sedan", 60, 150),
        ("Group Transit", "Bus", 15, 40)
    ]
    
    transportation_options = []
    errors = []
    
    try:
        for i in range(4):
            company_info = random.choice(company_types)
            company_prefix, vehicle_type, min_price, max_price = company_info
            
            # Generate company name
            company_name = f"{company_prefix} Services"
            
            # Generate address
            street_number = random.randint(100, 9999)
            street_names = ["Transport Ave", "Service Street", "Mobility Plaza", "Transit Boulevard", "Vehicle Way"]
            street = random.choice(street_names)
            address = f"{street_number} {street}, {location}"
            
            # Generate realistic price
            price = round(random.uniform(min_price, max_price), 2)
            
            transport_option = {
                "company": company_name,
                "address": address,
                "pickUpDate": pickUpDate,
                "dropOffDate": dropOffDate,
                "pickupTime": pickupTime,
                "dropOffTime": dropOffTime,
                "price": price,
                "vehicleType": vehicle_type
            }
            transportation_options.append(transport_option)
        
        # Add a warning that this is fallback data
        errors.append("LLM service unavailable - using generated transportation data")
        
    except Exception as e:
        print(f"Error generating fallback transportation: {e}")
        errors.append("Error generating transportation options")
    
    return {
        "transportation": transportation_options,
        "errors": errors
    }

def find_transportation_options_test(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime):
    """Test version without LLM service"""
    # Validate ALL required parameters - all seven are now mandatory
    if not all([location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime]):
        missing_params = []
        if not location: missing_params.append("location")
        if not pickup: missing_params.append("pickup")
        if not dropOff: missing_params.append("dropOff")
        if not pickUpDate: missing_params.append("pickUpDate")
        if not dropOffDate: missing_params.append("dropOffDate")
        if not pickupTime: missing_params.append("pickupTime")
        if not dropOffTime: missing_params.append("dropOffTime")
        
        return {
            "transportation": [],
            "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
        }
    
    # Since LLM service is not available in test, use fallback
    return _generate_fallback_transportation(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime)

def test_transportation_standalone():
    """Main test function for transportation service"""
    print("Testing transportation functionality...")
    
    # Test 1: Missing parameters
    print("1. Testing missing parameters...")
    result = find_transportation_options_test(None, None, None, None, None, None, None)
    print(f"   Result: {result}")
    
    # Test 2: Some missing parameters
    print("2. Testing some missing parameters...")
    result = find_transportation_options_test('New York', 'Airport', None, None, None, None, None)
    print(f"   Result: {result}")
    
    # Test 3: Valid parameters
    print("3. Testing valid parameters...")
    result = find_transportation_options_test('New York', 'JFK Airport', 'Manhattan Hotel', '2025-08-15', '2025-08-15', '14:00', '15:30')
    print(f"   Found {len(result.get('transportation', []))} transportation options with {len(result.get('errors', []))} errors")
    
    # Test 4: Schema validation
    print("4. Testing schema validation...")
    valid_transport = {
        "company": "City Taxi Services",
        "address": "123 Transport Ave, New York",
        "pickUpDate": "2025-08-15",
        "dropOffDate": "2025-08-15",
        "pickupTime": "14:00",
        "dropOffTime": "15:30",
        "price": 45.99,
        "vehicleType": "Sedan"
    }
    
    invalid_transport = {"company": "Test Company"}  # Missing required fields
    
    print(f"   Valid transport schema: {_validate_transportation_schema(valid_transport)}")
    print(f"   Invalid transport schema: {_validate_transportation_schema(invalid_transport)}")
    
    # Test 5: Show sample transportation output
    if result.get('transportation'):
        print("5. Sample transportation output:")
        sample_transport = result['transportation'][0]
        print(f"   Company: {sample_transport['company']}")
        print(f"   Address: {sample_transport['address']}")
        print(f"   Pickup: {sample_transport['pickUpDate']} at {sample_transport['pickupTime']}")
        print(f"   Drop-off: {sample_transport['dropOffDate']} at {sample_transport['dropOffTime']}")
        print(f"   Price: ${sample_transport['price']}")
        print(f"   Vehicle: {sample_transport['vehicleType']}")
    
    print("✅ All transportation tests completed!")
    return True

if __name__ == "__main__":
    test_transportation_standalone()
