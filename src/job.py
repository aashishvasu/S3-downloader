import os
import json

class Job(object):
	# Folder in which to store jobs
	job_folder:str = 'jobs/'
	def __init__(self, jobname:str, write_on_change:bool=False):
		self.jobname=jobname.replace('/', '')
		self.write_on_change=write_on_change
		self.completed=[]

		# Load the job if any detected
		self.load_job()
	
	# Updates the list of completed files in job
	def update_job(self, filename:str):
		self.completed.append(filename)

		# If write on change is active, dump to file immediately
		if self.write_on_change:
			self.save_job()

	# Load json job from file
	def load_job(self):
		job_path = f'{os.path.join(Job.job_folder, self.jobname)}.json'

		if os.path.exists(job_path):
			with open(job_path, 'r') as f:
				data = json.load(f)
				self.completed = data['completed']
				f.close()
		elif os.path.exists(Job.job_folder) == False:
			os.makedirs(Job.job_folder)			

	# Dump json to file
	def save_job(self):
		completed:dict = {
							"completed":self.completed
						}
		
		if not os.path.exists(Job.job_folder):
			os.makedirs(Job.job_folder)

		with open(f'{os.path.join(Job.job_folder, self.jobname)}.json', 'w') as f:
			json.dump(completed, f)
			f.close()