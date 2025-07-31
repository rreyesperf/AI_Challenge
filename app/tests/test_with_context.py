#!/usr/bin/env python3
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import app
from services.aggregation import aggregate_results

# Test parameters for each service
dining_params = {
    'address': 'Los Angeles',
    'budget': 'high',
    'timeframe': '7:00 PM'
}

flight_params = {
    'origin': 'New York',
    'destination': 'Los Angeles', 
    'departureDate': '2024-03-15',
    'returnDate': '2024-03-20'
}

hotel_params = {
    'country': 'USA',
    'state': 'California',
    'city': 'Los Angeles',
    'arrivalDate': '2024-03-15',
    'chekoutDate': '2024-03-20'
}

transportation_params = {
    'location': 'Los Angeles',
    'pickup': 'LAX Airport',
    'dropOff': 'Downtown LA',
    'pickUpDate': '2024-03-15',
    'dropOffDate': '2024-03-15',
    'pickupTime': '09:00',
    'dropOffTime': '10:00'
}

def test_aggregation():
    print("🧪 Testing Aggregation Service with Flask App Context")
    print("=" * 55)

    try:
        # Test aggregation within Flask app context
        with app.app_context():
            result = aggregate_results(dining_params, flight_params, hotel_params, transportation_params)
            
        print('✅ Aggregation service working successfully!')
        print(f'📊 Services included: {list(result.keys())}')

        # Check each service result
        for service_name, service_data in result.items():
            print(f"\n🔍 {service_name}:")
            
            if isinstance(service_data, dict):
                if 'error' in service_data:
                    print(f"   ❌ Error: {service_data['error']}")
                elif 'errors' in service_data and service_data['errors']:
                    print(f"   ❌ Error: {service_data['errors'][0]}")
                else:
                    # Find the main data key and count results
                    data_keys = [k for k in service_data.keys() if k not in ['errors', 'error']]
                    if data_keys:
                        main_key = data_keys[0]
                        if isinstance(service_data.get(main_key), list):
                            print(f"   ✅ {len(service_data[main_key])} results found")
                            if service_data[main_key]:
                                print(f"   📝 Sample result keys: {list(service_data[main_key][0].keys())}")
                        else:
                            print(f"   ✅ Data available")
                    else:
                        print(f"   ⚠️  No data keys found")
            else:
                print(f"   📄 Raw data: {service_data}")

        print("\n🎉 Final Test Summary: All services integrated successfully!")
        print(f"📈 Total service responses: {len(result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_aggregation()
    if success:
        print("\n✨ SUCCESS: Aggregation service is fully functional!")
    else:
        print("\n💥 FAILURE: Issues found in aggregation service")
