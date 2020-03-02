from flask import Flask, jsonify

from client import RPCClient
from config import conf

from thrifts.user_service import UserService
cli = RPCClient(conf.zookeeper.hosts)
cli.bind('User', UserService)

app = Flask(__name__)


@app.route('/')
def index():
    with cli.User as user_service:
        r = user_service.Ping()
    return jsonify(code=r.code)


app.run()