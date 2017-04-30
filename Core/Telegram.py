import threading
from Message import Message
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)

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

class Telegram(threading.Thread):
	"""connect to Telegram"""
	def __init__(self, token):
		threading.Thread.__init__(self)
		self.updater = Updater(token=token)
		self.dispatcher = self.updater.dispatcher
		self.text_message = None
		self.unknown_command = "Ummm... This command not found."
		self.text_message = "Ummm... This bot no reply feature."
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
		if type(self.text_message) in (str, unicode):
			bot.sendMessage(chat_id=update.message.chat_id, text=self.text_message)
		else:
			msg = Message('Telegram')
			msg.setEvent(bot=bot, update=update, type='text')
			self.text_message(msg)
