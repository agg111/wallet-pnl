from flask import Flask, jsonify
import database_manager
from database_manager import initialize_firebase

app = Flask(__name__)

# Visualization API
@app.route('/api/wallet_pnl', methods=['GET'])
def wallet_pnl_endpoint():
    # Assuming wallet_activity and token_hourly_data are defined globally or fetched from a database
    db = initialize_firebase()
    wallet_pnl_stream = database_manager.get_collection(db, "wallet_pnl")
    wallet_pnl = [doc.to_dict() for doc in wallet_pnl_stream]
    print(type(wallet_pnl))
    return jsonify(wallet_pnl)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
