document.addEventListener('DOMContentLoaded', function() {
    profilePhotoUpload();

    function profilePhotoUpload() {
        const saveProfileButton = document.getElementById('save_profile');
        const modal = document.getElementById('exampleModal');
        const usernameElement = document.getElementById('username');
        const profilePhoto = document.getElementById('userphoto_container');

        if (modal && saveProfileButton) {

            modal.addEventListener('shown.bs.modal', function() {
                const username = usernameElement.textContent || usernameElement.value;
                const imagePath = `/media/Profile_Photo/${username}/head.png`;
                profilePhoto.src = imagePath;
                profilePhoto.style.display = 'block';
            });
    
            saveProfileButton.addEventListener('click', function() {

                
                const formData = new FormData();
                formData.append('image', photoUploadButton.files[0]);
            
                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Image uploaded successfully!');
                    } else {
                        alert('Image upload failed!');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while uploading the image.');
                });


            });

        }
    }


});