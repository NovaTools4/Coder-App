#--------Operating System Project--------
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
import requests
import plyer
import json
import os
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
import ssl
import android
from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path, secondary_external_storage_path

    
class Function(ScreenManager):		
	def execute_prompt(self,root):
		self.dialog = False
		if self.ids.name_prompt.text != '' and self.ids.prompt.text != '':
			try:
				os.chdir('/root/')
				if not self.dialog:
							self.dialog = MDDialog(
								title = "Coder",
								text = "Looks like you didn't download the app from the store or maybe your network is not secure.",
								buttons =[
									MDRectangleFlatButton(
										text="Ok", on_release = self.neat_dialog
										),
									],
								)
				
				self.dialog.open()
				

			except:
				name_prompt = str(self.ids.name_prompt.text)
				prompt = str(self.ids.prompt.text)
				try:
					url = requests.get("https://deepai.nova8593.repl.co/coder?text={}".format(prompt)).text
					response = json.loads(url)
					code = response["info"]["Order"]
				
					if os.path.exists("/sdcard/Coder"):
							with open(f"/sdcard/Coder/{name_prompt}.py", "w") as file:
								file.write(str(code))
							self.ids.result.text="The file has been saved to : "+"/sdcard/Coder/"+name_prompt+".py"
							self.ids.result_title.text="RESULT"
							self.ids.result_title.color="cyan"
							self.ids.result.color="green"
							self.ids.all.text=""
							root.current="result"
					else:
							os.mkdir("/sdcard/Coder/")
							with open(f"/sdcard/Coder/{name_prompt}.py", "w") as file:
								file.write(str(code))
							self.ids.result.text="The file has been saved to : "+"/sdcard/Coder/"+name_prompt+".py"
							self.ids.result_title.text="RESULT"
							self.ids.result_title.color="cyan"
							self.ids.result.color="green"
							self.ids.all.text=""
							root.current="result"
						
				except requests.exceptions.SSLError:
						if not self.dialog:
							self.dialog = MDDialog(
								title = "Coder",
								text = "Looks like you didn't download the app from the store or maybe your network is not secure.",
								buttons =[
									MDRectangleFlatButton(
										text="Ok", on_release = self.neat_dialog
										),
									],
								)
				
						self.dialog.open()

			else:
				self.ids.result.text="Input Field is Empty"
				self.ids.result_title.text=""
				self.ids.all.text="ERROR"
				self.ids.all.color="red"
				self.ids.result.color="pink"
				root.current="result"
			
	def neat_dialog(self, obj):
		self.dialog.dismiss()
		
		
			
	def make_another(self,root):
		self.ids.prompt.text = ''
		self.ids.name_prompt.text = ''
		root.current="first"
		

class Main(MDApp):
	Builder.load_file('layout.kv')
	
	def build(self):
			self.title = 'Coder'
			self.theme_cls.theme_style = "Light"
			self.theme_cls.primary_palette = "DeepPurple"
			ssl._create_default_https_context = ssl._create_unverified_context
			request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
			primary_ext_storage = primary_external_storage_path()
			secondary_ext_storage = secondary_external_storage_path()
			print("Primary Storage:", primary_ext_storage)
			print("Secondary Storage:", secondary_ext_storage)
			try:
				return Function()
			except Exception as error:
					print(error)
					url = requests.get('https://coder-logs.nova8593.repl.co/logs/?text={}'.format(str(error))).text
					print(url)
					if not self.dialog:
							self.dialog = MDDialog(
								title = "Error",
								text = '''
Oops, something went wrong.
Please try again later
								''',
								buttons =[
									MDRectangleFlatButton(
										text="Ok", on_release = self.neat_dialog
										),
									],
								)
				
					self.dialog.open()

Main().run()
