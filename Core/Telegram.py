import threading

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)

class CommandCall:
	def __init__(self, cmd, ret):
		self.cmd = cmd
		self.ret = ret

	def __call__(self, bot, update, args=None):
		if type(self.ret) is str:
			text = self.ret
		elif args is None:
			text = self.ret(update)
		else:
			text = self.ret(update, args)
		bot.sendMessage(chat_id=update.message.chat_id, text=text)

class Telegram(threading.Thread):
	"""connect to Telegram"""
	def __init__(self, token):
		threading.Thread.__init__(self)
		self.updater = Updater(token=token)
		self.dispatcher = self.updater.dispatcher
		self.text_message = None
		self.unknown_command = "Ummm... This command not found."
		self._first = True

	def __exit__(self):
		self.Stop()

	def Command(self, command, func, pass_args=False):
		handler = CommandHandler(command, CommandCall(command, func), pass_args=pass_args)
		self.dispatcher.add_handler(handler)

	def run(self):
		if self._first:
			self.dispatcher.add_handler(MessageHandler(Filters.text, self.got_text))
			self.dispatcher.add_handler(MessageHandler(Filters.command, self.Unknown))
			self._first = False
		self.updater.start_polling()

	def stop(self):
		self.updater.stop()

	def Unknown(self, bot, update):
		bot.sendMessage(chat_id=update.message.chat_id, text=self.unknown_command)

	def got_text(self, bot, update):
		if self.text_message is not None:
			text = self.text_message(update.message.chat_id, update.message.text)
		else:
			text = "Ummm... This bot no reply feature."
		bot.sendMessage(chat_id=update.message.chat_id, text=text)

	def Send(self, id, msg):
		echo_handler = MessageHandler(Filters.text, echo)
		dispatcher.add_handler(echo_handler)