function linkIssuesInCell(cell)
{
    var misRE = /(^|\D)(\d{5,6})(\D|$)/g;
    var issueLinkPrefix = 'https://mist.agfa.net/MISCore/importsissue/Issue.asp?Ref=';
    var matches = cell.innerHTML.match(misRE);
    if( matches != null )
    {
        cell.innerHTML = cell.innerHTML.replace(misRE, 
                                                function (str, before, issueNumber, after, offset, s) 
                                                {
                                                    return before + issueNumber.link(issueLinkPrefix + issueNumber) + after;
                                                });
    }
}

function addIssueLinks()
{
    var $modificationRows = $("tr.modifications-evenrow, tr.modifications-oddrow");

    for ( var rowNum = 0; rowNum < $modificationRows.length; rowNum++ )
    {

        var row = $modificationRows[rowNum];

        linkIssuesInCell(row.cells[row.cells.length-1]);
    }
    
    //     // This section is to highlight the MIS Issue # for the Last Log Entry in the header information
    //     var $headerRows = $("//table.header tbody tr th");
    //     for ( var k = 0; k < $headerRows.length; k++ )
    //     {
    //         var header = $headerRows[k];
    //         alert(header.innerHTML);
    //         if ( header.innerHTML.indexOf('Last log entry:') >= 0 )
    //         {
    //             linkIssuesInCell(header.parentNode.getElementsByTagName('td')[0]);
    //             break;
    //         }
    //     }
}

function linkIssuesInCell(cell)
{
    var misRE = /(^|\s|MIS)(\d{5,6})(\D|$)/ig;
    var issueLinkPrefix = 'https://mist.agfa.net/MISCore/importsissue/Issue.asp?Ref=';
    var matches = cell.innerHTML.match(misRE);
    if( matches != null )
    {
        cell.innerHTML = cell.innerHTML.replace(misRE, 
                                                function (str, before, issueNumber, after, offset, s) 
                                                {
                                                    return before + issueNumber.link(issueLinkPrefix + issueNumber) + after;
                                                });
    }
}

function linkSvnInCell(cell)
{
    var revisionRE = /(\d+)/;
    var revisionLinkPrefix = 'http://wtlslsven01.mitra.com:8080/svn/repos/impax-mvf/info?revision='
    var matches = cell.innerHTML.match(revisionRE);
    if( matches != null )
    {
        cell.innerHTML = cell.innerHTML.replace(revisionRE, 
                                                function (str, revisionNumber, offset, s) 
                                                {
                                                    return revisionNumber.link(revisionLinkPrefix + revisionNumber);
                                                });
    }
}

function addSvnLinks()
{
    var $modificationRows = $("tr.modifications-evenrow, tr.modifications-oddrow");

    for ( var rowNum = 0; rowNum < $modificationRows.length; rowNum++ )
    {

        var row = $modificationRows[rowNum];
        

        linkSvnInCell(row.cells[row.cells.length-3]);
    }    
}


function reorderModificationsColumns()
{
    var $modificationRows = $("tr.modifications-evenrow, tr.modifications-oddrow");
    $modificationRows.each(function(index) {
        var $children = $(this).children();
        $firstCell = $($children[0]);
        $pathCell = $($children[2]);
        $pathCell.insertAfter($firstCell);
    });    
}

function collapseCommits()
{
    var $modificationRows = $("tr.modifications-evenrow, tr.modifications-oddrow");

    var evenRow = "true";
    var lastIndex = 0;
    while ( lastIndex < $modificationRows.length )
    {
        var lastCommit = $modificationRows[lastIndex].cells[3].innerHTML;
        
        var i = lastIndex;
        while ( i < $modificationRows.length )
        {
            $modificationRows[i].setAttribute("class", evenRow ? "modifications-evenrow" : "modifications-oddrow");
            if ( lastCommit != $modificationRows[i].cells[3].innerHTML )
            {
                // found a new commit
                break;
            }
            i = i + 1;
        }
        
        for ( col = 5; col >= 2; col-- )
        {
            $modificationRows[lastIndex].cells[col].setAttribute('rowspan', i - lastIndex);
        }

        lastIndex += 1;
        while ( lastIndex < i )
        {
            // alert('removing ' + lastIndex);
            for ( col = 5; col >= 2; col-- )
            {
                $modificationRows[lastIndex].removeChild($modificationRows[lastIndex].cells[col]);
            }
            lastIndex += 1;
        }

        evenRow = ! evenRow;
    }
}

addSvnLinks();
addIssueLinks();
reorderModificationsColumns();
collapseCommits();