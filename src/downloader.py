import os
import boto3
import src.settings as settings
import src.file_progress as fileProgress
from os.path import exists
os.system('cls' if os.name == 'nt' else 'clear')
# Create boto3 client
session = boto3.session.Session()
client:boto3.Session

# Callbacks
cb_downloads_started=None
cb_downloads_finished=None
cb_file_started=None
cb_file_finished=None
cb_file_progress=None

def init_session():
	global _filescomplete
	_filescomplete = 0

	global client
	client = session.client('s3', region_name=settings.bucket_region, endpoint_url=settings.endpoint, aws_access_key_id=settings.api_key, aws_secret_access_key=settings.api_secret)

def list_toplevel_folders():
	paginator = client.get_paginator('list_objects')
	result = paginator.paginate(Bucket=settings.bucket_name, Delimiter='/')

	toplevel:list = []
	for prefix in result.search('CommonPrefixes'):
		toplevel.append(prefix.get('Prefix'))

	return toplevel

def list_objects(prefix:str):
	paginator = client.get_paginator('list_objects')
	result = paginator.paginate(Bucket=settings.bucket_name, Prefix = prefix)

	files:list = []
	for name in result.search('Contents'):
		files.append(name.get('Key'))

	return files

def download_files(localpath:str, files:list, foldername:str):
	# Create the directory if it does not exist
	full_path = os.path.abspath(localpath)
	os.chdir(full_path)

	# Starting download callback
	if cb_downloads_started != None:
		cb_downloads_started()

	for filename in files:
		# Only download this file if it hasnt already been downloaded. Will help in resuming aborted downloads
		if exists(os.path.join(full_path,filename)) == False:
			if cb_file_started != None:
				cb_file_started(os.path.basename(filename))
			download_single_file(full_path, filename)
		else:
			print(f'Skipping file {filename} as it has already been downloaded')
		
		if cb_file_finished != None:
			cb_file_finished(os.path.basename(filename))
			
	print("Downloads completed!")

	# Call finishing downloads callback
	if cb_downloads_finished != None:
		cb_downloads_finished()

def download_single_file(full_path:str, filename:str):
	# Use the full_path variable instead of constructing the path again
	file_path = os.path.join(full_path, filename)
	path = file_path
	if os.path.basename(path).find("."):
		path = os.path.dirname(path)
	if not os.path.exists(path):
		os.makedirs(path)

	progress = fileProgress.ProgressPercentage(client, settings.bucket_name, filename, cb_file_progress)
	client.download_file(settings.bucket_name, filename, file_path, Callback=progress)