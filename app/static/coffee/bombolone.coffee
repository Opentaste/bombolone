ot = angular.module("bombolone", ["ui", "ngResource"])

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


# List of custom directives
ot.directive "onKeyup", ->
  (scope, elm, attrs) ->
    elm.bind "keyup", ->
      scope.$apply attrs.onKeyup


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


_gaq = _gaq or []
_gaq.push ["_setAccount", "UA-23437071-1"]
_gaq.push ["_trackPageview"]

if not sync
  if not host.match(/^0.0.0.0:5000\/?$/i)
    ga_protocol = if 'https:' == protocol then '//ssl' else 'http://www'
    analytics = ga_protocol + '.google-analytics.com/ga.js'
    $script [analytics]