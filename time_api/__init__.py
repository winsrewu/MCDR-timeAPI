from mcdreforged.api.all import *

import datetime
import re
import json
import time
import os

from time_api.wsgiserver import *
from time_api.config import Config
from time_api.constants import *

config: Config

firstFlag = True

def on_load(server, prev):
	global firstFlag

	server.logger.info('Time Api onload')
	config = server.load_config_simple(target_class = Config)

	if firstFlag:
		firstFlag = False
		makesvr(config)

	if prev is not None:
		get_time(server)

	register_command(server)

def on_server_startup(server):
	waitForRcon(server)
	start_webserver()

def get_time(server):
	now_time = datetime.datetime.now().strftime('%F %T')
	day = 0
	daytime = 0

	l = []

	try:
		l = re.findall("\d+", str(server.rcon_query(command = 'time query day') + server.rcon_query(command = 'time query daytime')))
	except:
		day = 0
		daytime = 0

	try:
		day = int(l[0])
		daytime = int(l[1])
	except:
		server.logger.info('Time Api ERROR. Something wrong in executing command \'time query day \' or \'time query daytime\' with rcon')

	server.logger.info('Time get: ' + str(day) + ' : ' + str(daytime))

	data = {}
	data['realTime'] = now_time
	data['day'] = day
	data['daytime'] = daytime

	with open(configPath, 'w') as json_file:
		json.dump(data, json_file)

@new_thread
def waitForRcon(server):
	time.sleep(60)
	get_time(server)

#command

def regetTime(source: CommandSource):
	if source.get_server().get_permission_level(obj = source) >= 2:
		get_time(source.get_server())
		source.reply("Time reget.")
	else:
		source.reply("No permission")

def startServer(source: CommandSource):
	if source.get_server().get_permission_level(obj = source) >= 2:
		try:
			replyStr = start_webserver()
			waitForRcon(source.get_server())
			source.reply("Start Server. Time will be got in 60s.")
			source.reply(replyStr)
		except Exception as ex:
			source.reply("Error while starting server\n" + str(ex))

	else:
		source.reply("No permission")

def getInfo(source: CommandSource):
	if source.get_server().get_permission_level(obj = source) >= 2:
		with open(constants.configPath, 'r') as json_file:
			ret = json.load(json_file)
		source.reply(ret)
	else:
		source.reply("No permission")


def showHelp(source: CommandSource):
	help_msg_rtext = constants.helpMsg
	source.reply(help_msg_rtext)

def register_command(server: PluginServerInterface):
	server.register_command(
		#help
		Literal(preFix).
		runs(showHelp).

		#reget
		then(
			Literal('reget').
			runs(regetTime)
		).

		#startServer
		then(
			Literal('startServer').
			runs(startServer)
		).

		#Info
		then(
			Literal('info').
			runs(getInfo)
		)
	)