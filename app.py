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
from Features import (
	Link,
	Unlink
)
from DB import create_if_not_exists

BOT_ID = {
	'Telegram': os.environ['TG_NAME'],
	'LINE': os.environ['LINE_NAME']
}

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO,
	**({'filename':os.environ['LOG']} if 'LOG' in os.environ else {})
)

db = DB(os.environ["DATABASE_URL"])
create_if_not_exists(db())
app = Flask(__name__)

@app.route('/')
def index():
    return "<p>Hello World!</p>"

platforms = {}

platforms['Telegram'] = Telegram(app, os.environ['HTTP_HOST'],os.environ['TG_TOKEN'])

platforms['LINE'] = LINE(
	app,
	os.environ['LINE_TOKEN'],
	os.environ['LINE_SECRET'],
	**({'path':os.environ['LINE_PATH']} if 'LINE_PATH' in os.environ else {})
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

Link(
	Commands('link', platforms),
	db,
	**(platforms)
)
MessageProcess.set(Link.group.check, Link.group.message, from_type='group')

Link(
	Commands('unlink', platforms),
	db,
	**(platforms)
)

def UnknownMessage(msg):
	msg.Reply("Bye... (?")

MessageProcess.set(
	lambda msg: 1,
	UnknownMessage,
	from_type='all',
	priority=2
)

for key in platforms:
	platforms[key].text_message = MessageProcess.process
	platforms[key].Start()

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 33507)))
