import logging
from linebot.models import (
	TextSendMessage
)

class Message(object):
	"""global message event"""
	def __init__(self, platform):
		self.platform = platform

	def setEvent(self, **kwargs):
		if self.platform == 'Telegram':
			self.bot = kwargs['bot']
			self.update = kwargs['update']
			if self.update.message.chat.type == 'private':
				self.from_type = 'user'
			elif self.update.message.chat.type in ('supergroup', 'group'):
				self.from_type = 'room'
		elif self.platform == 'LINE':
			self.event = kwargs['event']
			self.bot = kwargs['bot']
			logging.debug(self.event)
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
			for entity in self.update.message.entities:
				if entity.type == 'mention':
					tag = self.update.message.text[ entity.offset+1 : entity.offset+entity.length ]
					logging.debug(tag)
					if compare is None:
						return True
					elif tag == compare:
						return True
		elif self.platform == 'LINE':
			result = re.findall(r'@(\w+)', self.event.message.text)
			logging.debug(result)
			if compare is None and len(result) > 0:
				return True
			if compare in result:
				return True

	def isGroup(self):
		return self.from_type == 'room'

	def isPrivate(self):
		return self.from_type == 'user'

	def UserName(self):
		if self.platform == 'Telegram':
			return self.update.message.user.id
		elif self.platform == 'LINE':
			return self.user.display_name

	def UserID(self):
		if self.platform == 'Telegram':
			return self.update.message.user.id
		elif self.platform == 'LINE':
			return self.event.source.sender_id()

	def RoomID(self):
		if self.platform == 'Telegram':
			return self.update.message.chat.id
		elif self.platform == 'LINE':
			return self.event.source.sender_id()

	def TextMessage(self):
		if self.platform == 'Telegram':
			return self.update.message.text
		elif self.platform == 'LINE':
			return self.event.message.text
