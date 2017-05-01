import threading
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")

class DB(threading.Thread):
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
		self.cur = self.conn.cursor()
		self.lock = False

	def Exec(self, sql, data=()):
		while not self.lock: pass
		self.lock = True
		self.cur.execute(sql, data)
		return self

	def Release(self):
		self.lock = False

	def FetchOne(self):
		return self.cur.fetchone()

	def FetchAll(self):
		result = self.cursor.fetchall()
		self.lock = False
		return result
		
	def __exit__(self):
		self.cur.close()
		self.conn.close()
