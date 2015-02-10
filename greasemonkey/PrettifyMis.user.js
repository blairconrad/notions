// ==UserScript==
// @name          PrettifyMis
// @namespace     http://agfa.com/blair.conrad
// @description   Pretty up the MIS
// @include       https://mist.agfa.net/*
// @exclude       https://mist.agfa.net/MISCore/importsproduct/cvsmanager.asp?FormNm=NewIssue*
// @exclude       https://mist.agfa.net/MISCore/importsframework/findgeneral.asp*
// @exclude       https://mist.agfa.net/MISCore/importsworklist/WorklistSelect.asp*
// ==/UserScript==

(
    function()
    {
        function removeNode(node)
        {
            node.parentNode.removeChild(node);
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

        function xpath(query, node) 
        {
            return document.evaluate(query, node, null,
                                     XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
        }

        function makeMenuToggle(key, defaultValue, toggleOn, toggleOff, prefix) {
            // Load current value into variable
            window[key] = GM_getValue(key, defaultValue);
            // Add menu toggle
            GM_registerMenuCommand((prefix ? prefix+": " : "") + (window[key] ? toggleOff : toggleOn), function() {
                GM_setValue(key, !window[key]);
                location.reload();
            });
        }

        function addGlobalStyle(css)
        {
            var head, style;
            head = document.getElementsByTagName('head')[0];
            if (!head) { return; }
            style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = css;
            head.appendChild(style);
        }

        function getPreviousNode(node, name)
        {
            var uName = name.toUpperCase();
            var prev;
            prev = node.previousSibling;
            while ( prev.nodeName.toUpperCase() != uName )
            {
                prev = prev.previousSibling;
            }
            return prev;
        }

        function squashHeader()
        {
            var headerRows = xpath("//tr[th]", document);
            if ( headerRows && headerRows.snapshotLength > 0 )
            {
                var headerRow = headerRows.snapshotItem(0);

                var child = xpath("td[1]", headerRow).snapshotItem(0);
                headerRow.removeChild(child);
                
                var child = xpath("th[9]", headerRow).snapshotItem(0);
                headerRow.removeChild(child);
                
                var child = xpath("th[8]", headerRow).snapshotItem(0);
                headerRow.removeChild(child);

                for ( var j = 0; j < 4; j++ )
                {
                    var child = xpath("th[2]", headerRow).snapshotItem(0);
                    headerRow.removeChild(child);
                }
                
                headerCell = document.createElement('th');
                headerCell.innerHTML = 'Description';
                headerRow.appendChild(headerCell);
            }
        }

        function whitenUpFrozens(table)
        {
            allFrozens = xpath(".//td[@BGCOLOR='#669966']", table)
            for ( var i = 0; i < allFrozens.snapshotLength; ++i )
            {
                var frozen = allFrozens.snapshotItem(i);
                var attr = document.createAttribute('style');
                attr.value = 'color: white; font-weight: bold;';
                frozen.setAttributeNode(attr);
            }
        }

        function squashRows(table)
        {
            allDescriptions = xpath(".//td[@colspan=13]", table);

            for ( var i = 0; i < allDescriptions.snapshotLength; ++i )
            {
                var desc = allDescriptions.snapshotItem(i);

                var sib;
                if ( desc.parentNode )
                {
                    sib = getPreviousNode( desc.parentNode, 'TR' );
                }

                if ( desc.firstChild.firstChild.nodeValue.match('^Resolution:') )
                {
                    // sib = getPreviousNode(sib, 'TR');
                }
                else
                {
                    if ( sib )
                    {
                        var child = xpath("td[12]", sib).snapshotItem(0);
                        sib.removeChild(child);
                        
                        var child = xpath("td[9]", sib).snapshotItem(0);
                        sib.removeChild(child);
                        
                        var child = xpath("td[8]", sib).snapshotItem(0);
                        sib.removeChild(child);
                        
                        for ( var j = 0; j < 4; ++j )
                        {
                            var child = xpath("td[2]", sib).snapshotItem(0);
                            sib.removeChild(child);
                        }
                    }
                }

                if ( sib )
                {
                    var p = desc.parentNode;
                    sib.appendChild(desc);
                }
            }
        }

        function workOnTable(thisTable)
        {
            var attr = document.createAttribute('class');
            attr.value = 'flat';
            
            thisTable.setAttributeNode(attr);
            
            thisTable.removeAttribute('border');

            var subTables;
            
            subTables = xpath('.//table', thisTable);
            for (var i = 0; i <  subTables.snapshotLength; i++)
            {
                subTables.snapshotItem(i).removeAttribute('border');
            }
        }

        function getTables()
        {

            // possibly bail
            titles = xpath("//h2", document);
            for ( var i = 0; i < titles.snapshotLength; i++ )
            {
                var title = titles.snapshotItem(i).firstChild.nodeValue;
                if ( /Send Email/.test(title) ||
                     /Transfer Ownership/.test(title) )
                {
                    return;
                }
            }


            //return xpath("/html/body/center/form/table", document);
            var someTables = $x("/html/body/center/form/table");

            var tables = [];
            var i;

            for ( i = 0; i < someTables.length; ++i )
            {
                tables.push(someTables[i]);
            }

            //       someTables = $x("/html/body/form/center/table");

            //       for ( i = 0; i < someTables.length; ++i )
            //       {
            //          tables.push(someTables[i]);
            //       }

            if ( tables.length == 0 )
            {
                tables = $x("/html/body/form/table");
                // center them up
                for ( i = 0; i <  tables.length; i++)
                {
                    alert($i);
                    var table = tables[i];
                    var tableParent = table.parentNode;
                    newElement = document.createElement('center');
                    tableParent.insertBefore(newElement, table);         
                    tableParent.removeChild(table);
                    newElement.appendChild(table);
                }
                
            }
            return tables;
        }


        function containingLinkNode(node)
        {
            while ( node.parentNode )
            {
                node = node.parentNode;
                if ( node.nodeName.toUpperCase() == 'A' )
                {
                    return node;
                }
            }
            return null;
        }

        function addCaseLinks()
        {

            var misRE = /(case(:|\(s\))?\s*([0-9]{5,6})/ig;
            var candidates = $x('//text()');
            for (var node = null, i = 0; node = candidates[i];  i++ )
            {
                try
                {
                    if ( node.nodeValue && node.nodeValue.match(misRE))	    
                    {

	                linkNode = containingLinkNode(node);
	                if ( linkNode == null )
	                {
		            var span = document.createElement('span');
                            span.innerHTML = node.nodeValue.replace(misRE, function (str, caseWord, caseNumber, offset, s) {
                                return '<a href="https://mist.agfa.net/MISCore/importscase/Case.asp?Ref=' +caseNumber+'" target='+linkOpenTarget()+'>' + caseWord + ' ' + caseNumber+'</a>';});
                            node.parentNode.replaceChild(span, node);
	                }
	                else
	                {
	                    linkNode.target = linkOpenTarget();
	                }
                    }
                }
                catch(err)
                {
                }
            }
        }

        function addIssueLinks()
        {
            var misRE = /\b([0-9]{5,6})\b/g;
            var candidates = $x('//text()');
            for (var node = null, i = 0; node = candidates[i];  i++ )
            {
                try
                {
                    if ( node.nodeValue && node.nodeValue.match(misRE))	    
                    {
	                linkNode = containingLinkNode(node);
	                if ( linkNode == null )
	                {
		            var span = document.createElement('span');
                            span.innerHTML = node.nodeValue.replace(misRE, function (str, issueNumber, offset, s) {
                                return '<a href="https://mist.agfa.net/MISCore/importsissue/Issue.asp?Ref=' +issueNumber+'" target='+linkOpenTarget()+'>' +issueNumber+'</a>';});
                            node.parentNode.replaceChild(span, node);
	                }
	                else
	                {
	                    linkNode.target = linkOpenTarget();
	                }
                    }
                }
                catch(err)
                {
                }
            }
        }

        function addReviewLinks()
        {
            var reviewRE = /(review:?\s+)\b([0-9]+)\b/ig;
            var candidates = $x('//text()');
            for (var node = null, i = 0; node = candidates[i];  i++ )
            {
                try
                {
                    if ( node.nodeValue && node.nodeValue.match(reviewRE))	    
                    {
	                linkNode = containingLinkNode(node);
	                if ( linkNode == null )
	                {
		            var span = document.createElement('span');
                            span.innerHTML = node.nodeValue.replace(reviewRE, function (str, reviewWord, reviewNumber, offset, s) {
                                return '<a href="http://wtlswcoderev01:8080/index.jsp?page=ReviewDisplay&reviewid=' +reviewNumber+'" target='+linkOpenTarget()+'>' +reviewWord + reviewNumber+'</a>';});
                            node.parentNode.replaceChild(span, node);
	                }
	                else
	                {
	                    linkNode.target = linkOpenTarget();
	                }
                    }
                }
                catch(err)
                {
                }
            }
        }

        function addSvnLinks()
        {
            var revisionRE = /\b(?:r|(?:[Rr]evisions?:? ))([0-9]{5,})/g;
            var candidates = $x('//text()');
            for (var node = null, i = 0; node = candidates[i];  i++ )
            {
                try
                {
                    if ( node.nodeValue && node.nodeValue.match(revisionRE))	    
                    {
	                linkNode = containingLinkNode(node);
	                if ( linkNode == null )
	                {
		            var span = document.createElement('span');
                            span.innerHTML = node.nodeValue.replace(revisionRE,
                                                                    '<a href="http://svn.mitra.com:8080/svn/revinfo.svn?revision=$1&name=repo" target='+linkOpenTarget()+'>$&</a>');
                            node.parentNode.replaceChild(span, node);
	                }
	                else
	                {
	                    linkNode.target = linkOpenTarget();
	                }
                    }
                }
                catch(err)
                {
                }
            }
        }

        function linkOpenTarget()
        {
            return openLinksInNewWindow ? "_blank" : "_self";
        }
        
        function addNodeLinks()
        {
            var nodeRE = /\b([0-9]{8})\b/g;
            var imageUrn = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzf/wAARCAAIAAcDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAgEAABBAICAwEAAAAAAAAAAAACAQMEBQASEyEGBxEU/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/ALWDVeSWHsJ2/KZKg0cd8o4Vzz7ifqEWzAnuPZRROTXXpNhTb4i9mxjA/9k=';
            var candidates = $x('//text()');
            for (var node = null, i = 0; node = candidates[i];  i++ )
            {
                try
                {
                    if ( node.nodeValue && node.nodeValue.match(nodeRE))
                    {
	                linkNode = containingLinkNode(node);
	                if ( linkNode == null )
	                {
                            var span = document.createElement('span');
                            span.innerHTML = node.nodeValue.replace(nodeRE, function (str, nodeNumber, offset, s) {
                                return '<a href="https://livelink.agfa.net/Livelink/livelink.exe/overview/' + nodeNumber+'" target='+linkOpenTarget()+'>' + nodeNumber + '<img src="' + imageUrn + '"></a>';});
                            node.parentNode.replaceChild(span, node);
                        }
       	                else
	                {
	                    linkNode.target = linkOpenTarget();
	                }
                    }
                }
                catch(err)
                {
                }
            }
        }

        function fixupTitle()
        {
            var candidates = document.evaluate('//H2[@align="center"]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
            for (var node = null, i = 0; (node = candidates.snapshotItem(i));  i++ )
            {
                GM_log(node.textContent);
                document.title = node.textContent;
            }
        }

        function addMenuCommands()
        {
            makeMenuToggle("openLinksInNewWindow", false, "Open Links in New Window", "Open Links in Same Window", "MIS");
        }

        function isModuleManager()
        {
            return location.href.indexOf('https://mist.agfa.net/MISCore/importsproduct/cvsmanager.asp') == 0;
        }

        function updateModuleManager()
        {
            
            $x('//input[@OnChange]').forEach(function (element, index, array)
                                   {
//                                       alert(element);
                                       alert(element.onchange);
                                       element.removeEventListener(
                                           'onchange',
                                           'PopulateModule(form.CVS_KEYWORDS,form.MODULE_REF,form.MODULE_VERSION_REF);',
//                                           PopulateModule,
                                           false);
//                                       removeNode(element);
                                   }
                                  );

//             $x('//input/@OnChange').forEach(function (element, index, array)
//                                             {
//                                                 alert(element);
//                                             }
//                                            );
        }

        // ========================================================================
//       if ( isModuleManager() ) 
//       {
//           updateModuleManager();
//       }
//        else
        {
            addGlobalStyle('table.flat { margin:0 0 0 0; border:1px solid black; padding: 0px 0px 0px 0px; border-collapse:collapse; } table.flat td { border:1px solid black; padding: 2px 2px 2px 2px; } a { text-decoration: none; color: #4400FF; }');


            var squash = false;
            if ( location.href.match(/MyWorklist.asp[?]ORDER=(STATUS|PRIORITY|SEVERITY)/) 
                 //        || location.href.match(/importsworklist\Linklist/)
               )
            {
                squash = true;
            }

            var allTables = getTables();
            if ( allTables )
            {
                if ( 0 < allTables.length ) 
                {
                    for (var i = 0; i <  allTables.length; i++)
                    {
                        var table = allTables[i];
                        workOnTable(table);
                        if ( squash )
                        {
                            squashRows(table);
                        }
                        whitenUpFrozens(table);
                    }

                    if ( squash )
                    {
                        squashHeader();
                    }
                }
            }

            fixupTitle();
            addMenuCommands();
            addSvnLinks();
            addCaseLinks();
            addIssueLinks();
            addReviewLinks();
            addNodeLinks();
        }
    }
)(); 
