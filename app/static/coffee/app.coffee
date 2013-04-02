# Application controller
AppCtrl = ($scope, $resource, $rootScope) ->

  $scope.dropdown = ->
    if $rootScope.dropdown_status is "open"
      $rootScope.dropdown_status = ""
    else
      $rootScope.dropdown_status = "open"

  # Set language: there are two case:
  # 1) no sign in, so the language is saved in the cookie
  # 2) otherwise it's saved user profile
  # It's called a ajax request that if is everything fine,
  # it will reload the current page
  $scope.set_language = (code) ->
    $rootScope.lan = code
    $.ajax
      data_format: "json"
      url: "/language/#{code}/"
      success: (data) ->
        data = $.parseJSON data
        location.reload true  if data.result

  $scope.la = (list_code) ->
    if $.inArray($rootScope.lan, list_code) >= 0
      $rootScope.lan
    else
      list_code[0]

  $scope.status_msg = (success) ->
    return if success is false then "msg msg-error" else "msg msg-success"

  $scope.show_message = (resource, type_msg) ->
    if type_msg
      $rootScope["#{type_msg}_message_show"] = true
      $rootScope["#{type_msg}_message_status"] = $scope.status_msg(resource.success)
      $rootScope["#{type_msg}_message_message"] = resource.message
    else
      $scope.scroll_top()
      $rootScope.message_show = true
      $rootScope.message_status = $scope.status_msg(resource.success)
      $rootScope.message_message = resource.message

   $scope.close_message = (type_msg) ->
    if type_msg
      $rootScope["#{type_msg}_message_show"] = false
    else
      $rootScope.message_show = false

  $scope.scroll_top = ->
    $("html, body").animate
        scrollTop: 0
      , "slow"

  request_with_token = 
    get: 
      method: "JSONP", 
      params: 
        token: app["token"]

  $rootScope.request_with_token = request_with_token      

  # Ajax User API Resource
  # ===================================================================
  $scope.ajaxUsersNew = $resource($rootScope.API + "/users/new.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxUsersShow = $resource($rootScope.API + "/users/show.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } } )
  $scope.ajaxUsersList = $resource($rootScope.API + "/users/list.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxUserFavorites = $resource($rootScope.API + "/favorites/list.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxUserDraft = $resource($rootScope.API + "/drafts/list.json",
    { callback: "JSON_CALLBACK" }, request_with_token )

  # Ajax Account API Resource
  # ===================================================================
  $scope.ajaxAccountUpdate = $resource($rootScope.API + "/account/update.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxAccountUpdateProfile = $resource($rootScope.API + "/account/update_profile.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxAccountUpdateAccount = $resource($rootScope.API + "/account/update_account.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxAccountUpdatePassword = $resource($rootScope.API + "/account/update_password.json",
    { callback: "JSON_CALLBACK" }, request_with_token )

  # Ajax Admin API Resource
  # ===================================================================
  $scope.ajaxHashTableList = $resource($rootScope.API + "/hash_table/list.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxHashTableNew = $resource($rootScope.API + "/hash_table/new.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxHashTableGet = $resource($rootScope.API + "/hash_table/get.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxHashTableUpdate = $resource($rootScope.API + "/hash_table/update.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxRecipesList = $resource($rootScope.API + "/recipes/list.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  
  
  return
AppCtrl.$inject = ["$scope", "$resource", "$rootScope"]