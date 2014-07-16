'use strict';

/* Users controller v4 */
angular.module('bombolone.controllers.users', [])
.controller('UsersCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope", 
  "api",
  function($scope, $resource, $rootScope, api) {
    var user_value, __init_submit;

    user_value = page["user"] || {};
    $scope.user = {
      _id: user_value["_id"] || "",
      username: user_value["username"] || "",
      email: user_value["email"] || "",
      rank: user_value["rank"] || "",
      lan: user_value["lan"] || "",
      time_zone: user_value["time_zone"] || "",
      name: user_value["name"] || "",
      location: user_value["location"] || "",
      web: user_value["web"] || "",
      description: user_value["description"] || "",
      password: "",
      password_new: "",
      password_check: "",
      image_show: user_value["image_show"] || "/static/layout/default/avatar.png",
      image_uploaded: "",
      status: user_value["status"] || 0
    };
    $scope.description_counter = 200;
    
    __init_submit = function() {
      var params;
      $rootScope.message_show = false;
      params = $scope.user;
      return params;
    };

    /* Save */
    $scope.save = function() {
      var params;
      params = __init_submit();
      api.accountUpdate.post(params, function(resource) {
        $scope.show_message(resource);
        if (resource.success) {
          $scope.user = resource.user;
        }
      });
    };

    /* New */
    $scope.create = function() {
      var params;
      params = __init_submit();
      api.usersNew.post(params, function(resource) {
        $scope.show_message(resource);
        if (resource.success) {
          $scope.user = resource.user;
        }
      });
    };

    /* Update */
    $scope.update_profile = function() {
      var params;
      params = __init_submit();
      api.accountUpdateProfile.post(params, function(resource) {
        $scope.show_message(resource);
        if (resource.success) {
          $scope.user = resource.user;
        }
      });
    };

    $scope.update_account = function() {
      var params;
      params = __init_submit();
      api.accountUpdateAccount.post(params, function(resource) {
        $scope.show_message(resource);
        if (resource.success) {
          $scope.user = resource.user;
        }
      });
    };

    $scope.update_password = function() {
      var params;
      params = __init_submit();
      api.accountUpdatePassword.post(params, function(resource) {
        $scope.show_message(resource);
        if (resource.success) {
          $scope.user = resource.user;
        }
      });
    };
  }
]);
