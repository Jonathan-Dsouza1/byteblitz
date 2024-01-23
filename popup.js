document.getElementById('analyzeButton').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var activeTab = tabs[0];
      chrome.tabs.sendMessage(activeTab.id, {"message": "analyze_page"});
    });
  });
  
  chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (request.message === "result") {
        document.getElementById('result').innerText = 'Result: ' + request.result;
      }
    }
  );
  