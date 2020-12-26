$(document).ready(function() {
    console.log("ayyy tone");

    $("#btn-img-upload").click(function(event){
        event.preventDefault();
        console.log("boo");

        let fd = new FormData();
        let fileInput = document.getElementById('img');

        
        if(fileInput.files.length == 0) {
            alert("please select a image to upload");
        } 
        
        else {
            
            let img = fileInput.files[0];
    
            fd.append('file',img);
    
            console.log(fileInput.files) 

            // clear the form
            document.getElementById("upload-form").reset();
            

            $.ajax({
                url: '/upload',
                type: 'post',
                data: fd,
                contentType: false,
                // contentType: "multipart/form-data",
                processData: false,
                success: function(response){

                },
                failure: function(jqXhr, textStatus, errorThrown) {       
            
                    console.log(errorThrown);
                } 
            });
        }
        

    
        // alert("hello there!");
    });


});





