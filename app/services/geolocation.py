import requests
from os import environ
from flask import jsonify

def find_geolocation(address):

    try:
        if address is None:
            return jsonify({'error': 'Invalid address'}), 400

        apiKey = environ.get('GOOGLE_API_KEY')

        if apiKey is None:
            return jsonify({'error': 'Invalid address'}), 400

        # Construct the external URL (replace with your target URL)
        external_url = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={apiKey}}"  # Replace this!

        # Send a POST request to the external URL
        response = requests.get(external_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        formatted_address = data['results'][0]['formatted_address']
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']

        address_data = {
            "formatted_address": formatted_address,
            "lat": lat,
            "lng": lng
        }


        if response.status_code == 200:
            return address_data, 200  # OK
        else:
            return jsonify({'status': 'error', 'message': f"External URL failed with status {response.status_code}, response: {response.text}"}), response.status_code # Return error details


    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the external request: {e}")  # Log the error
        return jsonify({'error': 'External request failed'}), 500  # Internal Server Error

    except Exception as e:
         print(f"An unexpected error occurred: {e}")
         return jsonify({'error': 'Internal Server Error'}), 500
    
    # Extract relevant information (name, price, rating)
    #dining_options = []
    #for restaurant in soup.find_all('div', class_='restaurant'): # Example class
    #    name = restaurant.find('h2').text
    #    price = restaurant.find('span', class_='price').text
    #    rating = restaurant.find('i', class_='rating').text
    #    dining_options.append({'name': name, 'price': price, 'rating': rating})