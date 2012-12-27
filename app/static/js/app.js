'use strict';

// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives', 'ui', 'ngResource']).
  config(['$routeProvider', '$interpolateProvider', function($routeProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('[['); 
    $interpolateProvider.endSymbol(']]');
  }]);

/* Services */
// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', []).
  value('version', '0.1');

/* Filters */
angular.module('myApp.filters', []).
  filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }]);

/* Directives */
angular.module('myApp.directives', []).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);

/* Controllers */
function MyCtrl1() {}
MyCtrl1.$inject = [];


function MyCtrl2() {
}
MyCtrl2.$inject = [];


//var b = {
//    msg: {
//        close_msg: function() {
//            t.get('.msg .close').on('click', function() {
//                t.get('.msg').attr('class', 'msg-hidden');
//            });
//        }
//    }
//}

function AppCtrl($scope, $resource, $rootScope) {

  $rootScope.dropdown_status = "";

  $rootScope.lan = $.data('[data-lan]', 'lan');
  $rootScope.language = $.data('[data-language]', 'language');

  $scope.clean = function() {
    $rootScope.ac_show = "";
  }

  $scope.dropdown = function(){
    if ($rootScope.dropdown_status == "open") {
      $rootScope.dropdown_status = "";
    } else {
      $rootScope.dropdown_status = "open";
    }
  }

  // Set language: there are two case:
  // 1) no sign in, so the language is saved in the cookie
  // 2) otherwise it's saved user profile
  // It's called a ajax request that if is everything fine,
  // it will reload the current page
  $scope.set_language = function(code){
    $rootScope.lan = code;
    t.ajax({
      data_format: 'json',
      url: '/language/'+code+'/', 
      success: function(data) {
        if (data.result) {
          location.reload(true);
        }
      }
    });
  }

  window.scope = angular.element(document).scope();
}
AppCtrl.$inject = ['$scope', '$resource', '$rootScope'];

