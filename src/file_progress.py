import os
import sys
import threading

class ProgressPercentage(object):

	def __init__(self, client, bucket, filename, cb_file_progress):
		self._filename = filename
		self._size = client.head_object(Bucket=bucket, Key=filename)['ContentLength']
		self._seen_so_far = 0
		self._lock = threading.Lock()
		self.prog_bar_len = 80
		self.cb_file_progress=cb_file_progress

	def __call__(self, bytes_amount):
		# To simplify, assume this is hooked up to a single filename
		with self._lock:
			self._seen_so_far += bytes_amount
			percent_done = (self._seen_so_far / self._size) * 100

			if self.cb_file_progress != None:
				self.cb_file_progress(percent_done)

			done = round(percent_done/(100/self.prog_bar_len))
			togo = self.prog_bar_len-done

			done_str = '█'*int(done)
			togo_str = '░'*int(togo)

			print(f'\t⏳ {self._filename}: [{done_str}{togo_str}] {round(percent_done, 2)}% done', end='\r\033[2J')

			if round(percent_done) == 100:
				print('\t✅')

