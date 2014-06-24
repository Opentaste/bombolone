'use strict';

/*
Application controller v5
*/
bombolone.controller('AppCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope", 
  "$http", 
  "$location", 
  function($scope, $resource, $rootScope, $http, $location) {
    var scrollTo;
    
    $rootScope.API = app["base_url"] + '/api/1.0';
    $rootScope.ac_show = "";
    $rootScope.ac_tag_show = "";
    $rootScope.dropdown_status = "";
    $rootScope.message_show = page["message_show"] || false;
    $rootScope.message_status = page["message_status"] || "";
    $rootScope.message_message = page["message_message"] || "";
    $rootScope.message_icon = "x";
    $rootScope.loader = false;
    $rootScope.username = app["username"];
    $rootScope.lan = app["lan"];
    $rootScope.language = app["language"];
    $rootScope.location = $location;
    $rootScope.list_code = ["en", "it"];
    $rootScope.all_the_languages = app["all_the_languages"];
    window.scope = angular.element(d).scope();  

    $scope.clean = function() {
      return $rootScope.ac_show = "";
    };

    $scope.dropdown = function() {
      if ($rootScope.dropdown_status === "open") {
        return $rootScope.dropdown_status = "";
      } else {
        return $rootScope.dropdown_status = "open";
      }
    };

    $scope.status_msg = function(success) {
      if (success === false) {
        return "msg msg-error";
      } else {
        return "msg msg-success";
      }
    };

    $scope.show_message = function(resource, type_msg, stop_scroll) {
      if (!stop_scroll) {
        $scope.scroll_top();
      }
      if (type_msg) {
        $rootScope["" + type_msg + "_message_show"] = true;
        $rootScope["" + type_msg + "_message_status"] = $scope.status_msg(resource.success);
        if (resource.success) {
          $rootScope["" + type_msg + "_message_message"] = resource.message;
        } else{
          $rootScope["" + type_msg + "_message_message"] = resource.errors[0].message;
        }
      } else {
        $rootScope.message_show = true;
        $rootScope.message_status = $scope.status_msg(resource.success);
        if (resource.success) {
          $rootScope.message_message = resource.message;
        } else{
          $rootScope.message_message = resource.errors[0].message;
        }
      }
    };

    $scope.close_message = function(type_msg) {
      if (type_msg) {
        $rootScope["" + type_msg + "_message_show"] = false;
      } else {
        $rootScope.message_show = false;
      }
    };

    scrollTo = function(element, to, duration) {
      var difference, perTick;
      if (duration < 0) {
        return;
      }
      difference = to - element.scrollTop;
      perTick = difference / duration * 10;
      setTimeout((function() {
        element.scrollTop = element.scrollTop + perTick;
        scrollTo(element, to, duration - 10);
      }), 10);
    };

    $scope.scroll_top = function() {
      return scrollTo(document.body, 0, 400);
    };
  }
]);
