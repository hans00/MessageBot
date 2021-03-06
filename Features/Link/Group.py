import logging
from Common import newLinkID

class Group(object):
	def __init__(self, DB, Telegram, LINE):
		self.DB = DB
		self.Telegram = Telegram
		self.LINE = LINE

	def check(self, msg):
		return self.DB().Exec("SELECT * FROM public.link_group WHERE group_id = %s;", [msg.GroupID()]).Fetch()

	def message(self, msg):
		if msg.platform == 'LINE':
			name = 'unknown'
		elif msg.platform == 'Telegram':
			if msg.UserName() is None or msg.UserName() == '':
				name = 'unknown'
			else:
				name = msg.UserName()
		sendMsg = "<" + name + ">: " + msg.TextMessage()
		result = self.DB().Exec(
			"""
			SELECT group_id, platform
				FROM public.link_group
				WHERE link_id IN (
					SELECT link_id
						FROM public.link_group
						WHERE group_id = %s
				)
				AND group_id <> %s;
			""",
			[msg.GroupID(), msg.GroupID()]
		).FetchAll()
		for group in result:
			if group[1] == 'Telegram':
				self.Telegram.Push(group[0], sendMsg)
			elif group[1] == 'LINE':
				self.LINE.Push(group[0], sendMsg)

	def __call__(self, msg):
		if not msg.isGroup():
			msg.Reply("This function only for group.")
		elif len(msg.args) != 1 or (msg.args[0] not in ('create', 'info') and len(msg.args[0]) != 32):
			msg.Reply("Invalid arguments.\nUse: /link group < create | info | *ID* >")
		else:
			if msg.args[0] == 'create':
				newid = newLinkID(self.DB())
				self.DB().Exec(
					"INSERT INTO public.link_group (link_id, platform, group_id, user_id) VALUES(%s, %s, %s, %s);",
					(
						newid,
						msg.platform,
						msg.GroupID(),
						msg.UserID()
					)
				)
				msg.Reply("Your ID is \n" + newid)
			elif msg.args[0] == 'info':
				result = self.DB().Exec("SELECT * FROM public.link_group WHERE group_id = %s;", [msg.GroupID()]).Fetch()
				if result:
					reply = "Your ID is \n" + result[0] + "\n\n"
					result = self.DB().Exec("SELECT COUNT(*) FROM public.link_group WHERE link_id = %s;", [result[0]]).Fetch()
					reply += "Now linked " + str(result[0]) + " groups."
					msg.Reply(reply)
				else:
					msg.Reply("Your group not in linked.")
			elif not self.DB().Exec("SELECT * FROM public.link_group WHERE group_id = %s;", [msg.GroupID()]).Fetch():
				self.DB().Exec(
					"INSERT INTO public.link_group (link_id, platform, group_id, user_id) VALUES(%s, %s, %s, %s);",
					(
						msg.args[0],
						msg.platform,
						msg.GroupID(),
						msg.UserID()
					)
				)
				msg.Reply("Now linked.")
			else:
				msg.Reply("Your group already linked.")
			