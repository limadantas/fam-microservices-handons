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

@app.route('/posts', methods=['GET'])
def list_posts ():
    return jsonify(execute_query("SELECT * FROM posts"))

@app.route('/posts/<post_id>', methods=['GET'])
def get_post_by_id (post_id):
    return jsonify(execute_query(f"SELECT * FROM posts WHERE post_id={post_id}")[0])

@app.route('/posts', methods=['POST'])
def create_post ():
    data    = request.get_json()

    columns = ", ".join(data.keys())
    values = list (map(lambda v: f"'{v}'", data.values()))
    values  = ", ".join(values)

    execute_update(f"""
        INSERT INTO posts ({columns})
        VALUES ({values})
    """), 201
    return jsonify(data)


@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post (post_id):
    return jsonify(execute_query(f"DELETE FROM posts WHERE post_id={post_id}"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

