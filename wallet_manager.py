import requests
import json
import logging
from datetime import datetime

# API endpoint and API key
url = 'https://api.allium.so/api/v1/explorer/queries/UWHFUe3BPTFpd7EDVIiI/run'
api_key = '5jwLBV9oVitGnSfkGl6rp5hhJzDbBvoKa-4KllVq5L4CoxfIv_-AT8jrNblF16YhXBKiZkdqzG16ZZSZW4m8CA'
address = '0x26a016De7Db2A9e449Fe5b6D13190558d6bBCd5F'

# Request headers and payload
headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': api_key
}
payload = {
    'address': address
}

def call_api(url, headers, payload):
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()

def process_response(data):
    wallet_activity = []
    if 'data' in data:
        for record in data['data']:
            activity = {
                'token_address': record.get('token_address', 'N/A'),
                'balance': record.get('balance', 'N/A'),
                'block_timestamp': record.get('block_timestamp', 'N/A'),
                'token_id': record.get('token_id', 'N/A')
            }
            wallet_activity.append(activity)
        wallet_activity.sort(key=lambda x: datetime.fromisoformat(x['block_timestamp']))
    else:
        logging.warning("No data found in the response")
        
    return wallet_activity

def get_wallet_activity():
    try:
        response_data = call_api(url, headers, payload)
        return process_response(response_data)
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return None


def get_pnl(wallet_activity, token_hourly_data):
    wallet_pnl = []
    wallet_iter = 0
    starting_worth = 0
    current_balance = 0

    for i in range(len(token_hourly_data['prices'])):
        price = token_hourly_data['prices'][i]
        timestamp = token_hourly_data['timestamps'][i]
        pnl = {}

        next_timestamp = token_hourly_data['timestamps'][i + 1] if i + 1 < len(token_hourly_data['timestamps']) else float('inf')

        # Process all wallet activities within the current hourly interval
        while wallet_iter < len(wallet_activity) and wallet_activity[wallet_iter]['r_timestamp'] < next_timestamp:
            wallet = wallet_activity[wallet_iter]
            if wallet['r_timestamp'] <= timestamp:
                current_balance = wallet["balance"]

                if starting_worth == 0:
                    starting_worth = current_balance * price
            wallet_iter += 1

        # Calculate current worth and PnL
        current_worth = current_balance * price
        pnl["worth"] = current_worth
        pnl["pnl"] = current_worth - starting_worth
        pnl["id"] = str(timestamp)
    
        wallet_pnl.append(pnl)

    return wallet_pnl
