import logging
from Message import Message
from flask import request, abort
import telegram
from telegram.ext import (
	Dispatcher,
	CommandHandler,
	MessageHandler,
	Filters
)

class CommandCall:
	def __init__(self, cmd, ret):
		self.cmd = cmd
		self.ret = ret

	def __call__(self, bot, update, args=None):
		if type(self.ret) is str:
			text = self.ret
			bot.sendMessage(chat_id=update.message.chat_id, text=text)
		else:
			msg = Message('Telegram')
			msg.setEvent(bot=bot, update=update, args=args, type='command')
			self.ret(msg)

class Telegram(object):
	"""connect to Telegram"""
	def __init__(self, app, host, token, cert=None, port='443', name='tg_callback'):
		self.app = app
		self.app.add_url_rule('/'+token, name, self.callback, methods=['POST'])
		self.bot = telegram.Bot(token)
		self.bot.setWebhook(webhook_url='https://%s:%s/%s' % (host, port, token),
			**({'certificate':open(cert, 'rb')} if cert is not None else {}))
		self.dispatcher = Dispatcher(self.bot, None, workers=0)
		self.unknown_command_text = "Ummm... This command not found."
		self.text_message = "Ummm... This bot no reply feature."
		self._stop = True
		self._inited = False

	def __exit__(self):
		self.stop()

	def callback(self):
		if self._stop:
			abort(404)
		update = telegram.update.Update.de_json(request.get_json(force=True), self.bot)
		logging.debug(update)
		self.dispatcher.process_update(update)
		return 'OK'

	def Command(self, command, func, pass_args=False):
		handler = CommandHandler(command, CommandCall(command, func), pass_args=pass_args)
		self.dispatcher.add_handler(handler)

	def Start(self):
		if not self._inited:
			self.dispatcher.add_handler(MessageHandler(Filters.text, self.got_text))
			self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown_command))
			self._inited = True
		self._stop = False

	def Stop(self):
		self._stop = True

	def unknown_command(self, bot, update):
		update.message.reply_text(self.unknown_command_text)

	def got_text(self, bot, update):
		if type(self.text_message) in (str, unicode):
			if update.message.chat.type not in ('supergroup', 'group'):
				bot.sendMessage(chat_id=update.message.chat_id, text=self.text_message)
		else:
			msg = Message('Telegram')
			msg.setEvent(bot=bot, update=update, type='text')
			self.text_message(msg)

	def Push(self, to, data, type='text'):
		if type == 'text':
			self.bot.sendMessage(chat_id=to, text=data)
