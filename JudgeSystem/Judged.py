import os
import pymysql
import subprocess
import sys
from time import sleep
import zc.lockfile
#from colorama import Fore, Back, Style

def daemon_init():
	try:
		pid = os.fork()
		if pid > 0:
			os._exit(0)
	except Exception as e:
		print(e)
		os._exit(1)

	os.setsid()
	os.chdir(oj_home)
	os.umask(0)

	si = open(os.devnull, 'r')
	so = open(os.devnull, 'w')
	sr = open(os.devnull, 'w')
	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(sr.fileno(), sys.stderr.fileno())

def get_jobs():
	try:
		#Since the isolation level(Repeatable read) for innodb, we need to commit whenever we exectute the command 
		#despite we just read the data. In such isolation level, the value we read from the table won't change 
		#for the duration of the transation. 
		cursor.execute("SELECT * FROM Judge_submission WHERE result = 0 ORDER BY id")
		db.commit()
	except Exception as e:
		print(e)
		db.rollback()
		print("get_jobs_error")
		exit(1)
	else:
		submissions = cursor.fetchall()
		jobs = []

		for submit in submissions:
			jobs.append(int(submit[0]))

		return jobs

def run_client(submission_id):
	os.system("python3 /home/haribo/Database/JudgeSystem/Judge_client.py %d" % submission_id)


#TODO
'''
	Set the limit of max running client, or the system will crash usually!!
'''
def work():
	jobs = get_jobs()
	jobs_num = len(jobs)
	print(jobs_num, jobs)

	if jobs_num > max_running_job:
		jobs_num = max_running_job

	for i in range(jobs_num):
		submission_id = jobs[i]

		pid = os.fork()
		if pid > 0:
			os.waitpid(pid, 0)
		else:
			pid = os.fork()
			if pid > 0:
				os._exit(0)
			else:
				run_client(submission_id)
				os._exit(0)
		
		print('finish job', i)

	return jobs_num

if __name__ == '__main__':
	oj_home = '/home/haribo/judge'
	db = pymysql.connect(host='localhost', port=3306, user='root', passwd='880915', db='JudgeSystem', charset='utf8')
	cursor = db.cursor()
	max_running_job = 10
	
	daemon_init()

	#To avoid mutiple daemons 
	lock = zc.lockfile.LockFile('/var/run/Judged.pid')

	finished_num = 1
	sleep_time = 5

	while True:
		while finished_num:
			finished_num = work()
			sleep(2)
		sleep(sleep_time)
		finished_num = 1

	cursor.close()
	db.close()