import PySimpleGUI as sg
import src.settings as settings

# Define the settings layout
layout = [
			[sg.Frame('Api Key', [[sg.InputText(default_text=settings.api_key, key='apikey')]], font=('Arial', 7))],
			[sg.Frame('Api Secret', [[sg.InputText(default_text=settings.api_secret, key='apisecret')]], font=('Arial', 7))],
			[sg.Frame('Bucket Name', [[sg.InputText(default_text=settings.bucket_name, key='bucketname')]], font=('Arial', 7))],
			[sg.Frame('Bucket Region', [[sg.InputText(default_text=settings.bucket_region, key='bucketregion')]], font=('Arial', 7))],
			[sg.Frame('Bucket URL', [[sg.InputText(default_text=settings.bucket_url, key='bucketurl')]], font=('Arial', 7))],
			[sg.Frame('Endpoint', [[sg.InputText(default_text=settings.endpoint, key='endpoint')]], font=('Arial', 7))],
		]

# Returns a different set of bg and text colors so that a toggling type look can be achieved
def get_button_color(pressed:bool):
	if pressed:
		return 'white', 'black'
	else:
		return sg.theme_button_color_background(), sg.theme_button_color_text()

# If pressed is false, then settings window is getting closed so the settings should be saved
def save_settings(pressed:bool, values):
	if not pressed:
		settings.api_key = values['apikey']
		settings.api_secret = values['apisecret']
		settings.bucket_name = values['bucketname']
		settings.bucket_region = values['bucketregion']
		settings.bucket_url = values['bucketurl']
		settings.endpoint = values['endpoint']

		# Write to file
		settings.write_config()