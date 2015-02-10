/*
	Copyright 2005 Peter Freitag - All rights reserved.
*/
// ==UserScript==
// @namespace     http://www.petefreitag.com/greasemonkey/amazon_localize
// @name          Amazon.ca Localizer
// @description   Replaces product links from amazon.com, etc. to amazon.ca
// @include       http://*
// @include		  https://*
// @exclude       http://*.amazon.*
// @exclude       https://*.amazon.*
// ==/UserScript==

(function() 
{
   var isbnReDelimited = /[^\d](\d{7,9}[\dXx])([^\dXx]|$)/;
   var links = document.getElementsByTagName("a");
   for (var i=0;i<links.length;i++) 
   {
      var href=links[i].href;
      if (href.match(/amazon\./i) && (href.match(isbnReDelimited)) ) 
      {
         try
         {
            var asin = href.match(isbnReDelimited)[1];
            GM_log('rewriting ' + href);
            links[i].href = "http://www.amazon.ca/exec/obidos/redirect?tag=dealazon-20&path=ASIN/" + asin + "/ref=";
         }
         catch ( e )
         {
            // eat the exception
            GM_log('caught exception ' + e + ' - ignoring');
         }
      }
   }
})();
