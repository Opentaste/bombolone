HashTableCtrl = ($scope, $resource, $rootScope, $location) ->
  $rootScope.admin_module = "hash_table"

  hash_table_overview = path.match(/^\/admin\/hash_table\/overview\/?$/i)
  hash_table_index = path.match(/^\/admin\/hash_table\/?$/i)
  hash_table_new = path.match(/^\/admin\/hash_table\/new\/?$/i)
  hash_table_update = path.match(/^\/admin\/hash_table\/update\/([^\/]+)\/?$/i)
  hash_table_view = path.match(/^\/admin\/hash_table\/view\/([^\/]+)\/?$/i)

  $scope.menu_language = false
  $scope.show_hash_map_list = false
  $scope.hash_map_id = ""

  $scope.hash_map = 
    name: ""
    value: {}
  
  _init_hash_table = () ->
    $scope.hash_table =
      language : $rootScope.language
      lan : $rootScope.lan

  # Index hash table
  if hash_table_index or hash_table_overview or hash_table_view
    $rootScope.loader = true
    $scope.ajaxHashTableList.get params, (resource) ->
      $rootScope.loader = false
      $rootScope.items_list = resource.hash_map_list
      $scope.show_hash_map_list = true

  # New hash table
  else if hash_table_new
    $scope.title = "New Hash Table"
    $scope.update = false
    _init_hash_table()


  # Update hash table
  if hash_table_update or hash_table_view
    $scope.title = "Update"
    $scope.update = true
    _init_hash_table()

    if hash_table_view
      $scope.hash_map_id = hash_table_view[1]
    else
      $scope.hash_map_id = hash_table_update[1]
    params = _id: $scope.hash_map_id

    $scope.ajaxHashTableGet.get params, (resource) ->
      $scope.hash_map = resource.hash_map
      for key, value of $scope.hash_map.value
        $scope.hash_map.value[key]["key"] = key


  # Upsert page: change language
  $scope.change_language = (code, language) ->
    $scope.hash_table.lan = code
    $scope.hash_table.language = language
    $scope.menu_language = false


  $scope.change_name_label = (name_label) ->
    $scope.name_label = name_label


  $scope.remove_label = (key) ->
    delete $scope.hash_map.value[key]


  counter = 0


  $scope.add_label = ->
    key = "aaa_key_#{counter}"
    counter += 1
    value =
      en: "",
      it: "",
      key: ""
    $scope.hash_map.value[key] = value


  $scope.menu_reveal = ->
    $scope.menu_language = not $scope.menu_language


  $scope.new = ->
    $rootScope.message_show = false
    paramas =
      "name": $scope.hash_map.name
      "token": app["token"]

    paramas = __get_value(paramas)
      
    $scope.ajaxHashTableNew.save paramas, (resource) ->
      $scope.show_message(resource)


  $scope.save = ->
    $rootScope.message_show = false
    paramas =
      "_id": $scope.hash_map_id
      "name": $scope.hash_map.name
      "token": app["token"]

    paramas = __get_value(paramas)
      
    $scope.ajaxHashTableUpdate.save paramas, (resource) ->
      $scope.show_message(resource)


  __get_value = (hash_map) ->
    for code in $scope.list_code
      counter = 0
      for key, value of $scope.hash_map.value
        hash_map["label-name-#{counter}"] = value["key"]
        hash_map["label-#{code}-#{counter}"] = value[code]
        counter += 1
      hash_map["len"] = counter
    return hash_map

HashTableCtrl.$inject = ["$scope", "$resource", "$rootScope", "$location"]


