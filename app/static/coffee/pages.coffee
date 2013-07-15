# Main element to change language
PagesCtrl = ($scope, $resource, $rootScope) ->

  # Get page id
  page_update = path.match(/^\/admin\/pages\/update\/?$/i)

  # Default variables
  $scope.module = "pages"
  $scope.menu_language = false
  $scope.code_language = $rootScope.lan
  $scope.name_language = $rootScope.language
  $scope.list_labels = []

  if page_update
    $scope.ajaxHashTableList.get params, (resource) ->
      $rootScope.loader = false
      $rootScope.items_list = resource.hash_map_list
      $scope.show_hash_map_list = true
  else
    $scope.page =
      "name": "",
      "from": "",
      "import": "",
      "url": { "it": "", "en": ""},
      "title":  { "it": "", "en": ""},
      "description":  { "it": "", "en": ""},
      "content":  { "it": "", "en": ""},
      "file": "",
      "labels": []

  $("[data-toggle=dropdown]").blur ->
    $scope.menu_language = false

  # Open and close the language dropdown
  $scope.menu_reveal = ->
    $scope.menu_language = not $scope.menu_language

  # Set the language page are you working on,
  # and change on the dropdown
  $scope.change_language = (code, name_language) ->
    $scope.code_language = code
    $scope.name_language = name_language
    $scope.menu_reveal()

  $scope.add_label = ->
    label = 
      "type": "text"
      "label": "", 
      "alias": "", 
      "value": ""
    $scope.page.labels.push label

  $scope.remove_label = (index) ->
    $scope.page.labels.splice index, 1

PagesCtrl.$inject = ["$scope", "$resource", "$rootScope"]