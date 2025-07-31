import json
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def find_transportation_options(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime):
    """
    Finds transportation options using LLM service based on location, pickup, dropoff, dates and times.
    Returns transportation data in the specified JSON schema format.
    
    Args:
        location (str): Location or city name
        pickup (str): Pickup location/address  
        dropOff (str): Drop-off location/address
        pickUpDate (str): Pickup date in YYYY-MM-DD format
        dropOffDate (str): Drop-off date in YYYY-MM-DD format
        pickupTime (str): Pickup time in HH:MM format
        dropOffTime (str): Drop-off time in HH:MM format
    
    Returns:
        dict: Dictionary with transportation array and errors array
    """
    try:
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
        
        # Import LLM service here to avoid circular imports
        from .llm_service import llm_service
        
        # Use None to let get_provider() handle priority selection and fallback
        provider_name = None
        logger.info(f"Using default LLM provider with fallback logic")
        
        # Create a detailed prompt for transportation search
        prompt = f"""
You are a transportation booking assistant. Find realistic transportation options in {location} from {pickup} to {dropOff}, for pickup on {pickUpDate} at {pickupTime} and drop-off on {dropOffDate} at {dropOffTime}.

Provide 4-6 transportation options with the following exact JSON format:
[
    {{
        "company": "City Taxi Services",
        "address": "123 Transport Ave, {location}",
        "pickUpDate": "{pickUpDate}",
        "dropOffDate": "{dropOffDate}",
        "pickupTime": "{pickupTime}",
        "dropOffTime": "{dropOffTime}",
        "price": 45.99,
        "vehicleType": "Sedan"
    }}
]

Consider realistic:
- Transportation companies that would operate in {location}
- Accurate company addresses for the specified location
- Pricing appropriate for the distance from {pickup} to {dropOff}
- Mix of vehicle types: Sedan, SUV, Van, Bus, Taxi, Rideshare
- Realistic pricing based on vehicle type and distance
- Different service levels (economy, standard, premium)
- Time-based pricing considerations (peak hours, overnight, etc.)

Return only valid JSON array without any additional text or explanations.
"""

        # Generate response using LLM with dynamic provider
        response = llm_service.generate_response(
            prompt=prompt,
            provider_name=provider_name,  # Use first available provider
            temperature=0.7,
            max_tokens=1000
        )
        
        if response.get('success') and response.get('response'):
            try:
                # Parse the JSON response
                transportation_data = json.loads(response['response'])
                
                # Ensure it's a list and validate structure
                if isinstance(transportation_data, list):
                    # Validate each transportation option has required fields
                    validated_transportation = []
                    validation_errors = []
                    
                    for i, transport in enumerate(transportation_data):
                        if _validate_transportation_schema(transport):
                            validated_transportation.append(transport)
                        else:
                            validation_errors.append(f"Transportation option {i+1} has invalid schema")
                    
                    if validated_transportation:
                        return {
                            "transportation": validated_transportation,
                            "errors": validation_errors if validation_errors else []
                        }
                    else:
                        logger.warning("LLM returned transportation with invalid schema, using fallback")
                        return _generate_fallback_transportation(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime)
                else:
                    logger.warning("LLM returned non-array response, using fallback")
                    return _generate_fallback_transportation(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime)
                    
            except json.JSONDecodeError:
                logger.warning("LLM returned invalid JSON, using fallback data")
                return _generate_fallback_transportation(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime)
        else:
            logger.warning("LLM service unavailable, using fallback data")
            return _generate_fallback_transportation(location, pickup, dropOff, pickUpDate, dropOffDate, pickupTime, dropOffTime)
            
    except ImportError:
        logger.warning("LLM service not available")
        return {
            "transportation": [],
            "errors": ["No services available at the moment"]
        }
    except Exception as e:
        logger.error(f"Error in transportation search: {e}")
        return {
            "transportation": [],
            "errors": ["No services available at the moment"]
        }


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
        logger.error(f"Error generating fallback transportation: {e}")
        errors.append("Error generating transportation options")
    
    return {
        "transportation": transportation_options,
        "errors": errors
    }
