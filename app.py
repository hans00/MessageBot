#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import logging
from Core.LINE import LINE
from Core.Telegram import Telegram

BOT_ID = {
	'Telegram': os.environ['TG_NAME'],
	'LINE': os.environ['LINE_NAME']
}

if 'LOG' in os.environ:
	logging.basicConfig(
		filename=os.environ['LOG'],
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.DEBUG
		)
else:
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.DEBUG
		)

tg = Telegram(os.environ['TG_TOKEN'])
line = LINE(os.environ['LINE_TOKEN'], os.environ['LINE_SECRET'])

def gotTextMessage(msg):
	if msg.Tagged(BOT_ID[msg.platform]):
		msg.Reply("Don't tag meeeee!!!!")
	elif msg.isGroup():
		msg.Reply("Ummm....")

def group(msg):
	msg.Reply("YES" if msg.isGroup() else "NO")

def etc(msg):
	msg.Reply("??")

def args(msg):
	if len(msg.args) == 0:
		msg.args = ['Nothing']
	msg.Reply("\n".join(msg.args))

tg.Command("start", "Hello!! ^.^")
line.Command("start", "Hello!! ^.^")
tg.Command("etc", etc)
line.Command("etc", etc)
tg.Command("args", args, pass_args=True)
line.Command("args", args, pass_args=True)
tg.Command("isgroup", group)
line.Command("isgroup", group)
tg.text_message = gotTextMessage
line.text_message = gotTextMessage

line.start()
tg.start()