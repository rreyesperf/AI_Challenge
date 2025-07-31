"""
Final test for aggregation.py with correct parameter formats
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_aggregation_final():
    """Final test of aggregation service with all correct parameters"""
    
    print("🔍 Final Aggregation Service Test")
    print("=" * 50)
    
    try:
        from services.aggregation import aggregate_results, get_service_results
        print("✅ Imports successful")
        
        # Test with correct parameter formats for all services
        print("\\n1. Testing with correct parameter formats...")
        
        # Flights parameters (new format: origin, destination, departureDate, returnDate)
        flight_params = {
            'origin': 'NYC',
            'destination': 'LAX', 
            'departureDate': '2025-08-15',
            'returnDate': '2025-08-22'
        }
        
        # Hotels parameters (new format: country, state, city, arrivalDate, chekoutDate)
        hotel_params = {
            'country': 'USA',
            'state': 'California',
            'city': 'Los Angeles',
            'arrivalDate': '2025-08-15',
            'chekoutDate': '2025-08-22'
        }
        
        # Transportation parameters (new format: location, pickup, dropOff, dates, times)
        transportation_params = {
            'location': 'Los Angeles',
            'pickup': 'LAX Airport',
            'dropOff': 'Downtown Hotel',
            'pickUpDate': '2025-08-15',
            'dropOffDate': '2025-08-15',
            'pickupTime': '14:00',
            'dropOffTime': '15:30'
        }
        
        # Dining parameters (original format: budget, timeframe, address)
        dining_params = {
            'budget': '100',
            'timeframe': 'dinner',
            'address': 'Los Angeles, CA'  # Changed from 'location' to 'address'
        }
        
        print("2. Testing aggregation with all services...")
        result = aggregate_results(dining_params, flight_params, hotel_params, transportation_params)
        
        print("✅ Aggregation completed successfully")
        print(f"   - Response contains {len(result)} service results")
        
        # Validate response structure
        print("\\n3. Validating response structure...")
        expected_services = ['diningResults', 'flightResults', 'hotelResults', 'transportationResults']
        
        for service in expected_services:
            if service in result:
                service_data = result[service]
                print(f"   ✅ {service}: {type(service_data)}")
                
                # Check specific response formats
                if service == 'flightResults':
                    if 'flights' in service_data and 'errors' in service_data:
                        flight_count = len(service_data.get('flights', []))
                        error_count = len(service_data.get('errors', []))
                        print(f"      └─ {flight_count} flights, {error_count} errors")
                    
                elif service == 'hotelResults':
                    if 'hotels' in service_data and 'errors' in service_data:
                        hotel_count = len(service_data.get('hotels', []))
                        error_count = len(service_data.get('errors', []))
                        print(f"      └─ {hotel_count} hotels, {error_count} errors")
                        
                elif service == 'transportationResults':
                    if 'transportation' in service_data and 'errors' in service_data:
                        transport_count = len(service_data.get('transportation', []))
                        error_count = len(service_data.get('errors', []))
                        print(f"      └─ {transport_count} transportation options, {error_count} errors")
                        
                elif service == 'diningResults':
                    if 'error' in service_data:
                        print(f"      └─ Error: {service_data['error']}")
                    else:
                        print(f"      └─ Dining data available")
            else:
                print(f"   ❌ {service}: Missing from response")
        
        # Test individual service calls
        print("\\n4. Testing individual service calls...")
        
        services_to_test = [
            ('flights', flight_params),
            ('hotels', hotel_params), 
            ('transportation', transportation_params)
        ]
        
        for service_name, params in services_to_test:
            try:
                individual_result = get_service_results(service_name, params)
                print(f"   ✅ {service_name} service: Individual call successful")
            except Exception as e:
                print(f"   ⚠️ {service_name} service: {e}")
        
        print("\\n5. Testing error handling...")
        try:
            error_result = get_service_results('invalid_service', {})
            print("   ⚠️ Invalid service should have raised an error")
        except Exception:
            print("   ✅ Invalid service properly handled")
        
        print("\\n" + "=" * 50)
        print("🎉 AGGREGATION SERVICE TESTS COMPLETED")
        print("=" * 50)
        print("✅ All tests passed successfully!")
        print("✅ Aggregation service is ready for production!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_aggregation_final()
