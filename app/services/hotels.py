import json
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def find_hotels_by_criteria(country, state, city, arrivalDate, chekoutDate):
    """
    Finds hotel options using LLM service based on country, state, city, arrival date, and checkout date.
    Returns hotel data in the specified JSON schema format.
    
    Args:
        country (str): Country name
        state (str): State or province name  
        city (str): City name
        arrivalDate (str): Arrival date in YYYY-MM-DD format
        chekoutDate (str): Checkout date in YYYY-MM-DD format
    
    Returns:
        list: List of hotel objects and errors array
    """
    try:
        # Validate ALL required parameters - all five are now mandatory
        if not all([country, state, city, arrivalDate, chekoutDate]):
            missing_params = []
            if not country: missing_params.append("country")
            if not state: missing_params.append("state")
            if not city: missing_params.append("city")
            if not arrivalDate: missing_params.append("arrivalDate")
            if not chekoutDate: missing_params.append("chekoutDate")
            
            return {
                "hotels": [],
                "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
            }
        
        # Import LLM service here to avoid circular imports
        from .llm_service import llm_service
        
        # Use None to let get_provider() handle priority selection and fallback
        provider_name = None
        logger.info(f"Using default LLM provider with fallback logic")
        logger.info(f"Using LLM provider: {provider_name}")
        
        # Create a detailed prompt for hotel search
        prompt = f"""
You are a hotel booking assistant. Find realistic hotel options in {city}, {state}, {country} for dates from {arrivalDate} to {chekoutDate}.

Provide 4-6 hotel options with the following exact JSON format:
[
    {{
        "hotel": "Grand Palace Hotel",
        "address": "123 Main Street, {city}, {state}, {country}",
        "arrivalDate": "{arrivalDate}",
        "chekoutDate": "{chekoutDate}",
        "price": 299.99,
        "rating": 4.5
    }}
]

Consider realistic:
- Hotel names that would exist in {city}, {state}, {country}
- Accurate addresses for the specified location
- Pricing appropriate for the location and dates ({arrivalDate} to {chekoutDate})
- Mix of budget, mid-range, and luxury hotels
- Realistic ratings between 2.0 and 5.0
- Different price points based on hotel category
- Seasonal pricing considerations

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
                hotel_data = json.loads(response['response'])
                
                # Ensure it's a list and validate structure
                if isinstance(hotel_data, list):
                    # Validate each hotel has required fields
                    validated_hotels = []
                    validation_errors = []
                    
                    for i, hotel in enumerate(hotel_data):
                        if _validate_hotel_schema(hotel):
                            validated_hotels.append(hotel)
                        else:
                            validation_errors.append(f"Hotel {i+1} has invalid schema")
                    
                    if validated_hotels:
                        return {
                            "hotels": validated_hotels,
                            "errors": validation_errors if validation_errors else []
                        }
                    else:
                        logger.warning("LLM returned hotels with invalid schema, using fallback")
                        return _generate_fallback_hotels(country, state, city, arrivalDate, chekoutDate)
                else:
                    logger.warning("LLM returned non-array response, using fallback")
                    return _generate_fallback_hotels(country, state, city, arrivalDate, chekoutDate)
                    
            except json.JSONDecodeError:
                logger.warning("LLM returned invalid JSON, using fallback data")
                return _generate_fallback_hotels(country, state, city, arrivalDate, chekoutDate)
        else:
            logger.warning("LLM service unavailable, using fallback data")
            return _generate_fallback_hotels(country, state, city, arrivalDate, chekoutDate)
            
    except ImportError:
        logger.warning("LLM service not available")
        return {
            "hotels": [],
            "errors": ["No services available at the moment"]
        }
    except Exception as e:
        logger.error(f"Error in hotel search: {e}")
        return {
            "hotels": [],
            "errors": ["No services available at the moment"]
        }


def _validate_hotel_schema(hotel):
    """Validate that a hotel object matches the required schema"""
    required_fields = ["hotel", "address", "arrivalDate", "chekoutDate", "price", "rating"]
    
    if not isinstance(hotel, dict):
        return False
        
    for field in required_fields:
        if field not in hotel:
            return False
            
    # Additional type validation
    if not isinstance(hotel["price"], (int, float)):
        return False
        
    if not isinstance(hotel["rating"], (int, float)):
        return False
        
    # Validate rating range
    if not (0.0 <= hotel["rating"] <= 5.0):
        return False
        
    return True


def _generate_fallback_hotels(country, state, city, arrivalDate, chekoutDate):
    """Generate realistic fallback hotel data when LLM is unavailable"""
    
    # Ensure we have all required parameters
    if not all([country, state, city, arrivalDate, chekoutDate]):
        missing_params = []
        if not country: missing_params.append("country")
        if not state: missing_params.append("state")
        if not city: missing_params.append("city")
        if not arrivalDate: missing_params.append("arrivalDate")
        if not chekoutDate: missing_params.append("chekoutDate")
        
        return {
            "hotels": [],
            "errors": [f"Missing required parameters: {', '.join(missing_params)}"]
        }
    
    hotel_types = [
        ("Grand", "Hotel", 4.0, 4.8, 200, 500),
        ("Comfort", "Inn", 3.0, 4.2, 80, 180),
        ("Budget", "Lodge", 2.5, 3.8, 50, 120),
        ("Luxury", "Resort", 4.5, 5.0, 300, 800),
        ("Business", "Suites", 3.8, 4.5, 150, 300),
        ("Boutique", "Hotel", 4.2, 4.7, 180, 350)
    ]
    
    hotels = []
    errors = []
    
    try:
        for i in range(4):
            hotel_type = random.choice(hotel_types)
            prefix, suffix, min_rating, max_rating, min_price, max_price = hotel_type
            
            # Generate hotel name
            hotel_name = f"{prefix} {city} {suffix}"
            
            # Generate address
            street_number = random.randint(100, 9999)
            street_names = ["Main Street", "Downtown Ave", "Central Plaza", "Park Boulevard", "Hotel District"]
            street = random.choice(street_names)
            address = f"{street_number} {street}, {city}, {state}, {country}"
            
            # Generate realistic price and rating
            price = round(random.uniform(min_price, max_price), 2)
            rating = round(random.uniform(min_rating, max_rating), 1)
            
            hotel = {
                "hotel": hotel_name,
                "address": address,
                "arrivalDate": arrivalDate,
                "chekoutDate": chekoutDate,
                "price": price,
                "rating": rating
            }
            hotels.append(hotel)
        
        # Add a warning that this is fallback data
        errors.append("LLM service unavailable - using generated hotel data")
        
    except Exception as e:
        logger.error(f"Error generating fallback hotels: {e}")
        errors.append("Error generating hotel options")
    
    return {
        "hotels": hotels,
        "errors": errors
    }
