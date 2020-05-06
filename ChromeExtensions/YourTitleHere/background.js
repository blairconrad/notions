chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.command == "update_title") {
        chrome.tabs.get(sender.tab.id, function (tab) {
            var url = tab.url;
            chrome.bookmarks.search(url, function (results) {
                for (var index in results) {
                    if (url == results[index].url) {
                        sendResponse({ "title": results[index].title });
                        break;
                    }
                }
            }
            );
        });

        // Indicates an aysnchronous response, since chrome.bookmarks.* are asynchronous functions.
        // Without this, the message channel will be closed before the response is read.
        return true;
    }
});
