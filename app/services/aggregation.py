import logging
from .dining import find_dining_options
from .flights import find_flights_by_criteria
from .hotels import find_hotels_by_criteria
from .transportation import find_transportation_options

logger = logging.getLogger(__name__)

def get_service_results(service, params):
    """
    Calls the appropriate service based on the 'service' parameter and merges results.
    Returns a dictionary in the desired format.
    """
    try:
        if service == 'dining':
            return find_dining_options(**params)  # Unpack parameters as keyword arguments
        elif service == 'flights':
            return find_flights_by_criteria(**params)
        elif service == 'transportation':
            return find_transportation_options(**params)
        elif service == 'hotels':
            return find_hotels_by_criteria(**params)
        else:
            raise ValueError("Invalid service type")
    except Exception as e:
        logger.error(f"Error in {service} service: {e}")
        # Return appropriate error format based on service
        if service == 'flights':
            return {"flights": [], "errors": [f"Error in {service} service: {str(e)}"]}
        elif service == 'hotels':
            return {"hotels": [], "errors": [f"Error in {service} service: {str(e)}"]}
        elif service == 'transportation':
            return {"transportation": [], "errors": [f"Error in {service} service: {str(e)}"]}
        else:  # dining
            return {"error": f"Error in {service} service: {str(e)}"}


def aggregate_results(dining_params, flight_params, hotel_params, transportation_params):
    """
    Aggregates results from all services into the desired format.
    Handles errors gracefully and ensures consistent response format.
    """
    
    # Initialize results with default error handling
    dining_results = {"error": "No dining parameters provided"}
    flight_results = {"flights": [], "errors": ["No flight parameters provided"]}
    hotel_results = {"hotels": [], "errors": ["No hotel parameters provided"]}
    transportation_results = {"transportation": [], "errors": ["No transportation parameters provided"]}
    
    # Get dining results if parameters provided
    if dining_params:
        try:
            dining_results = find_dining_options(**dining_params)
        except Exception as e:
            logger.error(f"Error in dining service: {e}")
            dining_results = {"error": f"Error in dining service: {str(e)}"}
    
    # Get flight results if parameters provided
    if flight_params:
        try:
            flight_results = find_flights_by_criteria(**flight_params)
        except Exception as e:
            logger.error(f"Error in flights service: {e}")
            flight_results = {"flights": [], "errors": [f"Error in flights service: {str(e)}"]}
    
    # Get hotel results if parameters provided
    if hotel_params:
        try:
            hotel_results = find_hotels_by_criteria(**hotel_params)
        except Exception as e:
            logger.error(f"Error in hotels service: {e}")
            hotel_results = {"hotels": [], "errors": [f"Error in hotels service: {str(e)}"]}
    
    # Get transportation results if parameters provided
    if transportation_params:
        try:
            transportation_results = find_transportation_options(**transportation_params)
        except Exception as e:
            logger.error(f"Error in transportation service: {e}")
            transportation_results = {"transportation": [], "errors": [f"Error in transportation service: {str(e)}"]}

    aggregated_data = {
        "diningResults": dining_results,
        "flightResults": flight_results,
        "hotelResults": hotel_results,
        "transportationResults": transportation_results,
    }
    return aggregated_data
