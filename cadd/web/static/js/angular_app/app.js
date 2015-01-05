'use strict';

var app = angular.module('cadd', ['cadd.services', 'cadd.directives']);

app.config(function($interpolateProvider)
{
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
app.config(['$routeProvider', '$locationProvider', function($routes, $location) {
	/*var loc = window.location.href;
	console.log("loc=", loc);    
 	if (loc.indexOf("#") != -1 &&  loc.indexOf("#!") == -1 ){
        window.location.href = loc.replace("#", "#!");
    }    
    $location.hashPrefix('!');*/
}]);
