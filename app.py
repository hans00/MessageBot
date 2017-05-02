#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import logging
from flask import Flask
from Core import (
	LINE,
	Telegram,
	DB,
	MessageProcess,
	Commands
)
from Features import Link

BOT_ID = {
	'Telegram': os.environ['TG_NAME'],
	'LINE': os.environ['LINE_NAME']
}

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO,
	**({'filename':os.environ['LOG']} if 'log' in os.environ else {})
	)

db = DB(os.environ["DATABASE_URL"])
app = Flask(__name__)

@app.route('/')
def index():
    return "<p>Hello World!</p>"

platforms = []

platforms.append(
	Telegram(app, os.environ['HTTP_HOST'],os.environ['TG_TOKEN'])
)

platforms.append(
	LINE(app, os.environ['LINE_TOKEN'], os.environ['LINE_SECRET'])
)

def TeggedMessage(msg):
	msg.Reply("OAO")

MessageProcess.set(
	lambda msg: msg.Tagged(BOT_ID[msg.platform]),
	TeggedMessage,
	from_type='user'
)

MessageProcess.set(
	lambda msg: msg.Tagged(BOT_ID[msg.platform]),
	TeggedMessage,
	from_type='group'
)

Link.cmds = Commands('link', platforms)
Link(db)
Link.group.Telegram = platforms[0]
Link.group.LINE = platforms[1]
MessageProcess.set(Link.group.check, Link.group.message, from_type='group')

def UnknownMessage(msg):
	msg.Reply("Bye... (?")

MessageProcess.set(
	lambda msg: 1,
	UnknownMessage,
	from_type='all',
	priority=2
)

for platform in platforms:
	platform.text_message = MessageProcess.process
	platform.Start()

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 33507)))
