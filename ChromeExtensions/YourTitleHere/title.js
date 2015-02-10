chrome.extension.sendRequest(request={msg: 'update_title'}, callback=function (response)
                             {
                                 document.title = response.title;
                             }
);