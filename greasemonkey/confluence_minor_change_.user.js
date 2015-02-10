// ==UserScript==
// @name           confluence minor change by default
// @namespace      http://userscripts.org/people/4764
// @include        http://wikihealthcare.agfa.net/pages/editpage.action?*
// ==/UserScript==

// <input id="minorEdit" type="checkbox" name="minorEdit" value="true"  />
document.getElementById('minorEdit').checked = true;
