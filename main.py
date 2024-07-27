import crypto_data_manager
import database_manager
import wallet_manager
import utils

from datetime import datetime, timedelta
import time

CRYPTO_MARKET_COLLECTION = "crypto_markets"
HOURLY_DATA_COLLECTION = "hourly_data"
WALLET_PNL_COLLECTION = "wallet_pnl"

def main():
    
    # Fetch the data from CoinGecko API
    crypto_data = crypto_data_manager.fetch_coin_data()
    
    coins_stream = crypto_data_manager.extract_fields(crypto_data)
    coins = list(coins_stream)
    
    db = database_manager.initialize_firebase()
    
    # Write data to Firebase Firestore
    database_manager.save(db, CRYPTO_MARKET_COLLECTION, coins)

    coins = database_manager.get_collection(db, CRYPTO_MARKET_COLLECTION)
    
    start_time = int(time.mktime((datetime.now() - timedelta(days=7)).timetuple()))
    end_time = int(time.mktime(datetime.now().timetuple()))

    hourly_data = crypto_data_manager.fetch_hourly_prices(coins, start_time, end_time)
    database_manager.save(db, HOURLY_DATA_COLLECTION, hourly_data)
    
    wallet_activity = wallet_manager.get_wallet_activity()
    # Randomly fetched timestamps within the range of last week mapped to the wallet
    timestamps = utils.pick_random_timestamps(start_time, end_time, len(wallet_activity))
    for activity, random_timestamp in zip(wallet_activity, timestamps):
        activity['r_timestamp'] = random_timestamp

    token_hourly_data = database_manager.get_hourly_data(db, HOURLY_DATA_COLLECTION, wallet_activity[0]['token_id'])
    
    wallet_pnl = wallet_manager.get_pnl(wallet_activity, token_hourly_data)
    database_manager.save(db, WALLET_PNL_COLLECTION, wallet_pnl)
    

if __name__ == "__main__":
    main()
