// draw upload contents

function getPublicImages() {

    

    $.ajax({
        type: 'get',
        url: '/get_images',
        contentType: false,
        // contentType: "multipart/form-data",
        processData: false,

        // the response
        dataType: "json",
        success: function(response){
            // console.log(response.length);
            displayImages(response);
        },
        failure: function(jqXhr, textStatus, errorThrown) {       
            console.log(errorThrown);
        } 
    });

}

function getFavorites() {

}

function getUploads() {

}

function clearImages() {
    $("#image-display-section").empty();
}


// clears thje username and password fields
function resetLogin() {
    document.getElementById("user_name").value = '';
    document.getElementById("user_psw").value = '';
    return;
}

function deleteImage(img_id) {
    
    // send delete request 
    let toSend = {"file_id" : img_id}
    toSend = JSON.stringify(toSend);

    $.ajax({
        type:"delete",
        url: "/del_image",

        // What we are sending
        data: toSend,
        contentType: "application/json",
        processData: false,        

        // the response
        // dataType: "json",
        success: function(response, textstatus, xhr){
            getPublicImages()       
        },

        failure: function(jqXhr, textStatus, errorThrown) {
            // console.log(errorThrown);
        } 
    });

}

function getLoggedIn() {

}

function displayImages(json) {

    // clear first
    $("#image-display-section").empty();

    // there will be an array of jsons, each element will be a 

    // do an ajax request to get the user id currently logged in. 


    for(i = 0 ; i < json.length; i++) {

        // get required data
        let id = json[i]["file_id"];
        let owner = json[i]["user_id"];
        let name = json[i]["filename"];
        let extension = json[i]["filetype"];
        let source = `uploads/${id}.${extension}`;
        let displaySection = document.getElementById("image-display-section");

        // create the outer div
        let outerDiv = document.createElement("div");
        outerDiv.setAttribute("class", "col");
        outerDiv.setAttribute("data-owner", owner);

        // the inner div
        let innerDiv = document.createElement("div");
        innerDiv.setAttribute("class", "card shadow-sm");

        // image element
        let image = document.createElement("img");
        image.setAttribute("src", source);
        image.setAttribute("width", "100%"); 
        image.setAttribute("height", "100%");

        // body div
        let bodyDiv = document.createElement("div");
        
        // body text contaning the name
        let bodyText = document.createElement("p");
        bodyText.setAttribute("class", "card-text");
        bodyText.textContent = name;

        // favorite button () - extra
        // delete button (if applicable)
        let delButton = document.createElement("button");
        delButton.setAttribute("class", "del-btn");
        delButton.setAttribute("onclick", `deleteImage(${id})`);
        // delButton.setAttribute("onclick", `deleteImage(${id}, ${owner})`);
        delButton.textContent = "Delete";
        // delButton.setAttribute("onclick", "getFavorites()");

        bodyDiv.appendChild(bodyText);
        bodyDiv.appendChild(delButton);
        innerDiv.appendChild(image);
        innerDiv.appendChild(bodyDiv);
        outerDiv.appendChild(innerDiv);
        displaySection.appendChild(outerDiv);
    }


    



}

$(document).ready(function() {

    getPublicImages();
    
    $("#btn-img-upload").click(function(event){
        event.preventDefault();
    
        let fileInput = document.getElementById('img');
        
        console.log()
        
        if(fileInput.files.length == 0) {
            alert("please select a image to upload");
        } 
        
        else {
            

            let numImages = fileInput.files.length;
            
            
            for(let i = 0; i < numImages; i++) {
    
                let fd = new FormData();
                let img = fileInput.files[i];
                fd.append('file', img);

                // console.log(fileInput.files[i]);

                $.ajax({
                    // url: '/upload',
                    url: '/multiupload',
                    type: 'post',
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function(response){
                        
                    },
                    failure: function(jqXhr, textStatus, errorThrown) {       
                        console.log(errorThrown);
                    }, 
                    
                });
            }
            
            getPublicImages();
            document.getElementById("upload-form").reset();

        }
        
    });
    
    
    $("#user_login").click(function(event) {
    
        event.preventDefault();
        let dataToSend = $("#login").serializeArray(); 
        dataToSend = JSON.stringify(dataToSend);  
    
        $.ajax({
            type:"post",
            url: "/login",
            data: dataToSend,
    
            // what the response will be
            dataType: "json",

            // What we are sending
            contentType: "application/json",
            processData: false,
            statusCode: {
                404: function() {
                    resetLogin();
                    alert("Username does not exist.");
                    
                },
                401: function() {
                    resetLogin();
                    alert("Invalid password.");
                }

            },
            success: function(response, textstatus, xhr){

                console.log(response)
                location.reload();

            },
            failure: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }        
        });    
        
    });

    // logout button
    $("#logout").click(function(event) {

        $.ajax({
            type:"post",
            url: "/logout",
            success: function(response, textstatus, xhr){
                location.reload();
            },
            failure: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            } 
        });
    });
    
});








