from random import choice
from string import ascii_uppercase, digits

def newLinkID(DB):
	rnd_id = "".join(choice(ascii_uppercase+digits) for i in range(32))
	DB.Exec("INSERT INTO public.link(id) VALUES(%s);", [rnd_id])
	return rnd_id
