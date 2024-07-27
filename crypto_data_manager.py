import requests
import os

API_KEY = os.getenv('COINGECKO_API_KEY')

def fetch_coin_data():
    if not API_KEY:
        raise ValueError("No API key provided. Set the COINGECKO_API_KEY environment variable.")

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 3,
        'page': 1
    }
    headers = {
        'accept': 'application/json',
        'x-cg-api-key': API_KEY
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()

def fetch_hourly_prices(coins, start_time, end_time):
    params = {
        'from': start_time,
        'to': end_time,
        'vs_currency': 'usd',
    }
    headers = {
        'accept': 'application/json',
        'x-cg-api-key': API_KEY
    }
    hourly_data = []
    for coin in coins:
        data = {}
        url = f"https://api.coingecko.com/api/v3/coins/{coin.id}/market_chart/range"
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data["id"] = coin.id
        data['timestamps'] = []
        data['prices'] = []
        for p in list(response.json()['prices']):
            data['timestamps'].append(p[0])
            data['prices'].append(p[1])
        hourly_data.append(data)

    return hourly_data

def extract_fields(data):
    fields = []
    for entry in data:
        field = {}
        field['id'] = entry['id']
        field['name'] = entry['name']
        field['current_price'] = entry['current_price']
        field['market_cap'] = entry['market_cap']
        fields.append(field)
    return fields
