document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('floatingTextarea');
    const submitButton = document.getElementById('postSubmit');
    const fileInput = document.getElementById('inputGroupFile01');
    


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

});
