import pymysql

if __name__ == '__main__':
	db = pymysql.connect(host='localhost', port=3306, user='root', passwd='880915', db='JudgeSystem', charset='utf8')
	cursor = db.cursor()
	sql = "desc Judge_problem"
	cursor.execute(sql)
	data = cursor.fetchall()
	print(data)
	cursor.close()
	db.close()