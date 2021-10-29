from flask import Flask, jsonify, request
from config import username, password
from git import Repo
from models import Repository
app = Flask(__name__)


@app.route('/register')
def register():
    name = request.json.get('name', -1)
    _token = request.json.get('token', -1)


    if name == -1 or _token == -1:
        return jsonify({'error': 'name or token not found'}), 400

    if _token != "asdwsadfgjnrkfu349re312_123!$dsaeewtghjjfncxmxdurentmykdsienjewqewq":
        return jsonify({'error': 'invalid token'}), 401

    full_local_path = "/var/www/{name}"

    try:
        remote = f"https://{username}:{password}@github.com/Paymona/{name}.git"
        Repo.clone_from(remote, full_local_path)
        
    except Exception as e:
        return jsonify({'error': str(e)})

    repo = Repository(
        path = full_local_path,
    )

    return jsonify({
        "msg" : "Successifully cloned",
        "code" : repo.code,
    })

@app.route('/register_domain')
def register_domain():
    _domain = request.json.get('domain', -1)
