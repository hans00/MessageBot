from Group import Group

def Link(DB):
	DB.Exec("CREATE TABLE IF NOT EXISTS public.link (id character(32), PRIMARY KEY (id));")
	Link.group = Group(DB)
	Link.cmds.setCommand('group', Link.group, """Link groups from different message platform.""")
Link.group = None

