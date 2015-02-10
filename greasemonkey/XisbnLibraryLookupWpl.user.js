// ==UserScript==
// @name        XISBN LibraryLookup
// @namespace   http://userscripts.org/people/4764
// @description Check book availability in one or more libraries
// @include     http://*.amazon.*
// @include     http://*chapters*/*
// @include     http://*.powells.com/*
// @include     http://*allconsuming.net/item/view/*
// @include     http://*allconsuming.net/item/asin/*
// @include     http://books.google.*
// @include     http://www.goodreads.com/book/show/*
// ==/UserScript==

var versionString = "2009.03.20";
var latestChange = "fixed goodreads support";
var scriptURL = "http://blairconrad.googlecode.com/svn/trunk/greasemonkey/XisbnLibraryLookupWpl.user.js";
 
// This script was inspired by Jon Udell's userscript of similar functionality
// that he posted in his 'Further adventures in lightweight service
// composition' post of 30 January, 2006
// (http://weblog.infoworld.com/udell/2006/01/30.html).
//
// I've modified the code in the following ways: 
// - it's more understandable to me - your mileage may vary, but I found the
//   background DOM modification and associated event a little confusing
// - it works against the Waterloo Public Library instead of the Keene
//   libraries
// - it only hits XISBN if the original ISBN doesn't appear in the library
// - if no versions of the book are found in the library, that fact is noted
//   on the Amazon page
//
// The latest version of this script is always available at 
// http://blairconrad.googlecode.com/svn/trunk/greasemonkey/XisbnLibraryLookupWpl.user.js
//
// Updates:
//
// 2006.08.10
// - removed the "isn't in the library" message, since it was really just
//   there for debugging anyhow
// - added a "keepLooking" property to libraries in case we want the script to
//   keep looking for books even after it's found it in a given library. This
//   feature was suggested by the mysterious Mrs. January.
// 
// 2006.03.30
// - added Region of Waterloo Library as last-checked library
// 
// 2006.03.20
// - Bugfixes, thanks to Kevin Yezbick's sharp eyes
//   - better detection of whether books are at the WPL & KPL
//   - persisting extra ISBN list until all libraries have been checked 
// - updated ISBN & title detection at Chapters
// 
// 2006.03.15
// - added support for fallback libraries - if the book isn't found
//   in the library, look in others. This could still use some work,
//   since we're relooking up the XISBNs
// - added fallback library of Kitchener Public Library
// - added support for Google Books, as requested by Kevin Yezbick
//
// 2006.03.09, later on
// - added All Consuming
//
// 2006.03.09
// - fixed broken ISBN detection on Powells
// 
// 2006.03.08
// - Added builtin support for Powells web pages (a US bookseller)
// - Fixed up some logs. A little.
//
// 2006.03.05
// - split 'source page' (formerly Amazon site) functionality into separate objects
//   and added builtin support for Chapters web pages (a Canadian bookseller)

