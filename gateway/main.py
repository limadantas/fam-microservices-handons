from hashlib import md5
import json
import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

accouts_url = os.environ['ACCOUNTS']
posts_url   = os.environ['POSTS']

def autenticate (user):
    headers = {
        'Content-Type': 'application/json'
    }
    payload_user = json.dumps(user)
    r            = requests.post(f"{accouts_url}/accounts/autenticate", headers=headers, data=payload_user)
    autenticate  = r.json()
    
    return autenticate['valid']

def get_user_id_by_username (username):
    user = requests.get(f"{accouts_url}/accounts/users/name/{username}").json()

    return user['user_id']

@app.route('/posts', methods=['GET'])
def list_posts ():
    posts = requests.get(f"{posts_url}/posts").json()
    return jsonify(posts)

@app.route('/posts/<post_id>', methods=['GET'])
def get_post_by_id (post_id):
    post = requests.get(f"{posts_url}/posts/{post_id}").json()
    return jsonify(post)

@app.route('/posts', methods=['POST'])
def create_post ():
    post    = request.get_json()
    user = {
        'username': request.headers.get("username"),
        'password': request.headers.get("password")
    }

    headers = {
        'Content-Type': 'application/json'
    }

    if autenticate(user):
        post['id_user'] = get_user_id_by_username (user['username'])
        payload_post    = json.dumps(post)
        posted          = requests.post(f"{posts_url}/posts", headers=headers, data=payload_post).json()
        return jsonify(posted), 201 # Postado com sucesso
    
    return jsonify({"error": "Invalid username or password."}), 403 # Proibida a postagem


@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post (post_id):
    user = {
        'username': request.headers.get("username"),
        'password': request.headers.get("password")
    }
    if autenticate(user):
        requests.delete(f"{posts_url}/posts/{post_id}")
        return jsonify({}), 204
    
    return jsonify({"error": "Invalid username or password."}), 403 # Proibida a remoção

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

