import os
import pymysql
import subprocess
import sys
import shutil
from time import sleep, time

def get_solution_info(problem_id):
	cursor = db_root.cursor()
	try:
		sql = "SELECT solution FROM Judge_problem WHERE id=%d" % problem_id
		cursor.execute(sql)
		solution = cursor.fetchone()
		cursor.close()
		db_root.commit()
		return (solution[0])
	except Exception as e:
		print(e)
		db_root.rollback()
		print('get_solution_info_error')
		error_exit()

def get_submission_info(submission_id):
	cursor = db_root.cursor()
	try:
		sql = "SELECT problem_id, user_id, language, source, result FROM Judge_submission WHERE id=%d" % submission_id
		cursor.execute(sql)
		submission = cursor.fetchone()
		cursor.close()
		db_root.commit()
		return (submission[0], submission[1], submission[2], submission[3], submission[4])
	except Exception as e:
		print(e)
		db_root.rollback()
		print('get_submission_info_error')
		error_exit()

def update_submission(submission_id, time, result):
	cursor = db_root.cursor()
	try:
		sql = "UPDATE Judge_submission SET time=%f, result=%d WHERE id=%d" % (time, result, submission_id)
		cursor.execute(sql)
		cursor.close()
		db_root.commit()
	except Exception as e:
		print(e)
		db_root.rollback()
		print('update_submission_error')
		error_exit()

def update_user(user_id):
	cursor = db_root.cursor()
	try:
		sql = "UPDATE Judge_user SET solved_num=(SELECT count(DISTINCT problem_id) FROM Judge_submission WHERE user_id=%d AND result=%d) WHERE id=%d"\
			  % (user_id, OJ_AC, user_id)
		cursor.execute(sql)
		sql = "UPDATE Judge_user SET submit_num=(SELECT count(DISTINCT problem_id) FROM Judge_submission WHERE user_id=%d) WHERE id=%d"\
			  % (user_id, user_id)
		cursor.execute(sql)
		cursor.close()
		db_root.commit()
	except Exception as e:
		print(e)
		db_root.rollback()
		print('update_user_error')
		error_exit()

def update_problem(problem_id, result):
	cursor = db_root.cursor()
	try:
		sql = "UPDATE Judge_problem SET %s_num=(SELECT count(*) FROM Judge_submission WHERE problem_id=%d AND result=%d) WHERE id=%d"\
			  % (OJ[result], problem_id, result, problem_id)
		cursor.execute(sql)
		sql = "UPDATE Judge_problem SET submit_num=(SELECT count(*) FROM Judge_submission WHERE problem_id=%d) WHERE id=%d"\
			  % (problem_id, problem_id)
		cursor.execute(sql)
		cursor.close()
		db_root.commit()
	except Exception as e:
		print(e)
		db_root.rollback()
		print('update_problem_error')
		error_exit()

def clean_workdir(work_dir):
	shutil.rmtree(work_dir)

def error_exit():
	clean_workdir(work_dir)
	exit(1)

def execute(source, language, file_path):
	if language == SQL:
		source = source.replace(';', '')
		cursor = db_client.cursor()
		try:
			save_instructions = " INTO OUTFILE '%s' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';" % file_path
			source += save_instructions
			start_time = time()
			cursor.execute(source)
			end_time = time()
			cursor.close()
			db_client.commit()
		except Exception as e:
			print(e)
			db_root.rollback()
			return 0
		else:
			return end_time-start_time
	elif language == RELATION_ALGEBRA:
		with open("main.ra", 'w') as f:
			f.write(source)
		conf = "/home/haribo/radb/conf/mysql.ini"
		try:
			start_time = time()
			os.system("radb -i main.ra -o %s -c %s" % (file_path, conf))
			end_time = time()
		except Exception as e:
			print(e)
			return 0
		else:
			return end_time-start_time	
	else:
		print("Unknown Language")
		return 0


#TODO 
'''
	1.Set the time limit for the client process to detect the anomalies,
	and let Judged to determine how long should it sleep after running a 
	batch of job; that is, wait for most of the clients finish their job
'''
if __name__ == '__main__':
	#Configuration
	print("Client is running")
	(SQL, RELATION_ALGEBRA) = (0, 1)
	(OJ_AC, OJ_WA, OJ_CE, OJ_RE) = (1, 2, 3, 4)
	OJ = {1:"OJ_AC", 2:"OJ_WA", 3:"OJ_CE", 4:"OJ_RE"}
	db_root = pymysql.connect(host='localhost', port=3306, user='root', passwd='880915', db='JudgeSystem', charset='utf8')

	oj_home = "/home/haribo/judge"
	submission_id = int(sys.argv[1])
	work_dir = "%s/submission_%s" % (oj_home, submission_id)

	#If the working directory still exist, this means that the old client hasn't finish the job yet,
	#so the new clinet will exit directly to avoid conflict 
	if os.path.exists(work_dir):
		exit(0)
	os.makedirs(work_dir)
	os.system("chmod -R 777 %s/" % work_dir)
	os.chdir(work_dir)

	#Preprocessing
	(problem_id, user_id, language, source, result) = get_submission_info(submission_id)
	#Since Judged may call Judge_client to run on same submission numerous times, if one of them
	#has judged successfully, then others will exit
	print('result is', result)
	if result != 0:
		exit(0)
	solution = get_solution_info(problem_id)


	#Compile and Run
	db_client = pymysql.connect(host='localhost', port=3306, user='client', passwd='880915', db='JudgeSystem', charset='utf8')
	
	solution_file_path = os.path.join(work_dir, 'solution.csv')
	execute_time = execute(solution, language, solution_file_path)
	if execute_time == 0:
		print('execute_solution_error')
		error_exit()
	else:
		print('execute_solution_success')

	result_file_path = os.path.join(work_dir, 'result.csv')
	execute_time = execute(source, language, result_file_path)
	if execute_time == 0:
		print('execute_source_error')
		result = OJ_RE
	else:
		#WARNIG
		'''
			I should change diff to read file from result.csv and solution.csv to compare them
			because the files are belong to user:mysql and permission is 644 in mysql version8
			, while permission is 666 prior to it and means user:haribo can't use diff.
			The approach to solve it by far is use root to run the program, which is dangerous.
		'''
		print('execute_source_success')
		cmd = ["diff", result_file_path, solution_file_path]
		#universal_newlines: decode bytes to ascii code, since the return values are bytes
		diff_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
		ret = diff_process.communicate()[0]
		diff_process.wait()
		if len(ret) == 0:
			result = OJ_AC
			print('AC!!')
		else:
			result = OJ_WA
			print('WA!!')		

	update_submission(submission_id, time=execute_time, result=result)
	update_user(user_id)
	update_problem(problem_id, result=result)
	clean_workdir(work_dir)
	db_client.close()
	db_root.close()
	exit(0)

