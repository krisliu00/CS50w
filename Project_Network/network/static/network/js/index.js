document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('floatingTextarea');
    const submitButton = document.getElementById('postSubmit');
    const fileInput = document.getElementById('inputGroupFile01');
    profilePhotoUpload();




    textarea.addEventListener('input', function() {
        if (textarea.value.trim().length > 0) {
            submitButton.classList.remove('disabled');
        } else {
            submitButton.classList.add('disabled');
        }
    });


    fileInput.addEventListener('change', previewImages);

    function previewImages(event) {
        var input = event.target;
        var files = input.files;
        var maxFiles = 4;

        var img_thumb = document.querySelector('#img_thumb');
        img_thumb.innerHTML = '';

        if (files.length > maxFiles) {
            alert('You can only select a maximum of ' + maxFiles + ' images');
            img_thumb.innerHTML = '';
            return;
        }

        function handleFile(file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var dataURL = e.target.result;
                var img = document.createElement('img');
                img.src = dataURL;
                img.classList.add('image-thumb');
                img.style.maxWidth = '80%';
                img.style.maxHeight = '80%';
    
                var container = document.createElement('div');
                container.classList.add('image-container');
                container.appendChild(img);
    
                var deleteBtn = document.createElement('badge');
                deleteBtn.classList.add('delete-btn');
                deleteBtn.innerHTML= 'X';
                deleteBtn.addEventListener('click', function() {
                    container.parentNode.removeChild(container);
                });
                container.appendChild(deleteBtn);
    
                img_thumb.appendChild(container);
            };
            reader.readAsDataURL(file);
        }
    
       
        for (var i = 0; i < files.length; i++) {
            handleFile(files[i]);
        }
    }   

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    
    function profilePhotoUpload() {
        const saveProfileButton = document.getElementById('save_profile');
        const modalCloseButton = document.getElementById('modalclosebutton');
        const usernameElement = document.getElementById('username');
        const profilePhoto = document.getElementById('userphoto_container');
        const modal = document.getElementById('exampleModal');
        const photoUploadInput = document.getElementById('photoUpload');

        let tempImageURL = null;

        if (modal && saveProfileButton) {

            modal.addEventListener('shown.bs.modal', function() {
                const username = usernameElement.textContent || usernameElement.value;
                const timestamp = new Date().getTime();
                const imagePath = `/media/Profile_Photo/${username}/head.png?${timestamp}`;
                profilePhoto.src = imagePath;
                profilePhoto.style.display = 'block';
            });

        if (photoUploadInput) {
            photoUploadInput.addEventListener('change', function(event) {
                if (event.target.files && event.target.files.length > 0) {
                    const selectedFile = event.target.files[0];
                    const reader = new FileReader();
    
                    reader.onload = function(e) {
                        tempImageURL = e.target.result;
                        profilePhoto.src = tempImageURL;
                    };
    
                    reader.readAsDataURL(selectedFile);
                }
            });
        }
    
        if (saveProfileButton) {
            saveProfileButton.addEventListener('click', function() {
                if (tempImageURL) {

                    fetch(tempImageURL)
                        .then(response => response.blob())
                        .then(blob => {
                            const formData = new FormData();
                            formData.append('image', blob);
                
                            fetch('/upload', {
                                credentials: "same-origin",
                                headers: {
                                    'X-CSRFToken': getCookie('csrftoken') 
                                },
                                method: 'POST',
                                body: formData
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    profilePhoto.src = tempImageURL;
                                } else {
                                    alert('Image upload failed!');
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                alert('An error occurred while uploading the image.');
                            });
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('An error occurred while fetching the image.');
                        });
                }
            });
        }
        
        if (modalCloseButton) {
            modalCloseButton.addEventListener('click', function() {
                tempImageURL = null;
                profilePhoto.src = ''; 
            });
        }
    }
}
});
