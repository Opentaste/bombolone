# Main element to change language
PagesCtrl = ($scope, $resource, $rootScope) ->
  $scope.module = "pages";
  $scope.menu_language = false
  $scope.tab_language = $rootScope.lan
  $scope.name_language = $rootScope.language
  $scope.list_labels = []
  $("[data-toggle=dropdown]").blur ->
    $scope.menu_language = false

  $scope.menu_reveal = ->
    $scope.menu_language = not $scope.menu_language

  $scope.change_language = (code, name_language) ->
    $scope.tab_language = code
    $scope.name_language = name_language

  $scope.add_label = ->
    label = type: 1
    $scope.list_labels.push label

  $scope.change_label = (index, type) ->
    console.log index + "   " + type
    $scope.list_labels[index]["type"] = type

  $scope.remove_label = (index) ->
    console.log index
    $scope.list_labels.splice index, 1
    
pages =
  init_language: ->
    button_languages = t.get(".button-lng")
    list_languages_in_menu = t.get(".dropdown-lng .dropdown-menu li")

  number_of_label: 0
  code_languages: []
  name_languages: {}
  init_change_name_label: ->
    t.get(".name_label").on "keyup", (e) ->
      label_press = e.currentTarget
      label_value = label_press.value
      label_num = label_press.className.split("_")[4]
      t.get(".label_en_name_" + label_num).value label_value
      t.get(".label_it_name_" + label_num).value label_value


PagesCtrl.$inject = ["$scope", "$resource", "$rootScope"]