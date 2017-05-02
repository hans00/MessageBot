from Group import Group

def Unink(cmds, DB):
	Unink.group = Group(DB)
	cmds.setCommand('group', Link.group, """Unink groups.""")
Unink.group = None
