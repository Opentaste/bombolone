'use strict';

/*
Rank v6
*/
bombolone.controller('RankCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope", 
  "api",
  function($scope, $resource, $rootScope, api) {
    var admin_rank, admin_rank_update, rank_index, rank_new,
        rank_update;
    $scope.sort_table = $scope.$parent.lan;
    $scope.rank = {};

    rank_index = path.match(/^\/admin\/rank\/?$/i);
    rank_new = path.match(/^\/admin\/rank\/new\/?$/i);
    rank_update = path.match(/^\/admin\/rank\/update\/([^\/]+)\/?$/i);

    admin_rank = function() {
      var params;
      $rootScope.admin_module = "rank";
      params = {};
      api.rankShow.get(params, function(resource) {
        $rootScope.items_list = resource.ranks;
      });
    };

    admin_rank_update = function() {
      var params;
      params = {
        "rank-id": rank_update[1]
      }
      api.rankShow.get(params, function(resource) {
        $scope.rank = resource.rank;
      });
    };

    $scope.create_rank = function() {
      var params;
      params = {
        'name': $scope.rank.name,
        'rank': $scope.rank.rank,
      };
      api.rankCreate.post(params, function(resource) {
        $scope.show_message(resource);
      });
    };

    $scope.update_rank = function() {
      var params;
      params = {
        'rank-id': rank_update[1],
        'name': $scope.rank.name,
        'rank': $scope.rank.rank,
      };
      api.rankUpdate.post(params, function(resource) {
        $scope.show_message(resource);
      });
    };

    if (rank_index) {
      admin_rank();
    } else if (rank_new) {
      $scope.update = false;
    } else if (rank_update) {
      admin_rank_update();
      $scope.update = true;
    }
  }
]);
