from random import choice
from string import ascii_uppercase, digits

def newLinkID(DBCur):
	rnd_id = "".join(choice(ascii_uppercase+digits) for i in range(32))
	DBCur.Exec("INSERT INTO public.link(id) VALUES(%s);", [rnd_id])
	return rnd_id
