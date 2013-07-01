ot = angular.module("bombolone", ["ngResource"])

protocol = window.location.protocol
host = window.location.host
path = window.location.pathname


# Init Application
ot.value "appName", "bombolone"


# Main configuration
ot.config ($locationProvider, $interpolateProvider) ->

  # others
  $interpolateProvider.startSymbol "[["
  $interpolateProvider.endSymbol "]]"


# First commands
ot.run ($rootScope, $location) ->

  # Api path
  $rootScope.API = app["api_path"]

  # Ddropdown show
  $rootScope.dropdown_status = ""

  # Message show
  $rootScope.message_show = page["message_show"] or false
  $rootScope.message_status = page["message_status"] or ""
  $rootScope.message_message = page["message_message"] or ""

  $rootScope.message_icon = "x"
  $rootScope.loader = false

  # Language list
  $rootScope.lan = app["lan"]
  $rootScope.language = app["language"]

  # Others
  $rootScope.location = $location
  $rootScope.list_code = ["en", "it"]

  window.scope = angular.element(d).scope()


checkBroser = ->
  if d.all && !d.addEventListener
    alert "You should upgrade your copy of Windows Internet Explorer. This website does not support completely IE <= 8"