from flask import Flask, request, jsonify, Blueprint
from .services.flights import find_flights_by_criteria
from .services.transportation import find_transportation_options
from .services.hotels import find_hotels_by_criteria
from .services.aggregation import aggregate_results
from .services.dining import find_dining_options

travel_bp = Blueprint('travel', __name__)

app = Flask(__name__)

@app.route('/api/dining', methods=['GET'])
def get_dining_options():
    budget = request.args.get('budget')
    timeframe = request.args.get('timeframe')
    location = request.args.get('location')

    if not all([budget, timeframe, location]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        dining_options = find_dining_options(budget, timeframe, location)
        return jsonify(dining_options)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/flights', methods=['GET'])
def get_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')

    if not all([origin, destination, date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        flights = find_flights_by_criteria(origin, destination, date)
        return jsonify(flights)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/transportation', methods=['GET'])
def get_transportation():
    type = request.args.get('type')  # e.g., 'bus', 'train'
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not all([type, origin, destination]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        transportation_options = find_transportation_options(type, origin, destination)
        return jsonify(transportation_options)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/hotels', methods=['GET'])
def get_hotels():
    location = request.args.get('location')
    checkin_date = request.args.get('checkin_date')
    checkout_date = request.args.get('checkout_date')

    if not all([location, checkin_date, checkout_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        hotels = find_hotels_by_criteria(location, checkin_date, checkout_date)
        return jsonify(hotels)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@travel_bp.route('/aggregate', methods=['POST'])  # Or GET, depending on how you want to pass parameters
def aggregate():
    """
    Aggregates results from all services based on POSTed parameters.
    """
    try:
        data = request.get_json() # Get the JSON data sent in the request

        dining_params = data.get('dining_params', {})  # Get dining params, default to empty dict if not provided
        flight_params = data.get('flight_params', {})
        hotel_params = data.get('hotel_params', {})
        transportation_params = data.get('transportation_params', {})

        aggregated_data = aggregate_results(dining_params, flight_params, hotel_params, transportation_params) # Call the aggregation function

        return jsonify(aggregated_data)  # Return the aggregated data as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors and return a 500 status code


# Entry point to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
