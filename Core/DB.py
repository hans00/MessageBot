import psycopg2
import urlparse
import logging

urlparse.uses_netloc.append("postgres")

class DBCursor(object):
	"""DB Cursor"""
	def __init__(self, cur):
		self.cur = cur

	def Exec(self, sql, data=()):
		self.cur.execute(sql, data)
		return self

	def Fetch(self):
		return self.cur.fetchone()

	def FetchAll(self):
		return self.cur.fetchall()

	def __exit__(self):
		self.cur.close()
		logging.debug('DBCurser destructed.')

class DB(object):
	"""Link DB"""
	def __init__(self, db_url):
		url = urlparse.urlparse(db_url)
		self.conn = psycopg2.connect(
				database=url.path[1:],
				user=url.username,
				password=url.password,
				host=url.hostname,
				port=url.port
			)
		self.conn.autocommit = True

	def __call__(self):
		return DBCursor(self.conn.cursor())
		
	def __exit__(self):
		self.conn.close()
