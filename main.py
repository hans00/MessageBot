#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import logging
from Core.LINE import LINE
from Core.Telegram import Telegram

logging.basicConfig(
	filename=os.environ['LOG'],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.DEBUG
	)

tg = Telegram(os.environ['TG_TOKEN'])
line = LINE(os.environ['LINE_TOKEN'], os.environ['LINE_SECRET'])

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

line.start()
tg.start()