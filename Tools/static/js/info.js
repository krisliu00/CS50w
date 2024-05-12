document.addEventListener('DOMContentLoaded', function() {
  daily();

  function fetchMarkdown(url, textContent) {
    return fetch(url)
        .then(response => response.text())
        .then(markdown => convertMarkdownToHtml(markdown, textContent))
        .catch(error => console.error('Error fetching Markdown:', error));
  }

  function convertMarkdownToHtml(markdownText, textContent) {
      var html = marked.parse(markdownText);
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

  function daily(){
    const url = 'https://raw.githubusercontent.com/krisliu00/MyLearningStuff/main/Tools/md/Daily.md'
    const textContent = ' '
    fetchMarkdown(url, textContent)
  }
});
