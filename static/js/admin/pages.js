'use strict';

angular.module('bombolone.controllers.pages', [])
.controller('PagesCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope", 
  "api",
  function($scope, $resource, $rootScope, api) {
    var LANGUAGES, page_list, page_new, page_view, page_update, params;
    LANGUAGES = {
        "ru" : "",
        "fr" : "",
        "en" : "",
        "cn" : "",
        "pt" : "",
        "no" : "",
        "jp" : "",
        "de" : "",
        "tr" : "",
        "it" : "",
        "ar" : "",
        "es" : "",
        "gr" : ""
    }
    $rootScope.admin_module = "pages";
    page_new = path.match(/^\/admin\/pages\/new\/?$/i);
    page_update = path.match(/^\/admin\/pages\/update\/([^\/]+)\/?$/i);
    page_view = path.match(/^\/admin\/pages\/view\/([^\/]+)\/?$/i);
    page_list = path.match(/^\/admin\/pages\/?$/i);
    $scope.module = "pages";
    $scope.menu_language = false;
    $scope.code_language = $rootScope.lan;
    $scope.name_language = $rootScope.language;
    $scope.list_labels = [];
    $scope.update = true;
    $scope.view = false;
    if (page_list) {
      $rootScope.loader = true;
      api.pagesList.get(function(resource) {
        $rootScope.loader = false;
        $rootScope.items_list = resource.page_list;
        $scope.show_item_list = true;
      });
    } else if (page_update) {
      $scope.page_id = page_update[1];
      params = {
        _id: $scope.page_id
      };
      api.pagesGet.get(params, function(resource) {
        $rootScope.page = resource.page;
      });
    } else if (page_view) {
      $scope.view = true;
      $scope.page_id = page_view[1];
      params = {
        _id: $scope.page_id
      };
      api.pagesGet.get(params, function(resource) {
        $rootScope.page = resource.page;
      });
    } else if (page_new) {
      $scope.update = false;
      $scope.page = {
        "name": "",
        "from": "",
        "import": "",
        "url": LANGUAGES,
        "title": LANGUAGES,
        "description": LANGUAGES,
        "content": [],
        "file": "",
        "labels": []
      };
    };
    //$("[data-toggle=dropdown]").blur(function() {
    //  $scope.menu_language = false;
    //});
    $scope.menu_reveal = function() {
      $scope.menu_language = !$scope.menu_language;
    };
    $scope.change_language = function(code, name_language) {
      $scope.code_language = code;
      $scope.name_language = name_language;
      $scope.menu_reveal();
    };
    $scope.add_label = function() {
      var content_item, label_item;
      label_item = {
        "name": "",
        "type": "text"
      };
      content_item = {
        "alias": LANGUAGES,
        "value": LANGUAGES
      };
      $scope.page.labels.push(label_item);
      $scope.page.content.push(content_item);
    };
    $scope.remove_label = function(index) {
      $scope.page.labels.splice(index, 1);
      $scope.page.content.splice(index, 1);
    };
    $scope["new"] = function() {
      var paramas;
      $rootScope.message_show = false;
      paramas = $scope.page;
      paramas["token"] = app["token"];
      api.pagesCreate.save(paramas, function(resource) {
        $scope.show_message(resource);
        $rootScope.page = resource.page;
        $scope.page_id = resource.page._id;
        $scope.update = true;
      });
    };
    $scope.save = function() {
      var paramas;
      $rootScope.message_show = false;
      paramas = $scope.page;
      paramas["_id"] = $scope.page_id;
      paramas["token"] = app["token"];
      api.pagesUpdate.save(paramas, function(resource) {
        $scope.show_message(resource);
      });
    };
  }
]);