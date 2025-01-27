import threading
import PySimpleGUI as sg
import layouts.settings as ly_settings
import layouts.browser as ly_browser
import layouts.fileprogress as ly_fileprogress
import src.downloader as downloader

downloader.init_session()

# Window theme
sg.theme('BrownBlue')

mainWindowLayout = [
						[sg.Column(layout=ly_browser.layout, key='-FILEVIEW-'), sg.Column(layout=ly_settings.layout, key='-SETTINGS-', visible=False), sg.Column(layout=ly_fileprogress.layout, key='-FILEPROGRESS-', visible=False)],
						[sg.Button('Download', disabled=True), sg.Button('S3 Settings', key='-SETTINGSBTN-'), sg.Push(), sg.Button('Quit')]
					]
window = sg.Window('S3 Downloader', mainWindowLayout)

def file_download_started(filename:str):
	window.write_event_value('file-download-started', filename)

def file_download_finished(filename:str):
	window.write_event_value('file-download-finished', filename)

def file_progress_updated(percentage:float):
	window.write_event_value('file-download-progress-updated', percentage)

def run():
	settings_pressed:bool = False
	while True:
		event, values = window.read()
		
		# S3 Settings button
		if event == '-SETTINGSBTN-':
			# Update visible layout flag
			settings_pressed = not settings_pressed
			# Update the settings layout
			window['-FILEVIEW-'].update(visible=not settings_pressed)
			window['-SETTINGS-'].update(visible=settings_pressed)
			ly_settings.save_settings(settings_pressed, values)

			btn_bg_color, btn_text_color = ly_settings.get_button_color(settings_pressed)
			window['-SETTINGSBTN-'].update(button_color=(btn_text_color, btn_bg_color))

		# Scan button
		if event == 'Scan Bucket':
			folderlist = downloader.list_toplevel_folders()
			if len(folderlist) > 0:
				window['files'].update(values=folderlist, visible=True)
				window['s3text'].update(visible=True)

		# File list event
		if event == 'files':
			ly_browser.selection=values[event][0]

		# Download location event
		if event == 'folderlocation' and values[event] != '':
			ly_browser.download_location = values[event]
		
		t:threading.Thread = None
		# Start download
		if event == 'Download':
			# Assign callbacks
			downloader.cb_file_started = file_download_started
			downloader.cb_file_finished = file_download_finished
			downloader.cb_file_progress = file_progress_updated

			# Update layouts and start downloads
			window['-FILEPROGRESS-'].update(visible=True)

			# List files to download and begin
			filelist = downloader.list_objects(ly_browser.selection)

			t = threading.Thread(target=downloader.download_files, args=(ly_browser.download_location, filelist, ly_browser.selection))
			t.start()

		# Download event callbacks
		if event == 'file-download-started':
			ly_fileprogress.update_filename(window, values[event])

		if event == 'file-download-progress-updated':
			ly_fileprogress.update_progress(window, values[event])
		
		if event == 'file-download-finished':
			ly_fileprogress.update_filelist(window, values[event])

		# Handle enabling and disabling the download button
		window['Download'].update(disabled=not ly_browser.is_selection_available())		

		# Exit button
		if event == 'Quit' or event == sg.WIN_CLOSED:
			if t != None:
				t.join()
			break
		
	window.close()