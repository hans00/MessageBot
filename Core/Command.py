class Commands(object):
	def __init__(self, name, platforms=[]):
		self.commands = {}
		self.descriptions = {}
		self.name = name
		for platform in platforms:
			platform.Command(name, self.callback, pass_args=True)

	def setCommand(self, name, call, description):
		self.commands[name] = call
		self.descriptions[name] = description

	def help(self):
		tmp = "Usage: ... <command>\n"
		tmp += (" "*12) + "help : Show this message\n"
		for cmd in self.commands:
			tmp += (" "*12) + cmd + " : " + self.descriptions[cmd] + "\n"
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

