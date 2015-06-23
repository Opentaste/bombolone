'use strict';

/* Api v4 */
angular.module('bombolone.services.api', [])
.factory('api', [
  "$rootScope", 
  "$resource", 
  "$http", 
  function($rootScope, $resource, $http) {
    var api, requestWithCredentials, getResourceByCredentials, 
    getResource;

    requestWithCredentials = {
      'get': { method: "GET" },
      'post': { method: "POST" },
      'remove': { method: "DELETE" }
    };
    
    $rootScope.request_with_token = requestWithCredentials;

    getResourceByCredentials = function(url) {
      return $resource($rootScope.API + url, {}, requestWithCredentials);
    };

    getResource = function(url) {
      return $resource($rootScope.API + url, {});
    };

    api = {
      // Account API
      accountUpdate: getResourceByCredentials("/account/update.json"),
      accountUpdateProfile: getResourceByCredentials("/account/update_profile.json"),
      accountUpdateAccount: getResourceByCredentials("/account/update_account.json"),
      accountUpdatePassword: getResourceByCredentials("/account/update_password.json"),

      // Hash Table API
      hashTableList: getResourceByCredentials("/hash_table/list.json"),
      hashTableGet: getResourceByCredentials("/hash_table/get.json"),
      hashTableNew: getResourceByCredentials("/hash_table/new.json"),
      hashTableUpdate: getResourceByCredentials("/hash_table/update.json"),

      // Lanugages API 
      languagesChange: getResource("/languages/change.json"),
      languageList: getResourceByCredentials("/languages/list.json"),
      languageGet: getResourceByCredentials("/languages/get.json"),
      languageNew: getResourceByCredentials("/languages/new.json"),
      languageCreate: getResourceByCredentials("/languages/create.json"),
      languageUpdate: getResourceByCredentials("/languages/update.json"),

      // Pages API
      pagesList: getResourceByCredentials("/pages/list.json"),
      pagesGet: getResourceByCredentials("/pages/get.json"),
      pagesCreate: getResourceByCredentials("/pages/create.json"),
      pagesUpdate: getResourceByCredentials("/pages/update.json"),

      // Rank API
      rankShow: getResourceByCredentials("/rank/show.json"),
      rankCreate: getResourceByCredentials("/rank/create.json"),
      rankUpdate: getResourceByCredentials("/rank/update.json"),

      // User API
      usersList: getResourceByCredentials("/users/list.json"),
      usersNew: getResourceByCredentials("/users/new.json"),
    };

    return api;
  }
]);
