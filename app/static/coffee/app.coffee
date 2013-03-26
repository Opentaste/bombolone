# Application controller
AppCtrl = ($scope, $resource, $rootScope) ->
  $("[data-attribute=autocomplete_off]").attr "autocomplete", "off"

  $scope.clean = ->
    $rootScope.ac_show = ""

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

  $scope.change_photo = ($event) ->
    slide_up = $("body").css("overflow")
    if slide_up is "hidden"
      if $event.keyCode is 37 and $rootScope.slide_now > 0
        next = parseInt($rootScope.slide_now) - 1
        $rootScope.slide_now = next
        $rootScope.slide_power next, $rootScope.recipe_id
      else if $event.keyCode is 39 and $rootScope.slide_now < $rootScope.slide_end
        next = parseInt($rootScope.slide_now) + 1
        $rootScope.slide_now = next
        $rootScope.slide_power next, $rootScope.recipe_id

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

  # Ajax Autocomplete API Resource
  # ===================================================================
  $scope.ajaxAutocompleteListIngredients = $resource($rootScope.API + "/autocomplete/list_ingredients.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })
  $scope.ajaxAutocompleteListTags = $resource($rootScope.API + "/autocomplete/list_tags.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })
  $scope.ajaxAutocompleteListIngredientSearch = $resource($rootScope.API + "/autocomplete/list_ingredient_search.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })
  $scope.ajaxAutocompleteListTagSearch = $resource($rootScope.API + "/autocomplete/list_tag_search.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

  # Ajax Timeline API Resource
  # ===================================================================
  $scope.ajaxTimelineHome = $resource($rootScope.API + "/timeline/home.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })
  $scope.ajaxTimelineUser = $resource($rootScope.API + "/timeline/user.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

  # Ajax Search Recipes API Resource
  # ===================================================================
  $scope.ajaxSearchRecipes = $resource($rootScope.API + "/search/recipes.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

  # Ajax Recipes API Resource
  # ===================================================================
  $scope.ajaxImageView = $resource($rootScope.API + "/images/view.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })
  $scope.ajaxRecipeShow = $resource($rootScope.API + "/recipes/show.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

  # Ajax Recipes measures API Resource
  # ===================================================================
  $scope.ajaxMeasuresList = $resource($rootScope.API + "/measures/list.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

  # Ajax Recipe buttons API Resource
  # ===================================================================
  $scope.ajaxTasty = $resource($rootScope.API + "/recipes/tasty.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxFavorite = $resource($rootScope.API + "/recipes/favorite.json",
    { callback: "JSON_CALLBACK" }, request_with_token )

  # Ajax Comments API Resource
  # ===================================================================
  $scope.ajaxComments = $resource($rootScope.API + "/comments/show.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })
  $scope.ajaxCommentsAdd = $resource($rootScope.API + "/comments/add.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxCommentsRemove = $resource($rootScope.API + "/comments/remove.json",
    { callback: "JSON_CALLBACK" }, request_with_token )

  # Ajax Write Recipe API Resource
  # ===================================================================
  $scope.ajaxSaveRecipe = $resource($rootScope.API + "/recipes/save.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxPublishRecipe = $resource($rootScope.API + "/recipes/publish.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxEditRecipe = $resource($rootScope.API + "/recipes/edit.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxRecipeAddIngredient = $resource($rootScope.API + "/recipes/add_ingredient.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxRecipeAddTag = $resource($rootScope.API + "/recipes/add_tag.json",
    { callback: "JSON_CALLBACK" }, request_with_token )
  $scope.ajaxRecipesRemoveDraft = $resource($rootScope.API + "/recipes/remove_draft.json",
    { callback: "JSON_CALLBACK" }, request_with_token )

  # Ajax Ingredients API Resource
  # ===================================================================
  $scope.ajaxIngredientsList = $resource($rootScope.API + "/ingredients/list.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

  # Ajax Tags API Resource
  # ===================================================================
  $scope.ajaxTagsList = $resource($rootScope.API + "/tags/list.json",
    { callback: "JSON_CALLBACK" }, { get: { method: "JSONP" } })

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