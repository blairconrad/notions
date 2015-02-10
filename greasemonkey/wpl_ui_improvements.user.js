// ==UserScript==
// @name           WPL UI improvements
// @namespace   http://userscripts.org/people/4764
// @description    sorts Waterloo Public Library hold and item tables by status or date, renders dates as yyyy-mm-dd, and autosubmits forms
// @include        http://books.wpl.ca/*
// ==/UserScript==

// Functions in here blatantly ripped off from the sorttable dynamic table sorting code.
// http://kryogenix.org/code/browser/sorttable/
// Simplifications have been made to accommodate the fact that I didn't need the full complexity 
// of the dynamic sorting.

(function()
{
   var myName = 'Blair Conrad';
   var myFavouriteLocation = 'wm   ';
   var FREEZE_COLUMN_INDEX = 5;

   // ------------------------------------------------------------------------

   function ts_getInnerText(el) 
   {
      if (typeof el == "string") return el;
      if (typeof el == "undefined") { return el };
      if (el.innerText) return el.innerText;	//Not needed but it is faster
      var str = "";
	
      var cs = el.childNodes;
      var l = cs.length;
      for (var i = 0; i < l; i++) {
         switch (cs[i].nodeType) {
            case 1: //ELEMENT_NODE
               str += ts_getInnerText(cs[i]);
               break;
            case 3:	//TEXT_NODE
               str += cs[i].nodeValue;
               break;
         }
      }
      return str;
   }

   function ts_resortTable(table, column, sortFunction) 
   {
      // get the span
      var td = xpath("tr/td[" + column + "]", table).snapshotItem(0);
      // Work out a type for the column
      if (table.rows.length <= 1) return;
      var itm = ts_getInnerText(table.rows[1].cells[column]);
      SORT_COLUMN_INDEX = column;
      var firstRow = new Array();
      var newRows = new Array();
      for (i=0;i<table.rows[0].length;i++) { firstRow[i] = table.rows[0][i]; }
      for (j=1;j<table.rows.length;j++) { newRows[j-1] = table.rows[j]; }
    
      newRows.sort(sortFunction);
    
      // We appendChild rows that already exist to the tbody, so it moves them rather than creating new ones
      // don't do sortbottom rows
      for (i=0;i<newRows.length;i++) { if (!newRows[i].className || (newRows[i].className && (newRows[i].className.indexOf('sortbottom') == -1))) table.tBodies[0].appendChild(newRows[i]);}
      // do sortbottom rows only
      for (i=0;i<newRows.length;i++) { if (newRows[i].className && (newRows[i].className.indexOf('sortbottom') != -1)) table.tBodies[0].appendChild(newRows[i]);}
   }
   
   function getParent(el, pTagName) {
      if (el == null) return null;
      else if (el.nodeType == 1 && el.tagName.toLowerCase() == pTagName.toLowerCase())	// Gecko bug, supposed to be uppercase
         return el;
      else
         return getParent(el.parentNode, pTagName);
   }

   function statusToScore(st)
   {
      if ( ! st )
      {
         st = '';
      }

      if ( st.match(/Ready/) )
      {
         return -100;
      }
      else if ( st.match(/IN TRANSIT/) )
      {
         return -80;
      }

      var score = parseFloat(st);
      if ( isNaN(score) )
      {
         return 0;
      }
      return score;
   }

   function isChecked(cell) {
      var attributes = cell.firstChild.attributes;
      if ( attributes )
      {
         for ( var i = 0; i < attributes.length; ++i )
         {
            if ( attributes[i].name == 'checked' )
            {
               return true;
            }
         }
      }
      return false;
   }

   function sortHoldStatus(row1, row2) { 
      row1Status = ts_getInnerText(row1.cells[SORT_COLUMN_INDEX]);
      row2Status = ts_getInnerText(row2.cells[SORT_COLUMN_INDEX]);

      row1Checked = isChecked(row1.cells[FREEZE_COLUMN_INDEX]);
      row2Checked = isChecked(row2.cells[FREEZE_COLUMN_INDEX]);

      if ( row1Checked && !row2Checked )
      {
         return 1;
      }
      else if ( row2Checked && ! row1Checked )
      {
         return -1;
      }
      
      row1Score = statusToScore(row1Status);
      row2Score = statusToScore(row2Status);
      return row1Score - row2Score;
   }

   function sortDue(a,b) { 
      a = ts_getInnerText(a.cells[SORT_COLUMN_INDEX]);
      b = ts_getInnerText(b.cells[SORT_COLUMN_INDEX]);

      if ( a < b )
      {
         return -1;
      }
      else if ( b < a )
      {
         return 1;
      }
      else
      {
         return 0;
      }

   }

   function xpath(query, node) 
   {
      return document.evaluate(query, node, null,
                               XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
   }

   function fixupTableDates(table, column)
   {
      for ( j=1; j < table.rows.length; j++ ) 
      {
      //var itm = ts_getInnerText(table.rows[1].cells[column]);
         var cell = table.rows[j].cells[column];
         cell.innerHTML = ts_getInnerText(cell).replace(/([0-9][0-9])-([0-9][0-9])-([0-9][0-9])/, 
         function(str, month, day, year, offset, s) {
                                                       return '20' + year + '.' + month + '.' + day;});
      }
    }
    
   function fixupTable()
   {
      infoTable = xpath(".//table[@class='patFunc']", document).snapshotItem(0);
      if ( ! infoTable )
      {
         return;
      }
   
      // remove the first row
      firstRow = xpath(".//tr[@class='patFuncTitle']", document).snapshotItem(0);
      firstRow.parentNode.removeChild(firstRow);
   
      if ( location.href.match(/holds/) )
      {
        fixupTableDates(infoTable, 4);
         ts_resortTable(infoTable, 2, sortHoldStatus);
   
         // remove the Cancel All button - what a stupid button
         var allForms;
         allForms = document.evaluate(
            "//form[@name='cancel_form_1']",
            document,
            null,
            XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
            null);
         var thisForm;
         for (var i = 0; i < allForms.snapshotLength; i++)
         {
            thisForm = allForms.snapshotItem(i);
            thisForm.parentNode.removeChild(thisForm);
            // do something with thisForm
         }
      }
      else if ( location.href.match(/items/) )
      {
         fixupTableDates(infoTable, 3);
         ts_resortTable(infoTable, 3, sortDue);
      }
   }

   function autoSubmit()
   {
      var toSubmit = true;
      var submit;
      var f = document.forms[0];
      if ( f )
      {
         for ( var i = 0; i < f.elements.length; i++ )
         {
            var elem = f.elements[i];
            var name = elem.name;
            if ( name == 'loc' || name == 'locx00' )
            {
               elem.value = myFavouriteLocation;
            }
            else if ( name == 'name' )
            {
               if ( ! elem.value || elem.value == '' )
               {
                  GM_log('no name - auto filling');
                  elem.value = myName;
               }
            }
            else if ( name == 'code' )
            {
               if ( ! elem.value || elem.value == '' )
               {
                  GM_log('no card number, so not submitting!');
                  toSubmit = false;
               }
            }
            else if ( name == 'submit' )
            {
               // save submit for later - we don't want to submit before filling out the fields
               submit = elem;
            }
         }
         if ( submit && toSubmit )
         {
            submit.click();
         }
      }
   }

   function consumptifyIsbn()
   {
      var isbnREdelimited = /[^\d](\d{9,12}[\dXx])([^\dXx]|$)/;   

      var allLinks, thisLink;
      allBibInfo = document.evaluate(
         '//td[@class="bibInfoData"]',
         document,
         null,
         XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
         null);
      for (var i = 0; i < allBibInfo.snapshotLength; i++) {
         thisInfo = allBibInfo.snapshotItem(i);
         // do something with thisInfo

         
         if ( thisInfo.firstChild.nodeValue && thisInfo.firstChild.nodeValue.match(isbnREdelimited) )
         {
            var span = document.createElement('span');
            span.innerHTML = thisInfo.firstChild.nodeValue.replace(isbnREdelimited, function(str, isbn, offset, s) {
                                                       return isbn.link('http://www.allconsuming.net/search/query?q=' + isbn + '&product=book&x=0&y=0');});
            thisInfo.replaceChild(span, thisInfo.firstChild);
         }
      }
   }      
      
   // ========================================================================

   autoSubmit();
   fixupTable();
   consumptifyIsbn();
})();
