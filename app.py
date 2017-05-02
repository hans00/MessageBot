#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import logging
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

if 'LOG' in os.environ:
	logging.basicConfig(
		filename=os.environ['LOG'],
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO
		)
else:
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO
		)

db = DB(os.environ["DATABASE_URL"])

def UnknownMessage(msg):
	msg.Reply("Bye... (?")

def TeggedMessage(msg):
	msg.Reply("OAO")

platforms = []
platforms.append(
	Telegram(os.environ['TG_TOKEN'])
)
platforms.append(
	LINE(os.environ['LINE_TOKEN'], os.environ['LINE_SECRET'])
)

Link.cmds = Commands('link', platforms)
Link(db)
Link.group.Telegram = platforms[0]
Link.group.LINE = platforms[1]
MessageProcess.set(Link.group.check, Link.group.message, from_type='group')

MessageProcess.set(
	lambda msg: msg.Tagged(BOT_ID[msg.platform]),
	TeggedMessage,
	from_type='user'
)

MessageProcess.set(
	lambda msg: msg.Tagged(BOT_ID[msg.platform]),
	TeggedMessage,
	from_type='group',
	priority=1
)

MessageProcess.set(
	lambda msg: 1,
	UnknownMessage,
	from_type='all',
	priority=2
)

for platform in platforms:
	platform.text_message = MessageProcess.process
	platform.start()