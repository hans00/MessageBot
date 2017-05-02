import logging
from Common import removeLinkID

class Group(object):
	def __init__(self, DB):
		self.DB = DB

	def __call__(self, msg):
		if not msg.isGroup():
			msg.Reply("This function only for group.")
		elif len(msg.args) != 1 or msg.args[0] not in ('this', 'all'):
			msg.Reply("Invalid arguments.\nUse: /unlink group < this | all >")
		else:
			if msg.args[0] == 'this':
				result = self.DB().Exec(
					"""
					SELECT link_id, COUNT(*)
						FROM public.link_group
						WHERE link_id IN (
							SELECT link_id
								FROM public.link_group
								WHERE group_id = %s
								AND user_id = %s
						)
						GROUP BY link_id;
					""",
					(
						msg.GroupID(),
						msg.UserID()
					)
				).Fetch()
				if result:
					link_id, count = result
					if count == 1:
						self.DB().Exec("DELETE FROM public.link_group WHERE link_id = %s;", [link_id])
						removeLinkID(self.DB(), link_id)
					else:
						self.DB().Exec("DELETE FROM public.link_group WHERE group_id = %s;", [msg.GroupID()])
					msg.Reply("Now unlinked.")
				else:
					msg.Reply("Your group not in linked or you not link creator.")
			elif msg.args[0] == 'all':
				result = self.DB().Exec(
					"SELECT link_id FROM public.link_group WHERE group_id = %s AND user_id = %s GROUP BY link_id;",
					(
						msg.GroupID(),
						msg.UserID()
					)
				).Fetch()
				if result:
					link_id = result[0]
					self.DB().Exec("DELETE FROM public.link_group WHERE link_id = %s;", [link_id])
					removeLinkID(self.DB(), link_id)
					msg.Reply("Now all unlinked.")
				else:
					msg.Reply("Your group not in linked or you not link creator.")
			