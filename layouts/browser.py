import PySimpleGUI as sg

# This will store the value of the currently selected toplevel folder
selection:str = ''
download_location:str = ''

# Define the main file view layout
layout = [
			[sg.Text('Folders on S3', key='s3text', visible=False)],
    		[sg.Listbox([], size=(None, 5), expand_x=True, enable_events=True, key='files', visible=False)],
            [sg.Frame('Download Location', [[sg.Input(enable_events=True, key='folderlocation'), sg.FolderBrowse('...', key='browse')]])],
            [sg.Button('Scan Bucket')]
		]

def is_selection_available():
    return True if selection != '' and download_location != '' else False