// ==UserScript==
// @name           Automatic Livelink Login
// @namespace   http://userscripts.org/people/4764
// @description    A template for creating new user scripts from
// @include        https://livelink*mitra.com/*getLogin*
// ==/UserScript==
var inputButton = document.getElementsByTagName( 'INPUT' );
for( var i = 0; i < inputButton.length; i++ )
{
    if ( inputButton[i].className == 'saveButton' &&
            inputButton[i].getAttribute('value') == 'Log-in' &&
            inputButton[i].getAttribute('border') == '5' )
	{
		inputButton[i].click();
	}
}
