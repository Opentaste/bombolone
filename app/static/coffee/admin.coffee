# Admin controller
AdminCtrl = ($scope, $resource, $rootScope, $compile) ->

  $rootScope.items_list = []

  $scope.tab_menu =
    selected: "account"


  $scope.select_tab = (tab_selected) ->
    $scope.tab_menu.selected = tab_selected


  $scope.remove = (id_item, index) ->
    $scope.id_item = id_item
    $scope.index_item = index
    $(".check_remove").removeClass "hidden"


  $scope.pop_item_from_list = (resource) ->
    $scope.items_list.splice $scope.index_item, 1


  $scope.remove_item = (check, index) ->
    if check
      params =
        "_id": $scope.id_item
        "token": app["token"]

      $scope.ajaxAdminRemoveItem = $resource($rootScope.API + "/" + $rootScope.admin_module + "/remove.json",
        { callback: "JSON_CALLBACK" }, $rootScope.request_with_token )
      
      $scope.ajaxAdminRemoveItem.get params, (resource) ->
        if resource.success
          $scope.pop_item_from_list()
        else
          alert "You can't remove this element"

    check_remove_hidden()


  check_remove_hidden = ->
    $(".check_remove").addClass "hidden"
    
  return
AdminCtrl.$inject = ["$scope", "$resource", "$rootScope"]