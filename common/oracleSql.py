#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2019年5月21日
@author: yuejing
'''
import cx_Oracle
from . import yamlHandle

def read_sql(file_name) :
	f = open(file_name, "r")
	str1 = f.read()
	f.close()
	return str1

class sqlHandle:

	Config = yamlHandle.configyaml('config.yaml').readyaml()

	def __init__(self,host=Config['db_stride']['host'],db=Config['db_stride']['server_name'],user=Config['db_stride']['username'],password=Config['db_stride']['password']):
		self.db_link=user+'/'+password+'@'+host+'/'+db

	def sqlTxt(self,path,username,nStart=0,nNum=-1):
		sql=read_sql(path).format(username)
		rt = []
		con = cx_Oracle.connect(self.db_link)
		cur = con.cursor()    # 获取cursor
		if not cur:
			return rt
		# 查询到列表
		cur.execute(sql)
		if (nStart == 0) and (nNum == 1):
			rt.append(cur.fetchone())
		else:
			rs = cur.fetchall()
			if nNum == - 1:
				rt.extend(rs[nStart:])
			else:
				rt.extend(rs[nStart:nStart + nNum])
		#print("Total: " + str(cur.rowcount)+'行数据')
		con.close()     # 释放cursor
		return rt

	def sqlQuery(self,sql,nStart=0,nNum=-1):
		rt = []
		con = cx_Oracle.connect(self.db_link)
		cur = con.cursor()    # 获取cursor
		if not cur:
			return rt
		# 查询到列表
		cur.execute(sql)
		if (nStart == 0) and (nNum == 1):
			rt.append(cur.fetchone())
		else:
			rs = cur.fetchall()
			if nNum == - 1:
				rt.extend(rs[nStart:])
			else:
				rt.extend(rs[nStart:nStart + nNum])
		#print("Total: " + str(cur.rowcount)+'行数据')
		con.close()     # 释放cursor
		return rt

