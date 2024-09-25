from flask import Flask, jsonify, request
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import threading


app = Flask(__name__)

# Inicializar Flask-Limiter con la estrategia de IP
limiter = Limiter(
    get_remote_address,
    app=app,
    #strategy='fixed-window',  # Usar estrategia de ventana fija
    #strategy='moving-window',
    default_limits=["100 per day", "10 per minute"]  # Limite global
)

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not data:  
                return {}
            return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file_path}.")
        return {}


def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

POSSIBLE_INVESTMENTS_FILE = "possible_investments.json"
USER_INVESTMENTS_FILE = "user_investments.json"

# Cargar datos desde los archivos JSON
possible_investments = load_json(POSSIBLE_INVESTMENTS_FILE)
user_investments = load_json(USER_INVESTMENTS_FILE)




@app.route('/AndisBank')
@limiter.limit("5 per minute")
def home():
    return jsonify({"message": "Welcome"})

@app.route('/AndisBank/investments/<account_id>', methods=['GET'])
@limiter.limit("10 per second")
def get_investments_by_account(account_id):
    investments = user_investments.get(account_id, [])
    return jsonify({"account_id": account_id, "investments": investments})

# investments, fixed-window
# @app.route('/AndisBank/investments', methods=['GET'])
# @limiter.limit("1 per second")
# def get_investments():
#   return jsonify({"possible_investments": possible_investments})

# Semáforo controla la concurrencia (por ejemplo, 2 concurrencias)
concurrency_limit = threading.Semaphore(10)

# investments, concurrency
@app.route('/AndisBank/investments', methods=['GET'])
def get_investments():
    # Intentar adquirir el semáforo, si no se puede, devolver un error.
    if not concurrency_limit.acquire(blocking=False):
        return jsonify({"error": "Too many concurrent requests, try again later."}), 429
    
    try:
        return jsonify({"possible_investments": possible_investments})
    finally:
        # Liberar el semáforo
        concurrency_limit.release()


@app.route('/AndisBank/investments/<account_id>', methods=['POST'])
@limiter.limit("10 per minute")
def invest(account_id):
    data = request.json
    investment_id = data.get('investment_id')
    amount = data.get('amount')

    investment = next((inv for inv in possible_investments if inv["id"] == investment_id), None)
    if investment:
        new_investment = {"id": investment_id, "name": investment["name"], "amount": amount}
        if account_id in user_investments:
            user_investments[account_id].append(new_investment)
        else:
            user_investments[account_id] = [new_investment]
        
        save_json(USER_INVESTMENTS_FILE, user_investments)
        
        return jsonify({"message": f"Inversión realizada para la cuenta {account_id}!", "investment": new_investment}), 201
    else:
        return jsonify({"error": "Inversión no encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
