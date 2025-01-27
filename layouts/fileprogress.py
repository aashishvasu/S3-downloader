import PySimpleGUI as sg
import src.downloader as downloader

files_downloaded:str = ''

layout = [
			[sg.Column([[sg.Text(text=files_downloaded, expand_x=True, key='filenames', visible=False)]], size=(None, 100), expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=True)],
			[sg.Frame('', [[sg.ProgressBar(max_value=100, orientation='h', key='fileprogress')]], key='fileframe')],
			[sg.Text(key="filesremaining")]
		]

def update_filename(window, filename):
	window['fileframe'].update(value=filename)

def update_progress(window, percentage):
	window['fileprogress'].update(percentage)

def update_filelist(window, filename):
	global files_downloaded
	files_downloaded += f'{filename} ✅\n'
	window['filenames'].update(files_downloaded, visible=True)