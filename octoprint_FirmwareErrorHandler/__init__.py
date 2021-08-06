# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os

class FirmwareErrorHandler(octoprint.plugin.AssetPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.SettingsPlugin):

	##~~ gcode received hook
	def process_gcode_received(self, comm, line, *args, **kwargs):
		if not line.startswith("Error"):
			return line
		
		listErrors = self._settings.get(["errors"])
		if any(d["error"] == line for d in listErrors):
			listErrors_error = self.error_search(listErrors,"error",line)
			
			if listErrors_error["disconnect"]:
				self._printer.disconnect()
				
			if listErrors_error["cmd_on_error"] != "":
				os.system(listErrors_error["cmd_on_error"])
				
			if listErrors_error["msgtype"] != "disabled":
				self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=line, msgtype=listErrors_error["msgtype"], autoclose=listErrors_error["autoclose"]))
			
			if listErrors_error["passthrough"]:
				return line

			return None

		return line
			
	##~~ Settings mixin
	def get_settings_defaults(self):
		return dict(errors=[{'error':'Error: MAXTEMP triggered!','disconnect':False,'cmd_on_error':'','msgtype':'error','autoclose':False,'passthrough':True}])
		
	def get_settings_version(self):
		return 1
		
	def on_settings_migrate(self, target, current=None):
		if current is None or current < self.get_settings_version():
		  #reset error settings to accomodate changes
		  self._settings.set(['errors'], self.get_settings_defaults()["errors"])
	
	##~~ Template mixin
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]
	
	##~~ AssetPlugin mixin
	def get_assets(self):
		return dict(js=["js/FirmwareErrorHandler.js"])
		
	##~~ Utility functions
	def error_search(self, list, key, value): 
		for item in list: 
			if item[key] == value: 
				return item
		
	##~~ Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			FirmwareErrorHandler=dict(
				displayName="FirmwareErrorHandler",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jneilliii",
				repo="OctoPrint-FirmwareErrorHandler",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/jneilliii/OctoPrint-FirmwareErrorHandler/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "FirmwareErrorHandler"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = FirmwareErrorHandler()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.process_gcode_received,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
