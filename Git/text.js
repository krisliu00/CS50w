function renderEmailContents(email) {

    const emailsContent = document.getElementById('mail_content');
    emailsContent.innerHTML = '';
    
    const emailDiv = document.createElement('dl');
    emailDiv.dataset.id = email.id;
    emailDiv.dataset.archived = email.archived;
    const mailboxContent = document.getElementById('mailbox_content');
    const mailboxType = mailboxContent.dataset.mailboxType;
  
    const inboxHTML = mailboxType === 'inbox' ?
    `
    <button id="archive-button" type="button" class="btn btn-success">Archive</button>
    <button id="reply-button" type="button" class="btn btn-primary">Reply</button>
    ` :
    '';
    const archiveboxHTML = mailboxType === 'archived' ?
    `
    <button id="archive-button" type="button" class="btn btn-success">UnArchive</button>
    ` :
    '';
  
    emailDiv.innerHTML = `
      <dl id="mail_content" class="row">
        <dt class="col-sm-3">Subject</dt>
        <dd class="col-sm-9">${email.subject}</dd>
  
        <dt class="col-sm-3">${email.timestamp}</dt>
        <dd class="col-sm-9">
            <p>From:&nbsp${email.sender} &nbsp&nbsp&nbspTo:&nbsp${email.recipients}</p>
            <p>${email.body}</p>
        </dd>
      </dl>
      ${inboxHTML}
      ${archiveboxHTML}
    `;
  
      emailsContent.appendChild(emailDiv);
      const archiveButton = document.getElementById('archive-button');
    if (archiveButton) {
      archiveButton.addEventListener('click', () => {
        archived(email.id)
        console.log('Archive button clicked');
        document.querySelector('#inbox').click();
      });
    }
    if ()
  }
  
  function mailContent(emailId, mailboxType) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#mailbox_content').style.display = 'none';
    document.querySelector('#reply-form').style.display = 'none';
    document.querySelector('#mail_content').style.display = 'block';
  
    fetch(`/emails/${emailId}`, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(email => {
      console.log('Returned emails:', email);
      renderEmailContents(email, mailboxType);
     
      if (mailboxType === 'inbox') {
      const replyButton = document.createElement('button');
      replyButton.className = 'btn btn-primary';
      replyButton.textContent = 'Reply';
      const mailContent = document.getElementById('mail_content');
      mailContent.appendChild(replyButton);
      replyButton.addEventListener('click', () => {
        replyToEmail(email);
      });
      // document.querySelector('#mail_content').appendChild(replyButton);
      }
    })
    .catch(error => {
      console.error('Error fetching inbox email:', error);
    });
}