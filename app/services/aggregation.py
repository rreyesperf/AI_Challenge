from .dining import find_dining_options
from .flights import find_flights_by_criteria
from .hotels import find_hotels_by_criteria
from .transportation import find_transportation_options


def get_service_results(service, params):
    """
    Calls the appropriate service based on the 'service' parameter and merges results.
    Returns a dictionary in the desired format.
    """
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


def aggregate_results(dining_params, flight_params, hotel_params, transportation_params):
    """
    Aggregates results from all services into the desired format.
    """

    dining_results = find_dining_options(**dining_params)
    flight_results = find_flights_by_criteria(**flight_params)
    hotel_results = find_hotels_by_criteria(**hotel_params)
    transportation_results = find_transportation_options(**transportation_params)

    aggregated_data = {
        "diningResults": dining_results,
        "flightResults": flight_results,
        "hotelResults": hotel_results,
        "transportationResults": transportation_results,
    }
    return aggregated_data
