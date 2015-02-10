function isAlreadyLinked(node)
{
    while ( node.parentNode )
    {
        node = node.parentNode;
        if ( node.nodeName.toUpperCase() == 'A' )
        {
            return true;
        }
    }
    return false;
}

function getTextNodeIterator()
{
    return document.createNodeIterator(
        document.body,
        NodeFilter.SHOW_TEXT,
        { acceptNode : function (node) {return NodeFilter.FILTER_ACCEPT;} },
        false
    );

    
}

function addSvnLinks()
{
    var revisionRE = /\b(?:r|(?:[Rr]evisions?[,:]? ))([0-9]{5,})/g;

    var iterator = getTextNodeIterator();
    var textNode;
    while ((textNode = iterator.nextNode()) != null) 
    {
        try
        {
            if ( textNode.nodeValue && textNode.nodeValue.match(revisionRE))	    
            {
                if ( ! isAlreadyLinked(textNode) )
	        {
	            var $span = $('<span></span>');
                    $span.html(textNode.nodeValue.replace(revisionRE,
                                                          '<a href="http://wtlslsven01.mitra.com:8080/svn/repos/impax-mvf/info?revision=$1">$&</a>'));
                    $(textNode).replaceWith($span);
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

    var iterator = getTextNodeIterator();
    var textNode;
    while ((textNode = iterator.nextNode()) != null) 
    {
        try
        {
            if ( textNode.nodeValue && textNode.nodeValue.match(misRE))	    
            {
                if ( ! isAlreadyLinked(textNode) )
                {
	            var $span = $('<span></span>');
                    $span.html(textNode.nodeValue.replace(misRE, function (str, issueNumber, offset, s) {
                        return '<a href="/MISCore/importsissue/Issue.asp?Ref=' +issueNumber+'">' +issueNumber+'</a>';}));
                    $(textNode).replaceWith($span);
                }
            }
        }
        catch(err)
        {}
    }
}

function addCaseLinks()
{
    var misRE = /(case(:|(\(s\)))?)\s*([0-9]{5,6})/ig;

    var iterator = getTextNodeIterator();
    var textNode;
    while ((textNode = iterator.nextNode()) != null) 
    {
        try
        {
            if ( textNode.nodeValue && textNode.nodeValue.match(misRE))	    
            {
                if ( ! isAlreadyLinked(textNode) )
                {
	            var $span = $('<span></span>');
                    $span.html(textNode.nodeValue.replace(misRE, function(str, caseWord, caseSuffix, optionalS, caseNumber, offset, s) {
                        return '<a href="/MISCore/importscase/Case.asp?Ref=' +caseNumber+'">' +caseWord + ' ' + caseNumber+'</a>';}));
                    $(textNode).replaceWith($span);
                }
            }
        }
        catch(err)
        {}
    }
}


chrome.extension.sendRequest(request={msg: 'show'});
// tryNodeIterator();
addSvnLinks();
addCaseLinks();
addIssueLinks();
// addReviewLinks();
// addNodeLinks();

