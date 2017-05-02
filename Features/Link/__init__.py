from Group import Group

def Link(cmds, DB, **args):
	Link.group = Group(DB, **args)
	cmds.setCommand('group', Link.group, """Link groups from different message platform.""")
Link.group = None

