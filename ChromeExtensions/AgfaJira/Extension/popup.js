document.addEventListener('DOMContentLoaded', function() {
  // We don't have direct access to write to the clipboard.
  // Hack around this by using the hidden textara control.
  // We need to make it temporarily visible for the copy to work.
  // In practice, this is too quick for users to notice.
  function copyToClipboard(text) {
    var ta = document.getElementById('ta');
    ta.style.display = 'block';
    ta.value = text;
    ta.select();
    document.execCommand('copy');
    ta.style.display = 'none';
  }

  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var tabId = tabs[0].id;
    chrome.tabs.sendMessage(tabId, {action: 'get page details'}, function(response) {
      var titleItem = document.getElementById('title_item');
      titleItem.onclick = function(event) {
        copyToClipboard(response.issueNumber + ' - ' + response.title);
        window.close();
      }

      var urlItem = document.getElementById('url_item');
      urlItem.onclick = function(event) {
        copyToClipboard('[' + response.issueNumber + ' - ' + response.title + '](http://jiraprod.agfahealthcare.com/browse/' + response.issueNumber + ')');
        window.close();
      }

      // We can't set window.location.href from within a popup's code,
      // so delegate to the code we've injected into the host page.
      var emailItem = document.getElementById('email_item');
      emailItem.onclick = function(event) {
        chrome.tabs.sendMessage(tabId, {action: 'send e-mail'});
        window.close();
      }
    });
  });
});
