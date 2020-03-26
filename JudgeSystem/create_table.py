import os
import sys
import pymysql
import argparse

def parse_command():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', type=str, dest='data', help='csv_file for the content of the table')
	parser.add_argument('-t', '--table', type=str, dest='table', help="New table's name")
	parser.add_argument('sql_script', type=str, help='SQL script for create table')
	return parser.parse_args()

def create_table(sql_script, table):
	with open(sql_script, 'r') as f:
		sql = f.read()
	try:
		cursor.execute('drop table if exists %s' % table)
		cursor.execute(sql)
		db.commit()
		print('create_table_success')
	except Exception as e:
		print(e)
		db.rollback()
		print('create_table_error')

	sql = "INSERT INTO %s VALUES ('%s')" % ('Judge_problem_table(name)', table)
	try:
		cursor.execute("SELECT name FROM Judge_problem_table WHERE name='%s'" % table)
		ret = cursor.fetchone()

		if len(ret) == 0:
			#cursor.execute("delete from Judge_problem_table where name='%s'" % table)
			cursor.execute(sql)
			db.commit()
			print('create_table_name_success')
	except Exception as e:
		print(e)
		db.rollback()
		print('create_table_name_error')	

def load_data(data_path, table):
	sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"\
		  % (data_path, 'JudgeSystem.'+table)
	try:
		cursor.execute("delete from %s" % table)
		cursor.execute(sql)
		db.commit()
		print('load_data_success')
	except Exception as e:
		print(e)
		db.rollback()
		print('load_data_error')


if __name__ == '__main__':
	args = parse_command()
	#We need to add local_infile parameter to avoid security error in mysql
	db = pymysql.connect(host='localhost', port=3306, user='root', passwd='880915', db='JudgeSystem', charset='utf8', local_infile=1)
	cursor = db.cursor()
	create_table(args.sql_script, args.table)
	load_data(args.data, args.table)
	cursor.close()
	db.close()