(
   // Settings ------------------------------------------------------------------
   
   function()
   {
      function Settingsobject(namespace)
      {
         this.prefix = namespace ? namespace + '.'  : "";
         this.default={};
      };
         
      Settingsobject.prototype.set = function(name, value)
      {
         if ( typeof value == "boolean" )
            value = value ? "{b}1" : "{b}0";
         else if ( typeof value == "string" )
            value = "{s}" + value;
         else if ( typeof value == "number" )
            value = "{n}" + value;
         else
            value = "{o}" + value.toSource();
         GM_setValue(this.prefix+""+name, value);
      };
      
      Settingsobject.prototype.get = function(name)
      {
         var value=GM_getValue(this.prefix+""+name, this.default[name] || "{b}0");
         if ( !value.indexOf )
            return value;
         if ( value.indexOf("{o}")==0 )
         {
            try
            {
               return eval("("+value.substr(3)+")");
            }
            catch ( e ) 
            {
               GM_log("Error while calling variable " + name + 
                      " while translating into an object: \n\n" + e +
                      "\n\ncode:\n"+value.substr(3))
                  return false;
            }
         }
         
         if ( value.indexOf("{b}") == 0 )
            return !!parseInt(value.substr(3));
         if ( value.indexOf("{n}") == 0 )
            return parseFloat(value.substr(3));
         if ( value.indexOf("{s}") == 0 )
            return value.substr(3);
         return value;
      };
         
      Settingsobject.prototype.register = function(name, defaultvalue)
      {
         this.default[name]=defaultvalue;
         return true;
      };
         
      // End Settings --------------------------------------------------------------

      var globalSettings = new Settingsobject('global');
      
      function checkForNewerScript()
      {
         var localLastModified = globalSettings.get('script-last-modified');
         
         headers = {};
         // GM_log('forceVersionCheck: ' + forceVersionCheck);
         if ( ! forceVersionCheck )
         {
            headers['Cache-Control'] = 'max-age=86400';
            if ( localLastModified )
            {
               headers['If-Modified-Since'] = localLastModified;
            }
         }
         
         // GM_log('headers: ' + headers['Cache-Control'] + ' ' + headers['If-Modified-Since']);
         GM_xmlhttpRequest(
         {
           method: 'GET', url: scriptURL, 
                      headers: headers,
                      
                      onload: function(response) 
                      {
                         var serverLastModified;
//                          GM_log('status: ' + response.status + 
//                                 '\r\nheaders:\r\n' + response.responseHeaders);
                         response.responseHeaders.split('\n').forEach(
                            function (t)
                            {
                               header = t.split(': ');
                               if ( header[0] == 'Last-Modified' )
                               {
                                  serverLastModified = header[1];
                               }
                            });
                         if ( ! forceVersionCheck && response.status == 304 )
                         {
                            GM_log('script returned from cache - no need to update');
                            return;
                         }
                         
                         GM_log('server: ' + serverLastModified + ', local: ' + localLastModified);
                         
                         globalSettings.set('script-last-modified', serverLastModified);
                         
                         if ( ! forceVersionCheck && localLastModified == serverLastModified )
                         {
                            GM_log('last modified is same!');
                            return;
                         }
                         
                         responseArray = response.responseText.split('\n');
                         for ( line in responseArray ) 
                         {
                            if ( responseArray[line].match('var versionString = ') ) 
                            {
                               var serverVersion = responseArray[line].split('"')[1];
                               GM_log('server version: ' + serverVersion + 
                                      ', local version = ' + versionString);
                               
                               if ( serverVersion == versionString )
                               {
                                  GM_log('no need to update');
                               }
                               else
                               {
                                  try
                                  {
                                     line = parseInt(line) + 1;
                                     latestChange = responseArray[line].split('"')[1];
                                  }
                                  catch  ( e )
                                  {
                                     latestChange = "can't determine latest change";
                                  }
                                  GM_log('latest change = ' + latestChange);
                                  notifyOfNewVersion(latestChange);
                               }
                               break;
                            }
                         }
                      }
                      }
            );
      };

      function notifyOfNewVersion(latestChange)
      {
         GM_registerMenuCommand('XISBN: update script', function() {
            location.href = scriptURL;
         });
      };
         
      function makeMenuToggle(key, defaultValue, toggleOn, toggleOff, prefix)
      {
         // Load current value into variable
         window[key] = GM_getValue(key, defaultValue);
         // Add menu toggle
         GM_registerMenuCommand((prefix ? prefix+": " : "") + (window[key] ? toggleOff : toggleOn), function() {
            GM_setValue(key, !window[key]);
            location.reload();
         });
      };

      function addMenuCommands()
      {
         makeMenuToggle("forceVersionCheck", false, "Always do full check for newer script", "Cache script to avoid pounding server", "XISBN");
      };
      
      function $x(path, context) 
      {
         if ( !context ) 
         {
            context = document;
         }
         var result = [];
         var xpr = document.evaluate(path, context, null,
                                     XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
         for (var i = 0; item = xpr.snapshotItem(i); i++)
         {
            result.push(item);
         }
         return result;
      };
         
      var xisbnQuery = 'http://old-xisbn.oclc.org/webservices/xisbn/';
      
      var isbnREdelimited = /[^\d](\d{9,12}[\dXx])([^\dXx]|$)/;
      
      var extraIsbns = [];

      // Libraries -----------------------------------------------------------

      var waterlooRegion =
         {
            name: 'Region of Waterloo Library',

            createSearchUrl: function(isbn)
            {
               var prefix = 'http://www.regionofwaterloo.canlib.ca/uhtbin/cgisirsi/uOtJAQjVct/HEADQUARTR/x/5/0/?searchdata1=';
               return prefix + isbn
                  },
            
            // Get the results of a lookup - mark up the page and return true
            // if there's a hit, otherwise return false.
            processLookup: function(isbn, results)
            {
               var notFound = /found no matches in the library you searched/;

               page = results.responseText;
               if ( notFound.test(page) )
               { 
                  GM_log('couldn\'t find ' + isbn + ' at the ' + this.name);
                  return false;
               }
               else
               {
                  return true;
               }
            },
            
         } // end waterlooRegion

      var wpl = 
         {
            name: 'Waterloo Public Library',

            createSearchUrl: function(isbn)
            {
               var prefix = 'http://books.wpl.ca/search/?searchtype=i&searcharg=';
               var suffix = '&searchscope=3&SORT=D&extended=0&SUBMIT=Search&searchlimits=';
               return prefix + isbn + suffix;
            },
            
            // Get the results of a lookup - mark up the page and return true
            // if there's a hit, otherwise return false.
            processLookup: function(isbn, results)
            {
               var notFound = /No matches found; nearby ISBN[/]ISSN/;

               page = results.responseText;
               if ( notFound.test(page) )
               { 
                  GM_log('couldn\'t find ' + isbn + ' at the ' + this.name);
                  return false;
               }
               else
               {
                  return true;
               }
            },
            
         } // end wpl

      var kpl = 
         {
            name: 'Kitchener Public Library',
            createSearchUrl: function(isbn)
            {
               var prefix = 'http://books.wpl.ca/search/?searchtype=i&searcharg=';
               var suffix = '&searchscope=1&SORT=D&extended=0&SUBMIT=Search&searchlimits=';
               return prefix + isbn + suffix;
            },

            // the Kitchener Public Library shares a catalog with the WPL, so
            // just copy their processLookup
            processLookup: wpl.processLookup,
         } // end kpl

      // End of Libraries ----------------------------------------------------

      // Figure out which site the source page comes from.
      // To add a new one, make a new block like the "chapters"
      // and "amazon" variables below, and extend the "if...else..."
      // block at the bottom of this function.
      function whichSiteIsThis()
      {
         var chapters =
            {
               getIsbn: function()
               {
                  try
                  {
                     return location.href.match(isbnREdelimited)[1];
                  }
                  catch ( e ) 
                  {
                     return null;
                  }
               },

               getOriginalTitle: function()
               {
                  return $x("//h1")[0];
               }
            }
      
         var allconsuming =
            {
               getIsbn: function()
               {
                  var isbn = null;
                  isbnLinkNode = $x("//div[@class='item-header-body']/a[@class='amazon-link']/@href")[0];
                  if ( isbnLinkNode )
                  {
                     isbn = isbnLinkNode.firstChild.nodeValue.match(isbnREdelimited)[1];
                  }
                  return isbn;
               },

               getOriginalTitle: function()
               {
                  return $x("//div[@class='item-header-body']/strong")[0];
               }
            }
      
         var amazon =
            {
               getIsbn: function()
               {
                  try
                  {
                     return location.href.match(isbnREdelimited)[1];
                  }
                  catch ( e ) 
                  {
                     return null;
                  }
               },

               getOriginalTitle: function()
               {
                  return $x("//div[@class='buying']/b[@class='sans']|//div[@class='buying']/b[@class='asinTitle']|//div[@class='buying']//span[@id='btAsinTitle']")[0];
               }
            }
      
         var librarything =
            {
               getIsbn: function()
               {
                  var isbn = null;
                  isbnLinkNode = $x("//div[@class='isbn']/a")[0];
                  if ( isbnLinkNode )
                  {
                     isbn = isbnLinkNode.firstChild.nodeValue.substr(5);
                  }
                  return isbn;
               },

               getOriginalTitle: function()
               {
                  return $x("//div[@id='usercover']")[0];
               }
            }
      
         var powells =
            {
               getIsbn: function()
               {
                  try
                  {
                     return location.href.match(isbnREdelimited)[1];
                  }
                  catch ( e ) 
                  {
                     return null;
                  }
               },

               getOriginalTitle: function()
               {
                  return $x("//div[@id='seemore']")[0];
               }
            }
      
         var googleBooks =
            {
               getIsbn: function()
               {
                  try
                  {
                     return location.href.match(/(\d{9,12}[\dXx])/)[1];
                  }
                  catch ( e ) 
                  {
                     return null;
                  }
               },

               getOriginalTitle: function()
               {
                  return $x("//span[@class='title']")[0];
               }
            }
      
         var goodReads =
            {
               getIsbn: function()
               {
                  try
                  {
                     var isbnHeaderNodeCandidates = $x("//div[@class='infoBoxRowTitle']");
                     
                     for ( var i = 0; i < isbnHeaderNodeCandidates.length; i++ )
                     {
                        if ( isbnHeaderNodeCandidates[i].innerHTML.match(/isbn/) )
                        {
                            var isbnNode = isbnHeaderNodeCandidates[i].nextSibling;
                            while ( isbnNode.nodeName != 'DIV' )
                            {
                                isbnNode = isbnNode.nextSibling;
                            }
                            var isbnText = isbnNode.innerHTML.match(isbnREdelimited)[1];
                            return isbnText;
                        }
                     }
                  }
                  catch ( e ) 
                  {
                     GM_log('error looking for ISBN: ' + e);
                  }
                  return null;
               },

               getOriginalTitle: function()
               {
                  return $x("//h1[@id='bookPageTitle']")[0];
               }
            }
      
         // figure out what site we're looking at
         if ( location.href.match(/chapters/) )
         {
            return chapters;
         }
         else if ( location.href.match(/allconsuming/) )
         {
            return allconsuming;
         }
         else if ( location.href.match(/powells/) )
         {
            return powells;
         }
         else if ( location.href.match(/google/) )
         {
            return googleBooks;
         }
         else if ( location.href.match(/goodreads/) )
         {
            return goodReads;
         }
         else if ( location.href.match(/librarything/) )
         {
            return librarything;
         }
         else
         {
            // Amazon's pretty popular - make it the default
            return amazon;
         }
      }

      // ---------------------------------------------------------------------
      var xisbnCache =
         {
            cache: {},
            
            get: function(isbn)
            {
               if ( null == this.cache[isbn] )
               {
                  return null;
               }
               else
               {
                  return this.cache[isbn].copy();
               }
            },

            set: function(isbn, isbns)
            {
               if ( ! isbns )
               {
                  GM_log('asked to cache nonsensical list of isbns');
                  isbns = [];
               }
               else
               {
                  // remove the first isbn from the list - it will be the same as
                  // the key 
                  isbns.shift();
               }

               if ( ! isbns )
               {
                  isbns = [];
               }

               GM_log('caching ' + isbns.length + ' items: [' + isbns + '] for ' + isbn);
               this.cache[isbn] = isbns.copy();
               return this.get(isbn);
            }
         }

      // ---------------------------------------------------------------------

      var isbnLibraryCache =
         {
            // cache: {},
            get: function(originalIsbn, library)
            {
               var foundValue = GM_getValue(originalIsbn + '/' + library.name);
               if ( undefined === foundValue )
               {
                  GM_log('no cached location for isbn ' + originalIsbn + ' in ' + library.name);
                  return null;
               }
               else
               {
                  GM_log('found cached location for isbn ' + originalIsbn + ' in ' + library.name);
                  return foundValue;
               }
            },

            set: function(originalIsbn, library, isbn)
            {
               GM_log('adding cached location for original ISBN ' + originalIsbn + ' as ' + isbn + ' in ' + library.name);
               GM_setValue(originalIsbn + '/' + library.name, isbn);
            }
         }

      // ---------------------------------------------------------------------
      var libraryLookup = 
         {
            originalTitle: null,
            infoSpan: null,

            getLibrary: function()
            {
               return this.libraries[0];
            },

            popLibrary: function()
            {
               if ( this.libraries )
               {
                  this.libraries.shift();
               }
            },

            addMessage: function(content)
            {
               if ( ! this.infoSpan )
               {
                  this.infoSpan = document.createElement("span");
                  this.originalTitle.appendChild(this.infoSpan);
               }
               
               var newSpan = document.createElement("span");
               newSpan.innerHTML = '<br>' + content;
               this.infoSpan.appendChild(newSpan);
            },

            replaceLastMessage: function(content)
            {
               var lastMessage = this.infoSpan.lastChild;
               lastMessage.innerHTML = '<br>' + content;
            },

            removeLastMessage: function()
            {
               this.infoSpan.removeChild(this.infoSpan.lastChild);
            },

            // Look up the alternate isbns for this one.  Store the results in
            // extraIsbns and start looking them up.
            lookUpAlternates: function(isbn)
            {
               alts = xisbnCache.get(isbn);
               if ( alts )
               {
                  extraIsbns = alts;
                  libraryLookup.keepLooking();
                  return;
               }
                  
               GM_log('loading extra ISBNs for ' + isbn);
               GM_xmlhttpRequest
                  (
                  {
                    method:  'GET',
                                url:     xisbnQuery + isbn,
                                onload:  function(results)
                                {
                                   var parser = new DOMParser();
                                   var xmlDoc = parser.parseFromString(results.responseText, "application/xml");
                                   var foundIsbnNodes = xmlDoc.getElementsByTagName('isbn');
                                   var foundIsbns = new Array();
                                   for (var i = 0; i < foundIsbnNodes.length; i++)
                                   {
                                      foundIsbns.push(foundIsbnNodes[i].firstChild.nodeValue);
                                   }
                                   
                                   extraIsbns = xisbnCache.set(isbn, foundIsbns);
                                   
                                   GM_log('extra ISBNs = ' + extraIsbns);
                                   libraryLookup.keepLooking();
                                }
                                }
                     );
            },

            // Lookup ISBNs from the libraryLookup.extraIsbns list. If there
            // aren't any extra ISBNs left, give up in disgust. Otherwise, try
            // the first ISBN. If it doesn't work out, call keepLooking again.
            keepLooking: function()
            {
               if ( 0 == extraIsbns.length && 1 == this.libraries.length )
               {
                  GM_log('giving up');
                  libraryLookup.removeLastMessage();
                  return;
               }
               else if ( 0 == extraIsbns.length )
               {
                  GM_log('time to try a new library');
                  libraryLookup.removeLastMessage();
                  this.popLibrary();
                  extraIsbns = null;
                  this.lookupBook(originalIsbn);
                  return;
               }

               var isbn = extraIsbns.shift();

               // look up the next book
               GM_xmlhttpRequest
                  (
                  {
                    method:  'GET',
                                url:     libraryLookup.getLibrary().createSearchUrl(isbn),
                                onload:  function(results)
                                {
                                   var found = libraryLookup.getLibrary().processLookup(isbn, results);
                                   if ( found )
                                   {
                                      var library = libraryLookup.getLibrary();
                                      libraryLookup.foundIt(libraryLookup.getLibrary(), isbn);
                                   }
                                   else
                                   {
                                      libraryLookup.keepLooking();
                                   }
                                }
                                }
                     )
                  },

            foundIt: function(library, isbn)
            {
               libraryLookup.replaceLastMessage('<a href="' +
                                                library.createSearchUrl(isbn) +
                                                '">Hey! The ' +
                                                library.name + 
                                                ' has this!');
               GM_log('found ' + isbn + ' in the ' + library.name );
               isbnLibraryCache.set(originalIsbn, library, isbn);
               if ( library.keepLooking )
               {
                  libraryLookup.popLibrary();
                  libraryLookup.lookupBook(isbn);
               }
            },

            // Look up an original ISBN - if this fails, fall back to the
            // alternate ISBNs provided by xisbn
            lookupBook: function(isbn)
            {
               GM_log('looking up ' + isbn + ' in the cache');
               cachedInfo = isbnLibraryCache.get(isbn, this.getLibrary());
               GM_log('found ' + cachedInfo);

               GM_log('looking up ' + isbn + ' in the ' + this.getLibrary().name);
               this.addMessage('looking in the ' + this.getLibrary().name);
               GM_xmlhttpRequest
                  (
                  {
                    method:  'GET',
                                url:     libraryLookup.getLibrary().createSearchUrl(isbn),
                                onload:  function(results)
                                {
                                   var found = libraryLookup.getLibrary().processLookup(isbn, results);
                                   if ( found )
                                   {
                                      libraryLookup.foundIt(libraryLookup.getLibrary(), isbn);
                                   }
                                   else
                                   {
                                      libraryLookup.lookUpAlternates(isbn);
                                   }
                                }
                                }
                     )
                  },
         } // end of libraryLookup


      var theSite = whichSiteIsThis();

      originalIsbn = theSite.getIsbn();
      GM_log('originalIsbn = ' + originalIsbn);
      if ( originalIsbn )
      {
         GM_log('found isbn = "' + originalIsbn + '" on source page');
      }
      else
      {
         return;
      }

      libraryLookup.originalTitle = theSite.getOriginalTitle();
      if ( ! libraryLookup.originalTitle )
      { 
         GM_log("couldn't find the original title");
         return;
      }

      // make sure we can copy arrays
      if ( typeof Array.prototype.copy==='undefined' ) 
      {
         Array.prototype.copy = function() 
         {
            var newArray = [];
            var i = this.length;
            while( i-- ) 
            {
               newArray[i] = typeof this[i].copy !== 'undefined' ? this[i].copy() : this[i];
            }
            return newArray;
         };
      }

      // Customizable settings ================================================

      // Modify this list to add, delete, or change order in which libraries
      // are checked
      libraryLookup.libraries = [wpl, waterlooRegion, kpl];

      // By default, once a book is found in a library, the script will stop
      // looking. If you want to keep looking after a book is found, set the
      // "keepLooking" property on a library to true. For example, if a book
      // is found in the Waterloo Public Library, I want this script to stop
      // looking for it, so I don't set the property on the wpl
      // object. However, if a book isn't in the WPL, I want to know if it's
      // in the Kitchener Public Library, the Region of Waterloo Library, or
      // both, so I set keepLooking to true on the kpl object. There's no need
      // to alter the setting of the waterlooRegion object, since it's the
      // last one in my list anyhow - there's nowhere else to go.

      kpl.keepLooking = true;

      // =====================================================================

      addMenuCommands();
      checkForNewerScript();

      libraryLookup.lookupBook(originalIsbn);

   }
   )();
