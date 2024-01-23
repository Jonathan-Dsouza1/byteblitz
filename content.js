chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (request.message === "analyze_page") {
        var url = window.location.href;
        fetch('http://127.0.0.1:5000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({ 'url': url }),
        })
        .then(response => response.json())
        .then(data => {
          chrome.runtime.sendMessage({ "message": "result", "result": data.result });
        })
        .catch(error => {
          console.error('Error:', error);
        });
      }
    }
  );
  