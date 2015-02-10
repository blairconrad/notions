// ==UserScript==
// @name           CruiseControl Build Results
// @namespace      http://www.agfa.com
// @description    Make the build results pages more usable
// @include        */buildresults/*
// ==/UserScript==

var versionString = "2009.06.24";
var latestChange = "put change type and path next to each other";
var scriptURL = 'http://blairconrad.googlecode.com/svn/trunk/greasemonkey/cruisecontrolbuildresult.user.js'

// Settings ------------------------------------------------------------------

function Settingsobject(namespace)
{
    this.prefix = namespace ? namespace + '.'  : "";
    this.default={};
}

Settingsobject.prototype.set=function(name, value)
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
}

Settingsobject.prototype.get = function(name)
{
    var value=GM_getValue(this.prefix+""+name, this.default[name] || "{b}0")
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
}

Settingsobject.prototype.register = function(name, defaultvalue)
{
    this.default[name]=defaultvalue;
    return true;
}

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
                // GM_log('status: ' + response.status + 
                //        '\r\nheaders:\r\n' + response.responseHeaders);
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

                globalSettings.set('script-last-modified', serverLastModified)

                if ( ! forceVersionCheck && localLastModified == serverLastModified )
                {
                    GM_log('last modified is same!');
                    return;
                }

	        responseArray = response.responseText.split('\r\n')
	        for ( line in responseArray ) 
                {
                    
	            if ( responseArray[line].match('var versionString = ') ) 
	            {
                        var serverVersion = responseArray[line].split('"')[1];
                        GM_log('server version: ' + serverVersion + 
                               ', local version = ' + versionString);
                        
                        line = parseInt(line) + 1;
                        latestChange = responseArray[line].split('"')[1];
                        if ( serverVersion == versionString )
                        {
                            GM_log('no need to update');
                        }
                        else
                        {
                            GM_log('latest change = ' + latestChange);
                            notifyOfNewVersion(latestChange);
                        }
		        break;
	            }
	        }
            }
        }
    );
}

function notifyOfNewVersion(latestChange)
{
    var newRow = document.createElement('tr');
    newRow.innerHTML=('<tr><td><blink><a class="link" href="' + scriptURL + '" title="' + latestChange + '">new user script available</a></blink></td></tr>');
    
    var tbody = $x('//table//table/tbody')[0];
    tbody.insertBefore(newRow, null);
}                       

function makeMenuToggle(key, defaultValue, toggleOn, toggleOff, prefix)
{
    // Load current value into variable
    window[key] = GM_getValue(key, defaultValue);
    // Add menu toggle
    GM_registerMenuCommand((prefix ? prefix+": " : "") + (window[key] ? toggleOff : toggleOn), function() {
        GM_setValue(key, !window[key]);
        location.reload();
    });
}

function addMenuCommands()
{
    makeMenuToggle("hideByDefault", true, "Collapse errors and warnings", "Show errors and warnings", "CC");
    makeMenuToggle("forceVersionCheck", false, "Always do full check for newer script", "Cache script to avoid pounding server", "CC");
}

//Run a particular XPath expression p against the context node context (or the
//document, if not provided). Returns the results as an array.
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
}

function toggleDisplay(node)
{
    if ( node != null )
    {
        ( node.style.display == '' ) ? node.style.display = 'none' : node.style.display = '';
    }
}

function showHideContents(event){

    if ( event.currentTarget.innerHTML.indexOf('Errors/Warnings') >= 0 )
    {
        var errorsAndWarnings = grabErrorsWarningsTable();
        if (errorsAndWarnings != null)
        {
            var rows = errorsAndWarnings.getElementsByTagName('tr');
            for ( var i = 1; i < rows.length; i++ )
            {
                toggleDisplay(rows[i]);
            }
        }
    }
    else if (event.currentTarget.innerHTML.indexOf('Error') >= 0)
    {
        toggleDisplay(document.getElementById('bottomTable'));
    }
    else
    {
        toggleDisplay(grabTopTable());
    }
}

function grandparent(node) {
    if ( node != null && node.parentNode != null )
    {
        return node.parentNode.parentNode;
    }
    return null;
}

function grabErrorsWarningsTable() {
    var mainTableInfo = $x("//table/tbody/tr/td[@class='compile-sectionheader']")[0];
    return grandparent(mainTableInfo);
}

function grabTopTable(){

    var mainTableInfo = $x("//table/tbody/tr/td[@class='unittests-data']")[0];
    if ( mainTableInfo.innerHTML.indexOf('All Tests Passed') >= 0 ) return null;

    return grandparent(mainTableInfo);
}

