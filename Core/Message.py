from types import FunctionType
import logging, re
from linebot.models import (
	TextSendMessage
)

class MessageProcess(object):
	TODO = {
		"user": [
			[],
			[],
			[]
		],
		"group": [
			[],
			[],
			[]
		]
	}

	@staticmethod
	def set(detect, call, from_type='user', priority=0):
		if from_type not in ('user', 'group'):
			raise Exception('from_type must in user or group')
		if priority not in range(3):
			raise Exception('priority out of range')
		if not callable(detect):
			raise Exception('detect must callable')
		if type(call) not in (str, unicode) and not callable(call):
			raise Exception('detect must be string or unicode or callable')
		MessageProcess.TODO[from_type][priority].append({
			"detect": detect,
			"call": call,
		})

	@staticmethod
	def process(msg):
		if msg.isGroup():
			for methods in MessageProcess.TODO['group']:
				for method in methods:
					if method['detect'](msg):
						if type(method['call']) in (str, unicode):
							msg.Reply(method['call'])
						else:
							method['call'](msg)
						return
		else:
			for methods in MessageProcess.TODO['user']:
				for method in methods:
					if method['detect'](msg):
						if type(method['call']) in (str, unicode):
							msg.Reply(method['call'])
						else:
							method['call'](msg)
						return


class Message(object):
	"""global message event"""
	def __init__(self, platform):
		self.platform = platform

	def setEvent(self, **kwargs):
		if self.platform == 'Telegram':
			self.bot = kwargs['bot']
			self.update = kwargs['update']
			self.from_type = self.update.message.chat.type
		elif self.platform == 'LINE':
			self.event = kwargs['event']
			self.bot = kwargs['bot']
			logging.debug(self.event.source.type)
			self.from_type = self.event.source.type
			if self.from_type == 'user':
				self.user = self.bot.get_profile(self.event.source.user_id)
		if 'args' in kwargs:
			self.args = kwargs['args']
		self.message_type = kwargs['type']

	def Reply(self, data, type='text'):
		if self.platform == 'Telegram':
			if type == 'text':
				self.bot.sendMessage(chat_id=self.update.message.chat_id, text=data)
		elif self.platform == 'LINE':
			if type == 'text':
				self.bot.reply_message(
						self.event.reply_token,
						TextSendMessage(text=data)
					)

	def Tagged(self, compare=None):
		if self.platform == 'Telegram':
			if compare is None:
				reault = []
			for entity in self.update.message.entities:
				if entity.type == 'mention':
					tag = self.update.message.text[ entity.offset+1 : entity.offset+entity.length ]
					if compare is None:
						reault.append(tag)
					elif tag == compare:
						return True
			if compare is None:
				return result
			else:
				return False
		elif self.platform == 'LINE':
			result = re.findall(r'@(\w+)', self.event.message.text)
			logging.debug(result)
			if compare is None:
				return result
			if compare in result:
				return True

	def URL(self):
		if self.platform == 'Telegram':
			if compare is None:
				reault = []
			for entity in self.update.message.entities:
				if entity.type == 'url':
					url = self.update.message.text[ entity.offset+1 : entity.offset+entity.length ]
					if compare is None:
						reault.append(url)
			logging.debug(result)
			return result
		elif self.platform == 'LINE':
			result = re.findall(
					r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)",
					self.event.message.text
				)
			logging.debug(result)
			return result

	def isGroup(self):
		return self.from_type in ('room', 'group', 'supergroup')

	def isPrivate(self):
		return self.from_type in ('user', 'private')

	def UserName(self):
		if self.platform == 'Telegram':
			logging.debug(self.update.message)
			return self.update.message.from_user.username
		elif self.platform == 'LINE':
			return self.user.display_name

	def UserID(self):
		if self.platform == 'Telegram':
			return str(self.update.message.from_user.id)
		elif self.platform == 'LINE':
			return self.event.source.sender_id

	def GroupID(self):
		if self.platform == 'Telegram':
			return str(self.update.message.chat.id)
		elif self.platform == 'LINE':
			return self.event.source.sender_id

	def TextMessage(self):
		if self.platform == 'Telegram':
			return self.update.message.text
		elif self.platform == 'LINE':
			return self.event.message.text
