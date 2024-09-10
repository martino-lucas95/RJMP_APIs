from flask import Flask, jsonify, request
import json

app = Flask(__name__)

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
def home():
    return jsonify({"message": "Welcome"})

@app.route('/AndisBank/investments/<account_id>', methods=['GET'])
def get_investments_by_account(account_id):
    investments = user_investments.get(account_id, [])
    return jsonify({"account_id": account_id, "investments": investments})


@app.route('/AndisBank/investments', methods=['GET'])
def get_investments():
    return jsonify({"possible_investments": possible_investments})


@app.route('/AndisBank/investments/<account_id>', methods=['POST'])
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