function prepareLowerTable(){
    
    var firstRowFound = false;
    var x = 0;
    var tempArray;
    var groupTable = document.createElement('table');
    groupTable.setAttribute('width', '98%');
    groupTable.setAttribute('border', '0');
    groupTable.setAttribute('cellspacing', '0');
    groupTable.setAttribute('cellpadding', '2');
    groupTable.setAttribute('align', 'center');
    groupTable.setAttribute('id', 'bottomTable');
    var tBody = document.createElement('tbody');
    groupTable.appendChild(tBody);

    var tableInfo = $x("//table/tbody/tr/td[@class='unittests-sectionheader']")[0];
    var mainTable = grandparent(tableInfo);
    for(var i = 0; i < mainTable.childNodes.length; i++)
    {
        var currentRow = mainTable.childNodes[i];
    	
        if (firstRowFound)
        {
            tempArray[x] = currentRow;
            x++;
        }    	
        else if (currentRow.innerHTML != null && currentRow.innerHTML.indexOf('Unit Test Error Details') >= 0)
        {
            firstRowFound = true;
            tempArray = new Array(mainTable.childNodes.length - i - 1);
        }
    }

    if (tempArray != null)
    {
        for( var j = 0; j < tempArray.length; j++ )
        {
            tBody.appendChild(tempArray[j]);
        }
    }

    var newCell = document.createElement('td');
    newCell.appendChild(groupTable);
    var newRow = document.createElement('tr');
    newRow.appendChild(newCell);
    
    mainTable.appendChild(newRow);
}

function addEventHandlers(){

    var tds = document.getElementsByTagName( 'TD' );
    for( var j = 0; j < tds.length; j++ )
    {
        if (tds[j].className == 'unittests-sectionheader')
        {
            var tr = tds[j].parentNode;
            tr.className = 'unitTestSection' + j;

            var testDetails = grabTopTable();
            if (testDetails != null)
            {
                tr.style.cursor = 'pointer';
                tr.addEventListener('click', showHideContents, true);
            }

        }
    }

    var errorsAndWarnings = grabErrorsWarningsTable();
    if (errorsAndWarnings != null)
    {
        var rows = errorsAndWarnings.getElementsByTagName('tr');
        rows[0].style.cursor = 'pointer';
        rows[0].addEventListener('click', showHideContents, true);
    }
}

function showHideTables(){

    var topTable = grabTopTable();
    var bottomTable = document.getElementById('bottomTable');

    var display = '';
    if ( hideByDefault )
    {
        display = 'none';
    }

    
    if (topTable != null) 
    {
        topTable.style.display = display;
    }

    if (bottomTable != null) 
    {
        bottomTable.style.display = display;
    }

    var errorsAndWarnings = grabErrorsWarningsTable();
    if (errorsAndWarnings != null)
    {
        var rows = errorsAndWarnings.getElementsByTagName('tr');
        for ( var i = 1; i < rows.length; i++ )
        {
            rows[i].style.display = display;
        }
    }

}


function linkIssuesInCell(cell)
{
    var misRE = /(^|[^0-9])([0-9]{5,6})([^0-9]|$)/ig;
    var issueLinkPrefix = 'https://mist.agfa.net/MISCore/importsissue/Issue.asp?Ref=';
    var matches = cell.innerHTML.match(misRE);
    if( matches != null )
    {
        cell.innerHTML = cell.innerHTML.replace(misRE, 
                                                function (str, p1, p2, p3, offset, s) 
                                                {
                                                    return p1 + p2.link(issueLinkPrefix + p2) + p3; 
                                                });
    }
}

function linkRevisionInCell(cell)
{
    var oldRevision = cell.innerHTML.replace(/^\s*(.*?)\s*$/, "$1");
    cell.innerHTML = '<a href="http://wtlslsven01:8080/svn/repos/impax-mvf/info?revision='  + oldRevision + '">' 
        + oldRevision 
        + '</a>'
}

function issueLinking(){
    
    var modificationRows = $x("//tr[@class='modifications-evenrow']").concat($x("//tr[@class='modifications-oddrow']"));

    for ( var rowNum = 0; rowNum < modificationRows.length; rowNum++ )
    {
        var row = modificationRows[rowNum];

        linkIssuesInCell(row.cells[row.cells.length-1]);
    }
    
    // This section is to highlight the MIS Issue # for the Last Log Entry in the header information
    var headerRows = $x("//table[@class='header']/tbody/tr/th");
    for ( var k = 0; k < headerRows.length; k++ )
    {
        var header = headerRows[k];
        if ( header.innerHTML.indexOf('Last log entry:') >= 0 )
        {
            linkIssuesInCell(header.parentNode.getElementsByTagName('td')[0]);
            break;
        }
    }
}

