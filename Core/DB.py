from unqlite import UnQLite

class DB():
	"""Link DB"""
	def __init__(self, file):
		self.db = UnQLite(file)
		self.db.transaction()
		self.tables = {}

	def Table(self, table):
		if table not in self.tables:
			self.tables[table] = self.db.collection(table)
			self.tables[table].create()
		return self.tables[table]

	def Drop(self, table):
		if table in self.tables:
			self.tables[table].drop()
			del self.tables[table]

	def Insert(self, table, value):
		return self.tables[table].store(value)

	def Select(self, table, filter = {}):
		if len(filter) == 0:
			return self.tables[table].all()
		else:
			return self.tables[table].filter(lambda obj: sum(obj[k] == filter[k] for k in filter))
		
	def Update(self, table, index, value):
		return self.tables[table].update(index, value)

	def __delitem__(self, table):
		return self.tables[table]

	def __getitem__(self, table):
		return self.tables[table]
