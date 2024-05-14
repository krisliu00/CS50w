document.addEventListener('DOMContentLoaded', function() {
    daily();
        
    const copyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/></svg>';
    const copiedIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16"><path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/></svg>';

    $(document).ready(function() {
    $('#calculator').click(function() {
        $("#calculatorarea, #displayarea").toggleClass("hidden");
        });
    });

      
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

      let blocks = document.querySelectorAll("#textarea pre");

      blocks.forEach((block) => {
          if (!navigator.clipboard) {
              return;
          }

          let button = document.createElement("button");
          button.className = "button-copy-code";
          button.innerHTML = copyIcon;
          block.appendChild(button);

          button.addEventListener("click", async () => {
              await copyCode(block);
          });
      });
  }

  document.querySelectorAll('#links-container .dropdown-item').forEach(link => {
        if (link.id !== 'calculator') {
            link.addEventListener('click', function(event) {
                event.preventDefault(); 
                const fileUrl = this.getAttribute('data-url');
                const textContent = this.textContent.trim(); 

                fetchMarkdown(fileUrl, textContent);
            });
        }
  });

  function daily(){
      const url = 'https://raw.githubusercontent.com/krisliu00/MyLearningStuff/main/Tools/md/Daily.md'
      const textContent = ' '
      fetchMarkdown(url, textContent)
  }

  async function copyCode(block) {
      let copiedCode = block.cloneNode(true);
      copiedCode.removeChild(copiedCode.querySelector("button.button-copy-code"));

      const html = copiedCode.outerHTML.replace(/<[^>]*>?/gm, "");

      block.querySelector("button.button-copy-code").innerHTML = copiedIcon;
      setTimeout(function () {
          block.querySelector("button.button-copy-code").innerHTML = copyIcon;
      }, 2000);

      const parsedHTML = htmlDecode(html);

      await navigator.clipboard.writeText(parsedHTML);
  }

  function htmlDecode(input) {
      const doc = new DOMParser().parseFromString(input, "text/html");
      return doc.documentElement.textContent;
  }

  async function searchInMarkdownFiles(searchTerm) {
    const queryFiles = document.querySelectorAll('#links-container .dropdown-item');
    const resultsContainer = document.getElementById("textarea");
    const fileNameContainer = document.getElementById("title");
    resultsContainer.innerHTML = "";
    fileNameContainer.innerHTML = "";
    let searchResults = [];
    queryFiles.forEach(link => {
        const file = link.getAttribute('data-url');
        fetch(file)
            .then(response => response.text())
            .then(text => {
                const lines = text.split('\n');
                let inCodeBlock = false;
                let codeBlockContent = '';
                let fileName = '';
    
                lines.forEach((line, index) => {
                    if (line.trim().startsWith('```')) {
                        inCodeBlock = !inCodeBlock;
                        if (inCodeBlock) {
                            fileName = file;
                        } else {
                            if (codeBlockContent.includes(searchTerm)) {
                                searchResults.push({ fileName, content: codeBlockContent });
                            }
                            codeBlockContent = '';
                            inCodeBlock = false;
                        }
                    } else if (inCodeBlock) {
                        codeBlockContent += line + '\n'; 
                    }
                });
    
                if (codeBlockContent.includes(searchTerm)) {
                    searchResults.push({ fileName, content: codeBlockContent });
                }
                if (searchResults.length > 0) {
                    const markdownText = searchResults.map(result => {
                        return '```\n' + result.content.trim() + '\n```';
                    }).join('\n\n');
                    const textContent = ' '; 
                    convertMarkdownToHtml(markdownText, textContent);
                }
            })
            .catch(error => {
                console.error(`Error fetching ${file}:`, error);
            });
    });
}

document.getElementById("searchbar").addEventListener("submit", function(event) {
    event.preventDefault();
    const searchTerm = document.getElementById("searchInput").value.trim();
    if (searchTerm) {
        searchInMarkdownFiles(searchTerm);
    } else {
        alert("Please enter a search term.");
    }
});
});
