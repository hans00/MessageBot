def create_if_not_exists(DBCur):
	# link DB
	try:
		DBCur.Exec("SELECT * FROM public.link;")
	except:
		DBCur.Exec(
			"""
			CREATE TABLE public.link (id character(32), PRIMARY KEY (id));
			CREATE TABLE public.link_group (link_id character(32), platform character varying(10), group_id character varying(40), user_id character varying(40));
			CREATE INDEX group_id ON public.link_group (group_id);
			ALTER TABLE public.link_group ADD FOREIGN KEY (link_id) REFERENCES public.link(id);
			"""
		)