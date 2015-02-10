// ==UserScript==
// @name        Fix WPL Port
// @namespace   http://userscripts.org/people/4764
// @description fix the bad port on WPL pages that breaks the work proxy
// @include     http://books.wpl.ca:2082/*
// ==/UserScript==
 
(function() {
   location.href = location.href.replace(/:2082/, '');
})();

