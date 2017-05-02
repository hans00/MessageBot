def removeLinkID(DBCur, id):
	DBCur.Exec("DELETE FROM public.link WHERE id = %s;", [id])