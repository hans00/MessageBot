from Group import Group

def Unink(cmds, DB, **args):
	Unink.group = Group(DB, **args)
	cmds.setCommand('group', Link.group, """Unink groups.""")
Unink.group = None
