from Group import Group

def Unlink(cmds, DB):
	Unlink.group = Group(DB)
	cmds.setCommand('group', Link.group, """Unlink groups.""")
Unlink.group = None
