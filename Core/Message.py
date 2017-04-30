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
			self.from_type = self.event.message.source.type
			if self.from_type == 'user':
				self.user = self.bot.get_profile(self.event.source.userId)
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

	def isRoom(self):
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
			return self.event.source.userId

	def RoomID(self):
		if self.platform == 'Telegram':
			return self.update.message.chat.id
		elif self.platform == 'LINE':
			return self.event.source.roomId

	def TextMessage(self):
		if self.platform == 'Telegram':
			return self.update.message.text
		elif self.platform == 'LINE':
			return self.event.text
