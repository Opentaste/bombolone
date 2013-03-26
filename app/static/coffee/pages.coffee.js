var pages = {
    init_language: function() {  
        
        // Main element to change language
        var button_languages = t.get('.button-lng');
        var list_languages_in_menu = t.get('.dropdown-lng .dropdown-menu li');

    },
    number_of_label: 0,
    code_languages: [],
    name_languages: {},
    init_change_name_label: function() {

        t.get('.name_label').on('keyup', function(e) {
            var label_press = e.currentTarget
            var label_value = label_press.value
            var label_num = label_press.className.split('_')[4]
            t.get('.label_en_name_' + label_num).value(label_value);
            t.get('.label_it_name_' + label_num).value(label_value);
        });

    }
}

function PagesCtrl($scope, $resource, $rootScope) {

    $scope.menu_language = false;
    $scope.tab_language = $rootScope.lan;
    $scope.name_language = $rootScope.language;

    $scope.list_labels = [];

    $("[data-toggle=dropdown]").blur(function(){
        $scope.menu_language = false;
    })

    $scope.menu_reveal = function(){
        $scope.menu_language = !$scope.menu_language;
    }

    $scope.change_language = function(code, name_language) {
        $scope.tab_language = code;
        $scope.name_language = name_language;
    }

    $scope.add_label = function(){
        var label = {
            "type": 1
        };
        $scope.list_labels.push(label);
    }

    $scope.change_label = function(index, type){
        console.log(index+'   '+type)
        $scope.list_labels[index]['type'] = type;
    }

    $scope.remove_label = function(index){
        console.log(index)
        $scope.list_labels.splice(index, 1);
    }
}
PagesCtrl.$inject = ['$scope', '$resource', '$rootScope'];
