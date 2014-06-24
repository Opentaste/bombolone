'use strict';

/*
Api v4
*/
bombolone.factory('api', [
  "$rootScope", 
  "$resource", 
  "$http", 
  function($rootScope, $resource, $http) {
    var api, request_with_credentials, get_resource_by_credentials, 
    get_resource;

    request_with_credentials = {
      'get': { method: "GET" },
      'post': { method: "POST" },
      'remove': { method: "DELETE" }
    };
    
    $rootScope.request_with_token = request_with_credentials;

    get_resource_by_credentials = function(url) {
      return $resource($rootScope.API + url, {}, request_with_credentials);
    };

    get_resource = function(url) {
      return $resource($rootScope.API + url, {});
    };

    api = {
      // Account API
      accountUpdate: get_resource_by_credentials("/account/update.json"),
      accountUpdateProfile: get_resource_by_credentials("/account/update_profile.json"),
      accountUpdateAccount: get_resource_by_credentials("/account/update_account.json"),
      accountUpdatePassword: get_resource_by_credentials("/account/update_password.json"),

      // Hash Table API
      hashTableList: get_resource_by_credentials("/hash_table/list.json"),
      hashTableNew: get_resource_by_credentials("/hash_table/new.json"),
      hashTableGet: get_resource_by_credentials("/hash_table/get.json"),
      hashTableUpdate: get_resource_by_credentials("/hash_table/update.json"),

      // Lanugages API 
      languagesChange: get_resource("/languages/change.json"),

      // Pages API
      pagesList: get_resource_by_credentials("/pages/list.json"),
      pagesGet: get_resource_by_credentials("/pages/get.json"),
      pagesCreate: get_resource_by_credentials("/pages/create.json"),
      pagesUpdate: get_resource_by_credentials("/pages/update.json"),

      // Rank API
      rankShow: get_resource_by_credentials("/rank/show.json"),
      rankCreate: get_resource_by_credentials("/rank/create.json"),
      rankUpdate: get_resource_by_credentials("/rank/update.json"),

      // User API
      usersList: get_resource_by_credentials("/users/list.json"),
      usersNew: get_resource_by_credentials("/users/new.json"),
    };

    return api;
  }
]);
