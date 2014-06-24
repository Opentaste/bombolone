'use strict';

/* Bombolone v4 */
var host, path, bombolone, protocol, qsa;
qsa = d.querySelectorAll.bind(d);
protocol = window.location.protocol;
host = window.location.host;
path = window.location.pathname;

bombolone = angular.module("bombolone", [
  'ngRoute', 
  'ngResource', 
  'ui',
]).config(function( $interpolateProvider) {
  /* $interpolateProvider 
   * we need replace {{ }} with  [[ ]]
   * */
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
})
