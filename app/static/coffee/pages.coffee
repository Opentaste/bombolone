# Main element to change language
PagesCtrl = ($scope, $resource, $rootScope) ->

  # Get page variables
  page_new = path.match(/^\/admin\/pages\/new\/?$/i)
  page_update = path.match(/^\/admin\/pages\/update\/?$/i)
  page_list = path.match(/^\/admin\/pages\/?$/i)

  # Default variables
  $scope.module = "pages"
  $scope.menu_language = false
  $scope.code_language = $rootScope.lan
  $scope.name_language = $rootScope.language
  $scope.list_labels = []

  if page_list
    $rootScope.loader = true
    $scope.ajaxPagesList.get (resource) ->
      $rootScope.loader = false
      $rootScope.items_list = resource.page_list
      $scope.show_item_list = true

  else if page_update
    params = 
      _id: $scope.page_id
    $scope.ajaxHashTableList.get params, (resource) ->
      $rootScope.loader = false
      $rootScope.items_list = resource.hash_map_list
      $scope.show_hash_map_list = true

  else if page_new
    $scope.page =
      "name": "",
      "from": "",
      "import": "",
      "url": { "it": "", "en": ""},
      "title":  { "it": "", "en": ""},
      "description":  { "it": "", "en": ""},
      "content":  [],
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
    label_item = 
      "name": ""
      "type": "text"

    content_item = 
      "alias": {"it": "", "en": ""}, 
      "value": {"it": "", "en": ""}

    $scope.page.labels.push label_item
    $scope.page.content.push content_item

  $scope.remove_label = (index) ->
    $scope.page.labels.splice index, 1
    $scope.page.content.splice index, 1

  $scope.new = ->
    $rootScope.message_show = false
    paramas = $scope.page
    paramas["token"] = app["token"]
      
    $scope.ajaxPagesNew.save paramas, (resource) ->
      $scope.show_message(resource)

  $scope.save = ->
    $rootScope.message_show = false
    paramas =
      "_id": $scope.hash_map_id
      "name": $scope.hash_map.name
      "token": app["token"]

    paramas = __get_value(paramas)
      
    $scope.ajaxPagesUpdate.save paramas, (resource) ->
      $scope.show_message(resource)

PagesCtrl.$inject = ["$scope", "$resource", "$rootScope"]