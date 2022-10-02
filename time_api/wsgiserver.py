from flask import Flask,request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wsgiref.simple_server import make_server
from werkzeug.middleware.proxy_fix import ProxyFix

from mcdreforged.api.decorator import new_thread

from time_api import constants

import json

app = Flask(__name__)
CORS(app, resources=r'/*')

limiter = Limiter(
	app,
	key_func = get_remote_address,
	default_limits = ["6 per minute"]
)

@app.route('/')
def hello_world():
	try:
		with open(constants.configPath, 'r') as json_file:
			ret = json.load(json_file)
	except Exception as ex:
		ret = "ERROR File Not Found"
		ret = ret + str(ex)

	print(ret)

	return ret

def makesvr(config):
	global webserver
	app.wsgi_app = ProxyFix(app.wsgi_app)
	webserver = make_server('', config.serverPort, app)

@new_thread
def start_webserver():
	webserver.serve_forever()