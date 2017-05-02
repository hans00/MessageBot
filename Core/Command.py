class Commands(object):
	def __init__(self, name, platforms=[]):
		self.commands = {}
		self.descriptions = {}
		self.name = name
		if type(platforms) in (list, tuple):
			for platform in platforms:
				platform.Command(name, self.callback, pass_args=True)
		elif type(platforms) is dict:
			for key in platforms:
				platforms[key].Command(name, self.callback, pass_args=True)
		else:
			raise Exception("platforms must be list oe tuple or dict")

	def setCommand(self, name, call, description):
		self.commands[name] = call
		self.descriptions[name] = description

	def help(self):
		tmp = "Usage: ... <command>\n"
		tmp += (" "*20) + "help : Show this message\n"
		for cmd in self.commands:
			tmp += (" "*20) + cmd + " : " + self.descriptions[cmd] + "\n"
		return tmp

	def callback(self, msg):
		if len(msg.args) == 0:
			msg.Reply(self.help())
		elif msg.args[0] == 'help':
			msg.Reply(self.help())
		elif msg.args[0] in self.commands:
			cmd = msg.args[0]
			del msg.args[0]
			self.commands[cmd](msg)
		else:
			msg.Reply("Not found this command.")