function linkToSvn()
{
    var tds =$x("//td[@class='modifications-data']");
    for ( var i = 0; i < tds.length-1; i++ )
    {
        var td = tds[i];
        var oldHtml = td.innerHTML;
        if ( oldHtml.indexOf('/') == 0 )
        {
            var newRevision = tds[i+1].innerHTML;

            td.innerHTML = '<a href="http://wtlslsven01:8080/svn/repos/impax-mvf/diff' + oldHtml + '?revision=' + newRevision + '">' 
                + oldHtml 
                + '</a>';

            linkRevisionInCell(tds[i+1]);
        }
    }

    // This section is to link the latest SVN revision in the header information
    var headerRows = $x("//table[@class='header']/tbody/tr/th");
    for ( var k = 0; k < headerRows.length; k++ )
    {
        var header = headerRows[k];
        if ( header.innerHTML.indexOf('SVN Revision:') >= 0 )
        {
            linkRevisionInCell(header.parentNode.getElementsByTagName('td')[0]);
            break;
        }
    }
}

function collapseCommits()
{
    var modificationRows = $x("//tr[@class='modifications-evenrow']|//tr[@class='modifications-oddrow']");

    // swap path and user to get change type and path together
    for ( i = 0; i < modificationRows.length; i++ )
    {
        oldCell = modificationRows[i].cells[2];
        modificationRows[i].removeChild(oldCell);
        modificationRows[i].insertBefore(oldCell, modificationRows[i].cells[1]);
    }

    lastIndex = 0;
    while ( lastIndex < modificationRows.length )
    {
        lastCommit = modificationRows[lastIndex].cells[3].innerHTML;
        
        i = lastIndex;
        while ( i < modificationRows.length )
        {
            if ( lastCommit != modificationRows[i].cells[3].innerHTML )
            {
                break;
            }
            i = i + 1;
        }
        
        for ( col = 5; col >= 2; col-- )
        {
            modificationRows[lastIndex].cells[col].setAttribute('rowspan', i - lastIndex);
        }

        lastIndex += 1;
        while ( lastIndex < i )
        {
            // alert('removing ' + lastIndex);
            for ( col = 5; col >= 2; col-- )
            {
                modificationRows[lastIndex].removeChild(modificationRows[lastIndex].cells[col]);
            }
            lastIndex += 1;
        }
    }
}

function addGlobalStyle(css) {
    var head, style;
    head = document.getElementsByTagName('head')[0];
    if (!head) { return; }
    style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = css;
    head.appendChild(style);
}

function getProjectName()
{
    try
    {
        return $x('//option[@selected="selected"]')[0].innerHTML;
    }
    catch ( e )
    {
        return 'unknown CC project';
    }
}

function setTitle(){
    var titleTextSnapshot = $x("//th[@class='big']");

    if ( titleTextSnapshot.length == 0 )
    {
        titleTextSnapshot = $x("//td[@class='header-title']");
    }

    if ( titleTextSnapshot.length > 0 )
    {
        var titleText = titleTextSnapshot[0].innerHTML;
        if ( titleText  == 'BUILD FAILED' )
        {
            titleText = 'FAIL ' + getProjectName() ;
        }

        titleText = titleText.replace(/\s+|&nbsp;/g, ' ');
        titleText = titleText.replace(/BUILD COMPLETE -/, 'CC');
        document.title = titleText;
    }
}

function runScriptMain(){
    addMenuCommands();
    checkForNewerScript();
    addGlobalStyle(
        '.modifications-oddrow { background-color:#FFFFFF ! important; } ' +
            '.modifications-evenrow { background-color:#E8E8FF ! important; } ' +
            '.failures-oddrow { background-color:#FFFFFF ! important; } ' +
            '.failures-evenrow { background-color:#E8E8FF ! important; } ' +
            '.unittests-oddrow { background-color:#E8E8FF ! important; } ' +
            '.unittests-failure { color:#000000 ! important; } ' 
    );

    setTitle();
    addEventHandlers();
    prepareLowerTable();	
    showHideTables();
    issueLinking();
    linkToSvn();
    collapseCommits();
}

runScriptMain();
