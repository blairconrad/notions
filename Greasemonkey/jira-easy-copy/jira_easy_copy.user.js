// ==UserScript==
// @name           JIRA Easy Copy
// @namespace      jira_easy_copy
// @description    Add buttons to copy JIRA issue title or link
// @include        http://jiraprod.agfahealthcare.com/browse/IEI*
// ==/UserScript==

(function()
 {
   if ( window.location.href.indexOf('jiraprod.agfahealthcare.com') < 0 ||
        window.location.href.indexOf('IEI') < 0 )
   {
     return;
   }

   function createCopyButton(title, valueToCopy)
   {
     var copyButtonAnchor = document.createElement('a');
     copyButtonAnchor.setAttribute('class', 'toolbar-trigger viewissue-share');
     copyButtonAnchor.setAttribute('href', '#');

     var copyButtonSpan = document.createElement('span');
     copyButtonSpan.setAttribute('class', 'icon aui-icon aui-icon-small aui-iconfont-share');
     copyButtonSpan.setAttribute('title', title);
     copyButtonSpan.onclick = function(event) {
       window.prompt("Copy to clipboard: Ctrl+C, Enter", valueToCopy);
     };

     return copyButtonAnchor
       .appendChild(copyButtonSpan);
   }

   function addCopyLinkButton(issueAnchor, issueTitle)
   {
     var copyLinkSpacer = document.createTextNode(' ');
     var copyLinkButton = createCopyButton(
       'Copy a link to this issue, formatted in MarkDown (good for MatterMost)',
       '[' + issueAnchor.textContent + ' - ' + issueTitle.textContent + '](' + window.location.href + ')');

     var anchorParent = issueAnchor.parentNode;
     anchorParent.appendChild(copyLinkSpacer);
     anchorParent.appendChild(copyLinkButton);
   }

   function addCopyTitleButton(issueTitle)
   {
     var copyTitleButton = createCopyButton(
       'Copy the title of this issue (good for Code Collaborator)',
       issueAnchor.textContent + ' - ' + issueTitle.textContent);

     issueTitle.parentNode.appendChild(copyTitleButton);
   }

   var issueAnchor = document.getElementById('key-val');
   var issueTitle = document.getElementById("summary-val");

   addCopyLinkButton(issueAnchor, issueTitle);
   addCopyTitleButton(issueTitle);
 })();
