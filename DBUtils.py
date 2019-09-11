import pymssql

class DBUtils(object):
	def __init__(self, host, database, user, password):
		self.host = host
		self.database = database
		self.user = user
		self.password = password

	def Connect(self):
		"""
		连接数据库
		"""
		self.conn = pymssql.connect(host = self.host,user = self.user,password = self.password,database = self.database)
		cur = self.conn.cursor()
		if not cur:
			raise ('数据连接失败')
		else:
			# print('connection complete!')
			return cur

	def ExecSql_dict(self, sql):
		"""
		功能：执行sql，返回字典，字典value仅有：字段值
		"""
		cur = self.Connect()
		cur.execute(sql)
		dataList = cur.fetchall()
		dataName = [col[0] for col in cur.description] #字段名称
		self.conn.close()
		return ([
		dict(zip(dataName, row))
		for row in dataList
		])
	
	def ExecSql_dict2(self, sql):
		"""
		功能：执行sql，返回字典，字典的value是一个tuple包含：字段值、字段类型type_code
		其中根据实际测试type_code和字段类型的对应关系如下:
			1:字符型
			2：	
			3：整型
			4：时间类型
		"""
		cur = self.Connect()
		cur.execute(sql)
		dataList = cur.fetchall()
		dataName = [col[0] for col in cur.description] #字段名称
		dataType = [col[1] for col in cur.description] #字段类型

		list_val_type = [list(zip(dataType,row)) for row in dataList]
		dict_res = [dict(zip(dataName,i)) for i in list_val_type]
		# print(list_val_type)
		self.conn.close()
		return(dict_res)

	def ExecSql_content(self, sql):
		"""
		功能：执行sql，直接返回，不加工
		"""
		cur = self.Connect()
		cur.execute(sql)
		content = cur.fetchall()
		self.conn.close()
		return (content)

	def ExecSql_Insert(self, sql, tableName):
		"""
		功能：执行sql(查询单表的语句)，返回'表插入语句'的字符串
		"""
		identity_sql = '''select b.name from sys.objects a,sys.columns b where a.object_id=b.object_id and a.type='U' 
						and a.name='{table}'and b.is_identity=1'''.format(table=tableName)
		identityCol = self.ExecSql_dict(identity_sql)
		if identityCol:
			identityCol = identityCol[0].get('name')
		else:
			identityCol =''
		sqlStart = 'INSERT INTO {table} ('.format(table=tableName)
		valueList = []
		data_dict2 = self.ExecSql_dict2(sql)
		sql = ''
		if data_dict2 :
			# print(data_dict2)
			for i in range(len(data_dict2)): 
				key1 = ''
				value1 = ''
				for key,value in data_dict2[i].items():
					value = list(value)
					if key==identityCol: #自增列不进行赋值
						continue
					key1 = key1 + ',' + key
					if value[0]==4:
						value[1] = str(value[1])[:23] #python转化sqlserver中的datetime类型数据时，末尾会追加000，此处去除
					value1 = value1 + ',\'' + str(value[1]).replace('\'','\'\'').replace('None','null')+'\''
					valueList.append(value1)
				sql =sql + sqlStart+' '+key1.strip(',')+')values('+str(value1).strip(',').replace('\'null\'','null')+')\n'
		return (sql+'\nGO')
