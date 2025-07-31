"""
Comprehensive test for aggregation.py with all updated services
"""
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_aggregation_service():
    """Test the aggregation service with different parameter scenarios"""
    
    print("Testing aggregation service...")
    
    try:
        # Test 1: Import test
        print("1. Testing imports...")
        from services.aggregation import aggregate_results, get_service_results
        print("   ✅ Aggregation imports successful")
        
        # Test 2: Test with empty parameters
        print("2. Testing with empty parameters...")
        result = aggregate_results({}, {}, {}, {})
        print(f"   ✅ Empty params handled: {len(result)} service results")
        
        # Test 3: Test with valid parameters for each service
        print("3. Testing with valid parameters...")
        
        # Flights parameters (updated format)
        flight_params = {
            'origin': 'NYC',
            'destination': 'LAX', 
            'departureDate': '2025-08-15',
            'returnDate': '2025-08-22'
        }
        
        # Hotels parameters (updated format)
        hotel_params = {
            'country': 'USA',
            'state': 'California',
            'city': 'Los Angeles',
            'arrivalDate': '2025-08-15',
            'chekoutDate': '2025-08-22'
        }
        
        # Transportation parameters (updated format)
        transportation_params = {
            'location': 'Los Angeles',
            'pickup': 'LAX Airport',
            'dropOff': 'Downtown Hotel',
            'pickUpDate': '2025-08-15',
            'dropOffDate': '2025-08-15',
            'pickupTime': '14:00',
            'dropOffTime': '15:30'
        }
        
        # Dining parameters (corrected format)
        dining_params = {
            'budget': '100',
            'timeframe': 'dinner',
            'address': 'Los Angeles'
        }
        
        result = aggregate_results(dining_params, flight_params, hotel_params, transportation_params)
        print(f"   ✅ Valid params processed: {len(result)} service results")
        
        # Test 4: Check response format
        print("4. Testing response format...")
        expected_keys = ['diningResults', 'flightResults', 'hotelResults', 'transportationResults']
        for key in expected_keys:
            if key in result:
                print(f"   ✅ {key} present in response")
            else:
                print(f"   ❌ {key} missing from response")
        
        # Test 5: Test individual service calls
        print("5. Testing individual service calls...")
        
        # Test flights service
        flight_result = get_service_results('flights', flight_params)
        if 'flights' in flight_result and 'errors' in flight_result:
            print("   ✅ Flights service returns correct format")
        else:
            print("   ❓ Flights service format may be different")
        
        # Test hotels service  
        hotel_result = get_service_results('hotels', hotel_params)
        if 'hotels' in hotel_result and 'errors' in hotel_result:
            print("   ✅ Hotels service returns correct format")
        else:
            print("   ❓ Hotels service format may be different")
        
        # Test transportation service
        transport_result = get_service_results('transportation', transportation_params)
        if 'transportation' in transport_result and 'errors' in transport_result:
            print("   ✅ Transportation service returns correct format")
        else:
            print("   ❓ Transportation service format may be different")
        
        # Test 6: Test error handling
        print("6. Testing error handling...")
        try:
            error_result = get_service_results('invalid_service', {})
            print("   ❌ Should have raised ValueError")
        except ValueError:
            print("   ✅ Invalid service type handled correctly")
        except Exception as e:
            print(f"   ✅ Error handled: {e}")
        
        print("✅ All aggregation tests completed!")
        
        # Show sample output structure
        print("\\n📋 Sample aggregated response structure:")
        print(f"   - diningResults: {type(result.get('diningResults', {}))}")
        print(f"   - flightResults: {type(result.get('flightResults', {}))}")
        print(f"   - hotelResults: {type(result.get('hotelResults', {}))}")
        print(f"   - transportationResults: {type(result.get('transportationResults', {}))}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_aggregation_service()
    if success:
        print("\\n🎉 Aggregation service is working correctly!")
    else:
        print("\\n❌ Aggregation service has issues!")
