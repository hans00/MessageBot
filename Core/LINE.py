import threading, os
from Message import Message
from flask import Flask, request, abort, Response
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage
)

from re import match as re_match

class LINE(threading.Thread):
	@staticmethod
	def get_key(event, message=None):
		if TextMessage is None:
			return event.__name__
		else:
			return event.__name__ + '_' + message.__name__

	def set_handler(self, callback, event, message=None):
		key = self.get_key(event, message=message)
		self.handler._handlers[key] = callback

	def __init__(self, api_token, secret, app='LINE', path='/callback', name='callback'):
		threading.Thread.__init__(self)
		if type(app) in (str, unicode):
			self.app = Flask(app)
			self.builtin_app = True
		else:
			self.app = app
			self.builtin_app = False
		self.app.add_url_rule(path, name, self.callback, methods=['POST'])
		self.bot_api = LineBotApi(api_token)
		self.handler = WebhookHandler(secret)
		self.set_handler(self.got_text, MessageEvent, message=TextMessage)
		self.text_message = None
		self.command_call = {}
		self.unknown_command = "Ummm... This command not found."
		self.text_message = "Umm... This bot no reply feature."
		self._stop = True

	def Command(self, command, func, pass_args = False):
		self.command_call[command] = {}
		self.command_call[command]['call'] = func
		self.command_call[command]['args'] = pass_args

	def run(self):
		self._stop = False
		if self.builtin_app:
			self.app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 33507)))

	def stop(self):
		self._stop = True

	def PushText(self, to, text):
		self.bot_api.push_message(to, TextSendMessage(text=text))

	def got_text(self, event):
		cmd = re_match( r'^\/(\w+)', event.message.text)
		if cmd:
			cmd = cmd.group(1)
			if cmd in self.command_call:
				if type(self.command_call[cmd]['call']) is str:
					text = self.command_call[cmd]['call']
					self.bot_api.reply_message(
							event.reply_token,
							TextSendMessage(text=text)
						)
				elif self.command_call[cmd]['args']:
					if ' ' in event.message.text:
						args = event.message.text.split()
						del args[0]
						msg = Message('LINE')
						msg.setEvent(bot=self.bot_api, event=event, args=args, type='command')
						self.command_call[cmd]['call'](msg)
					else:
						msg = Message('LINE')
						msg.setEvent(bot=self.bot_api, event=event, args=[], type='command')
						self.command_call[cmd]['call'](msg)
				else:
					msg = Message('LINE')
					msg.setEvent(bot=self.bot_api, event=event, type='command')
					self.command_call[cmd]['call'](msg)
			else:
				text = self.unknown_command
				self.bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text=text)
					)
		else:
			if type(self.text_message) in (str, unicode):
				self.bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text=self.text_message)
					)
			else:
				msg = Message('LINE')
				msg.setEvent(bot=bot_api, event=event, type='text')
				self.text_message(msg)

	def callback(self):
		if self._stop:
			abort(404)
			return '404'
		signature = request.headers['X-Line-Signature']
		body = request.get_data(as_text=True)
		self.app.logger.info("Request body: " + body)
		try:
			self.handler.handle(body, signature)
		except InvalidSignatureError:
			abort(400)
		return 'OK'
