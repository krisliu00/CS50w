document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#sent').addEventListener('click', () => {
    sent_mailbox(); 
  });

  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  
  document.querySelector('#compose_submit').addEventListener('click', function(event) {
    event.preventDefault(); 
    send_email(); 
  });
  
  // By default, load the inbox
  load_mailbox('inbox');

  function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#mailbox_content').style.display = 'none';
    
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  function load_mailbox(mailbox) {
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mailbox_content').style.display = 'none';
    
  
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  }

  function send_email() {
    const recipients = document.getElementById("compose-recipients").value;
    const subject = document.getElementById("compose-subject").value;
    const body = document.getElementById("compose-body").value;
  
    fetch('/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        recipients,
        subject,
        body
      })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('error sending message', error));
  }
  
  function sent_mailbox() {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mailbox_content').style.display = 'block';

    fetch('/emails/sent', {
      method: 'GET'
    })
    .then(response => response.json())
    .then(emails => {
      const emailsContent = document.getElementById('mailbox_content');
      emailsContent.innerHTML = ''; // Clear previous content
  
      emails.forEach(email => {
        // Create a new div element for each email
        const emailDiv = document.createElement('div');
        emailDiv.classList.add('list-group-item', 'list-group-item-action');
  
        // Construct HTML content for the email
        emailDiv.innerHTML = `
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${email.subject}</h5>
            <small>${email.timestamp}</small>
          </div>
          <p class="mb-1">${email.body}</p>
          <small>From: ${email.sender}</small>
        `;
  
        // Append the email div to the emailsContent element
        emailsContent.appendChild(emailDiv);
      });
    })
    .catch(error => {
      console.error('Error fetching emails:', error);
    });
  }
  
});
