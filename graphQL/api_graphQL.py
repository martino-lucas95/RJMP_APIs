from flask import Flask, jsonify, request
from ariadne import QueryType, make_executable_schema, graphql_sync, MutationType
from flask import request, jsonify
import json

app = Flask(__name__)

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not data:  
                return []
            return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file_path}.")
        return []


def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

POSSIBLE_INVESTMENTS_FILE = "graphQL/possible_investments.json"
USER_INVESTMENTS_FILE = "graphQL/user_investments.json"

# Cargar datos desde los archivos JSON
possible_investments = load_json(POSSIBLE_INVESTMENTS_FILE)
user_investments = load_json(USER_INVESTMENTS_FILE)

type_defs = """
    type Query {
        possibleInvestments: [Investment!]!
        userInvestments(accountId: ID!): [UserInvestment!]!
    }

    type Mutation {
        addUserInvestment(accountId: ID!, investmentId: ID!, amount: Float!): UserInvestment!
    }

    type Investment {
        id: ID!
        name: String!
        return_rate: Float!
    }

    type UserInvestment {
    id: ID!
    name: String!
    amount: Float!
    return_rate: Float!
}
"""

query = QueryType()
mutation = MutationType()

@query.field("possibleInvestments")
def resolve_possible_investments(_, info):
    possible_investments = load_json(POSSIBLE_INVESTMENTS_FILE)
    return possible_investments

@query.field("userInvestments")
def resolve_user_investments(_, info, accountId):
    user_investments_list = user_investments.get(accountId, [])
    
    if not isinstance(user_investments_list, list):
        return []
    
    enriched_investments = []
    for investment in user_investments_list:
        investment_detail = next(
            (inv for inv in possible_investments if inv["id"] == investment["id"]),
            None
        )
        if investment_detail:
            enriched_investment = {
                "id": investment["id"],
                "name": investment["name"],
                "amount": investment["amount"],
                "return_rate": float(investment_detail["return_rate"]),
            }
            enriched_investments.append(enriched_investment)

    return enriched_investments

@mutation.field("addUserInvestment")
def resolve_add_user_investment(_, info, accountId, investmentId, amount):
    investment_detail = next(
        (inv for inv in possible_investments if inv["id"] == int(investmentId)),
        None
    )
    
    if not investment_detail:
        raise Exception(f"Inversión con ID {investmentId} no encontrada.")
    
    new_investment = {
        "id": investmentId,
        "name": investment_detail["name"],
        "amount": amount
    }

    if accountId in user_investments:
        user_investments[accountId].append(new_investment)
    else:
        user_investments[accountId] = [new_investment]

    save_json(USER_INVESTMENTS_FILE, user_investments)

    return {
        "id": investmentId,
        "name": investment_detail["name"],
        "amount": amount,
        "return_rate": float(investment_detail["return_rate"])
    }


schema = make_executable_schema(type_defs, query, mutation)



@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return """
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset=utf-8/>
        <title>GraphQL Playground</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
        <link rel="shortcut icon" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png" />
        <script src="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
    </head>

    <body>
        <style>
            body {
                height: 100%;
                width: 100%;
                margin: 0;
                overflow: hidden;
            }
            #root {
                height: 100%;
                width: 100%;
            }
        </style>
        <div id="root"></div>
        <script>
            window.addEventListener('load', function (event) {
                const root = document.getElementById('root');
                GraphQLPlayground.init(root, {
                    endpoint: '/graphql'
                });
            });
        </script>
    </body>

    </html>
    """, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route('/AndisBank')
def home():
    return jsonify({"message": "Welcome"})

if __name__ == '__main__':
    app.run(debug=True)
