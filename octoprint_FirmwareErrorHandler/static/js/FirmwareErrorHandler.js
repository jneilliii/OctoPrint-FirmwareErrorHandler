$(function() {
    function FirmwareErrorHandlerViewModel(parameters) {
        var self = this;
		
		self.settingsViewModel = parameters[0];
		
		self.errors = ko.observableArray();
		self.msgTypes = ko.observableArray([{
						name : 'Notice',
						value : 'notice'
					}, {
						name : 'Error',
						value : 'error'
					}, {
						name : 'Info',
						value : 'info'
					}, {
						name : 'Success',
						value : 'success'
					}, {
						name : 'Disabled',
						value : 'disabled'
					}
				]);

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "FirmwareErrorHandler") {
				// console.log('Ignoring '+plugin);
                return;
            }
			
			if(data.type == "popup") {
				// console.log(data.msg);
				new PNotify({
					title: 'Firmware Error Received',
					text: data.msg,
					type: data.msgtype,
					hide: data.autoclose
					});
			}
		}
		
		self.onBeforeBinding = function() {
			self.errors(self.settingsViewModel.settings.plugins.FirmwareErrorHandler.errors());
        }
		
		self.onEventSettingsUpdated = function (payload) {
			self.errors(self.settingsViewModel.settings.plugins.FirmwareErrorHandler.errors());
        }
		
		self.addError = function() {
			self.settingsViewModel.settings.plugins.FirmwareErrorHandler.errors.push({'error':ko.observable(''),
									'disconnect':ko.observable(false),
									'cmd_on_error':ko.observable(''),
									'msgtype':ko.observable('error'),
									'autoclose':ko.observable(false),
									'passthrough':ko.observable(true)});
		}
		
		self.removeError = function(row) {
			self.settingsViewModel.settings.plugins.FirmwareErrorHandler.errors.remove(row);
		}
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        FirmwareErrorHandlerViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#settings_plugin_FirmwareErrorHandler"]
    ]);
});