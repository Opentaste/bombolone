function AdminCtrl($scope, $resource, $rootScope) {

  $scope.tab_menu = {
    "selected": "account"
  }

  $scope.select_tab = function(tab_selected){
    $scope.tab_menu.selected = tab_selected;
  }

  $scope.remove = function(id_item) {
    $scope.id_item = id_item;
    $('.check_remove').removeClass('hidden');
  }

  $scope.remove_item = function(check) {
    if (check) {
      $.ajax({
        'url': '/admin/' + $scope.module + '/remove/' + $scope.id_item + '/',
        'success': function(data) {
            if (data == 'ok') {
              $('[data-item=' + $scope.id_item + ']').remove();
            }
        }
      });
    }
    check_remove_hidden();
  }

  var check_remove_hidden = function() {
    $('.check_remove').addClass('hidden');
  }
}
AdminCtrl.$inject = ['$scope', '$resource', '$rootScope'];
