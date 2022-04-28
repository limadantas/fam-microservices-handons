from hashlib import md5
import os
from sqlalchemy import create_engine
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def execute_query (query_string):
    uri = os.environ['DATABASE_URL']
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    print(uri)
    engine = create_engine(uri, echo = False)
    # run a quick test
    result = engine.execute(query_string).fetchall()
    result = [ dict(r) for r in result ]
    return result

def execute_update (query_string):
    uri = os.environ['DATABASE_URL']
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    print(uri)
    engine = create_engine(uri, echo = False)
    # run a quick test 
    engine.execute(query_string)

@app.route('/accounts', methods=['GET'])
def list_accounts ():
    return jsonify(execute_query("SELECT * FROM accounts"))

@app.route('/accounts/users/<user_id>', methods=['GET'])
def get_account_by_user_id (user_id):
    return jsonify(execute_query(f"SELECT * FROM accounts WHERE user_id={user_id}")[0])

@app.route('/accounts/users/name/<username>', methods=['GET'])
def get_account_by_username (username):
    return jsonify(execute_query(f"SELECT * FROM accounts WHERE username='{username}'")[0])

@app.route('/accounts', methods=['POST'])
def sing_up ():
    data    = request.get_json()
    data["password"] = md5(data["password"].encode()).hexdigest() # Criptografando a senha para guardar

    columns = ", ".join(data.keys())
    values = list (map(lambda v: f"'{v}'", data.values()))
    values  = ", ".join(values)
    
    data.pop("password")

    execute_update(f"""
        INSERT INTO accounts ({columns})
        VALUES ({values})
    """), 201
    return jsonify(data)

@app.route('/accounts/authenticate', methods=['POST'])
def authenticate ():
    data             = request.get_json()
    username         = data["username"]

    accounts = execute_query(f"SELECT * FROM accounts WHERE username = '{username}'")

    if (accounts):
        account = accounts[0]
        if account["password"] == md5(data["password"].encode()).hexdigest():
            return jsonify({ "valid": True })
    
    return jsonify({ "valid": False })


@app.route('/accounts/users/name/<username>', methods=['DELETE'])
def delete_account (username):
    return jsonify(execute_query(f"DELETE FROM accounts WHERE username='{username}'"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

