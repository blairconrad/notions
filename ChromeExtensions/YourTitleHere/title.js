chrome.runtime.sendMessage({ command: "update_title" }, function (response) {
    document.title = response.title;
}
);