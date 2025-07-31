import json
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def find_flights_by_criteria(origin, destination, departureDate, returnDate=None):
    """
    Finds flight options using LLM service based on origin, destination, departure date, and return date.
    Returns flight data in the specified JSON schema format.
    NOTE: This service only supports round-trip flights.
    
    Args:
        origin (str): Origin airport code or city
        destination (str): Destination airport code or city  
        departureDate (str): Departure date in YYYY-MM-DD format
        returnDate (str): Return date in YYYY-MM-DD format for round-trip flights (REQUIRED)
    
    Returns:
        dict: Dictionary with flights array and errors array
    """
    try:
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
        
        # Import LLM service here to avoid circular imports
        from .llm_service import llm_service
        
        # Use None to let get_provider() handle priority selection and fallback
        provider_name = None
        logger.info(f"Using default LLM provider with fallback logic")
        
        # Create a detailed prompt for round-trip flight search
        prompt = f"""
You are a flight booking assistant. Find realistic flight options for a round-trip journey from {origin} to {destination}, departing on {departureDate} and returning on {returnDate}.

Provide 4-6 flight options (outbound flights) with the following exact JSON format:
[
    {{
        "airline": "American Airlines",
        "flightNumber": "AA1234",
        "departureTime": "08:30",
        "arrivalTime": "14:45",
        "stops": "0",
        "price": 299.99
    }}
]

Consider realistic:
- Flight times based on route distance between {origin} and {destination}
- Round-trip pricing for flights departing {departureDate} and returning {returnDate}
- Major airlines that service these routes
- Mix of direct flights (stops: "0") and connecting flights (stops: "1" or "2")
- Departure times spread throughout the day
- Realistic flight durations
- Round-trip discounts reflected in pricing

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
                flight_data = json.loads(response['response'])
                
                # Ensure it's a list and validate structure
                if isinstance(flight_data, list):
                    # Validate each flight has required fields
                    validated_flights = []
                    validation_errors = []
                    
                    for i, flight in enumerate(flight_data):
                        if _validate_flight_schema(flight):
                            validated_flights.append(flight)
                        else:
                            validation_errors.append(f"Flight {i+1} has invalid schema")
                    
                    if validated_flights:
                        return {
                            "flights": validated_flights,
                            "errors": validation_errors if validation_errors else []
                        }
                    else:
                        logger.warning("LLM returned flights with invalid schema, using fallback")
                        return _generate_fallback_flights(origin, destination, departureDate, returnDate)
                else:
                    logger.warning("LLM returned non-array response, using fallback")
                    return _generate_fallback_flights(origin, destination, departureDate, returnDate)
                    
            except json.JSONDecodeError:
                logger.warning("LLM returned invalid JSON, using fallback data")
                return _generate_fallback_flights(origin, destination, departureDate, returnDate)
        else:
            logger.warning("LLM service unavailable, using fallback data")
            return _generate_fallback_flights(origin, destination, departureDate, returnDate)
            
    except ImportError:
        logger.warning("LLM service not available")
        return {
            "flights": [],
            "errors": ["No services available at the moment"]
        }
    except Exception as e:
        logger.error(f"Error in flight search: {e}")
        return {
            "flights": [],
            "errors": ["No services available at the moment"]
        }


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
        logger.error(f"Error generating fallback flights: {e}")
        errors.append("Error generating flight options")
    
    return {
        "flights": flights,
        "errors": errors
    }
