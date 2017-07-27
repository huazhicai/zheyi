# coding:utf-8

import os 
import sys
import re
import psycopg2
import shutil


class PsqlOperator(object):
	def __init__(self):
		self.uid_username = []
		self.obj_users = []

	def connect_psql(self):
		global conn, cur 
		conn = psycopg2.connect(database="yfsrobot", host="116.62.4.239",
			user="postgres", password="DKilsioew213lHkY8", port="5432")
		cur = conn.cursor()
		print 'connect successful!'
		return (conn, cur)

	def get_userdata(self, pathfile):
		users_id = os.listdir(pathfile)
		users_id = [int(x) for x in users_id]
		for i in users_id:
			try:
				cur.execute("SELECT id, username FROM users where id= %d;" % i)
				rows = cur.fetchone()
				if rows is not None and len(rows) > 0:
					self.uid_username.append(rows)
			except:
				print "%d not exists" % i 
		# print self.uid_username
		return self.uid_username

	def connect_close(self):
		cur.close()
		conn.close()

	def _filter_user(self, arry):
		pattern = re.compile(r".+chan.+")
		result = pattern.search(arry[1])
		return result

	def get_estate_users(self):
		self.obj_users = list(sorted(filter(self._filter_user, self.uid_username),
		 key=lambda x: x[0]))
		# print self.obj_users
		return self.obj_users

	def copy_rename_file(self, src, target):
		for user in self.obj_users:
			shutil.copytree(os.path.join(src, str(user[0])) , os.path.join(target, "%d_%s" % user))
				

if __name__ == '__main__':
	db = PsqlOperator()
	db.connect_psql()
	db.get_userdata('/home/logfile/')
	db.connect_close()
	db.get_estate_users()
	db.copy_rename_file("/home/logfile", "/home/estate")
