document.addEventListener('DOMContentLoaded', function() {

  function fetchMarkdown(url, textContent) {
    return fetch(url)
        .then(response => response.text())
        .then(markdown => convertMarkdownToHtml(markdown, textContent))
        .catch(error => console.error('Error fetching Markdown:', error));
  }

  function convertMarkdownToHtml(markdownText, textContent) {
      var converter = new showdown.Converter();
      var html = converter.makeHtml(markdownText);
      document.getElementById('textarea').innerHTML = html;
      document.getElementById('title').innerHTML = textContent;
  }

  document.querySelectorAll('#links-container .dropdown-item').forEach(link => {
      link.addEventListener('click', function(event) {
          event.preventDefault(); 
          const fileUrl = this.getAttribute('data-url');
          const textContent = this.textContent.trim(); 

          fetchMarkdown(fileUrl, textContent);
      });
  });

});
