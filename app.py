from flask import Flask, jsonify, request
from config import username, password
from git import Repo
from models import Repository
import nginx
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

@app.route('/register_react')
def register_domain():
    _domain = request.json.get('domain', -1)
    _code = request.json.get('code', -1)
    if _code == -1 or _domain == -1:
        return jsonify(msg="Missing Something"), 400
    
    try:
        repo_query = Repo.get(Repo.code == _code)
    except:
        return jsonify(msg="Project Not Found")

    c = nginx.Conf()
    s = nginx.Server()
    s.add(
            nginx.Key('listen', '80'),
            nginx.Comment("Automated nginx conf from webhook"),
            nginx.Key('server_name', f"{_domain} www.{_domain}"),
            nginx.Key('root', repo_query.path),
            nginx.Key('index', "index.html index.htm index.nginx-debian.html"),
            nginx.Location("/",
                nginx.Key("try_files", "$uri $uri/ =404")
            )
    )
    c.add(s)
    nginx.dumpf(c, f'/etc/nginx/sites-available/{_domain}')


if __name__ == '__main__':
    app.run(port=5001)
