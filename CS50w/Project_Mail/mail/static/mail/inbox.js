document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {
    
    load_mailbox('inbox');
    inbox_mailbox();

  });
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#sent').addEventListener('click', () => {
    sent_mailbox(); 
  });

  document.querySelector('#archived').addEventListener('click', () => {
    load_mailbox('archive');
    archive_mailbox();
  
});
  
  document.querySelector('#compose_submit').addEventListener('click', function(event) {
    event.preventDefault(); 
    send_email(); 
  });

  inbox_mailbox();

  function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#mailbox_content').style.display = 'none';
    document.querySelector('#mail_content').style.display = 'none';
    
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  function load_mailbox(mailbox) {
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mail_content').style.display = 'none';
    document.querySelector('#mailbox_content').style.display = 'block';
    
  
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

function renderEmails(emails) {
  const emailsContent = document.getElementById('mailbox_content');
  emailsContent.innerHTML = '';

  emails.forEach(email => {
      const emailDiv = document.createElement('div');
      emailDiv.classList.add('list-group-item', 'list-group-item-action');
      emailDiv.dataset.id = email.id;
      emailDiv.dataset.archived = email.archived
      

      emailDiv.innerHTML = `
          <div class="d-flex w-100 justify-content-between">
              <h5 class="mb-1">${email.subject}</h5>
              <small>${email.timestamp}</small>
          </div>
          <p class="mb-1">${email.body}</p>
          <small>From: ${email.sender} To: ${email.recipients}</small>
      `;
      emailDiv.addEventListener('click', function() {
        const emailId = this.dataset.id;
        mailContent(emailId) ; 
      });
      emailsContent.appendChild(emailDiv);
      
  });
}

function inbox_mailbox() {
    document.querySelector('#mailbox_content').style.display = 'block';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mail_content').style.display = 'none';
    

    fetch('/emails/inbox', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(emails => {  renderEmails(emails);})
    .catch(error => {
        console.error('Error fetching inbox emails:', error);
    });
}

function sent_mailbox() {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mail_content').style.display = 'none';
    document.querySelector('#mailbox_content').style.display = 'block';

    fetch('/emails/sent', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(emails => renderEmails(emails))
    .catch(error => {
        console.error('Error fetching sent emails:', error);
    });
}

function archive_mailbox() {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mail_content').style.display = 'none';
    document.querySelector('#mailbox_content').style.display = 'block';

    fetch('/emails/archive', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(emails => renderEmails(emails))
    .catch(error => {
        console.error('Error fetching sent emails:', error);
    });


}

function renderEmailContents(email) {

  const emailsContent = document.getElementById('mail_content');
  emailsContent.innerHTML = '';
  
  const emailDiv = document.createElement('dl');
  emailDiv.dataset.id = email.id;
  emailDiv.dataset.archived = email.archived;

    if (!email.archived) {
      emailDiv.innerHTML = `
          <dd class="col-sm-9">${email.timestamp}</dd>
          <dt class="col-sm-3">From:&nbsp${email.sender} &nbsp&nbsp&nbspTo:&nbsp${email.recipients}</dt>
          <dt class="col-sm-3">Subject</dt>
          <dd class="col-sm-9">
            <p>${email.subject}</p>
            <p>${email.body}</p>
          </dd>
      `;
    } else {
      emailDiv.innerHTML = `
          <dd class="col-sm-9">${email.timestamp}</dd>
          <dt class="col-sm-3">From:&nbsp${email.sender} &nbsp&nbsp&nbspTo:&nbsp${email.recipients}</dt>
          <dt class="col-sm-3">Subject</dt>
          <dd class="col-sm-9">
            <p>${email.subject}</p>
            <p>${email.body}</p>
          </dd>
      `;
    }

    emailsContent.appendChild(emailDiv);
}

function mailContent(emailId) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mailbox_content').style.display = 'none';
  document.querySelector('#mail_content').style.display = 'block';

  fetch(`/emails/${emailId}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(email => {
    console.log('Returned emails:', email);
    renderEmailContents(email);
  })
  .catch(error => {
    console.error('Error fetching inbox email:', error);
  });

}
// function archived(emailId) {
//   document.querySelector('#emails-view').style.display = 'none';
//   document.querySelector('#compose-view').style.display = 'none';
//   document.querySelector('#mailbox_content').style.display = 'none';
//   document.querySelector('#mail_content').style.display = 'block';

//   fetch(`/emails/${emailId}`, {
//     method: 'PUT',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({
//       archived: true
//     })
//   })
//   .then(response => {
//     if (!response.ok) {
//       throw new Error(`HTTP error! Status: ${response.status}`);
//     }
//   })
//   .catch(error => {
//     console.error('Error archiving email:', error);
//   });
// }

});
