#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Core.LINE import LINE
from Core.Telegram import Telegram

tg = Telegram("TOKEN")
line = LINE("TOKEN", "SECRET")

def etc(event):
	print(event)
	return "??"

def args(event, args):
	if len(args) == 0:
		args = ['Nothing']
	return "\n".join(args)

tg.Command("start", "Hello!! ^.^")
line.Command("start", "Hello!! ^.^")
tg.Command("etc", etc)
line.Command("etc", etc)
tg.Command("args", args, pass_args=True)
line.Command("args", args, pass_args=True)

line.start()
tg.start()
tg.updater.idle()