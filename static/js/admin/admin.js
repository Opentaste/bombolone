'use strict';

/* Admin controller v6 */
angular.module('bombolone.controllers.admin', [])
.controller('AdminCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope", 
  "$http", 
  "$location",
  function($scope, $resource, $rootScope, $http, $location) {  
    var check_remove_hidden;
    $rootScope.items_list = [];
    $scope.dialog_show = false;

    $scope.select_tab = function(tab_selected) {
      $scope.tab_menu.selected = tab_selected;
    };

    $scope.remove = function(item_id) {
      $scope.item_id = item_id;
      $scope.dialog_show = true;
    };

    $scope.pop_item_from_list = function() {
      var i, item, _i, _len, _ref, _results;
      _ref = $scope.items_list;
      _results = [];
      for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
        item = _ref[i];
        if (item._id === $scope.item_id) {
          $scope.items_list.splice(i, 1);
          break;
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    };

    $scope.remove_item = function(check) {
      var params, url_api;
      if (check) {
        params = {
          "_id": $scope.item_id
        };
        url_api = $rootScope.API + "/" + $rootScope.admin_module + "/remove.json"
        $scope.ajaxAdminRemoveItem = $resource(url_api, {}, $rootScope.request_with_token);
        $scope.ajaxAdminRemoveItem.remove(params, function(resource) {
          if (resource.success) {
            $scope.pop_item_from_list();
          } else {
            alert("You can't remove this element");
          }
        });
      }
      check_remove_hidden();
    };
    
    check_remove_hidden = function() {
      $scope.dialog_show = false;
    };
  }
]);
