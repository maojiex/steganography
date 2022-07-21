const form = document.querySelector("form")
const encode_btn =  document.getElementById('encode_btn')
var img = ''
imgInput = form.querySelector(".file-input")
uploadingArea = document.querySelector(".uploading")
uploadedArea = document.querySelector(".uploaded")

form.addEventListener("click", () => {
    imgInput.click();
});




imgInput.onchange = ({target}) => {
    img = target.files[0];
    if (img) {
        imgName = img.name;
        console.log(img);
        console.log(imgName)
        // uploadFile(imgName);
    }
}

// function uploadFile(name){
//     let xhr = new XMLHttpRequest();
//     xhr.open("POST", "php/upload.php");
//     xhr.upload.addEventListener('progress', e => {
//         console.log(e);
//     })
//     let formData = new FormData(form)
//     xhr.send(formData);
// }


// function readImage(file) {
//     // Check if the file is an image.
//     if (file.type && !file.type.startsWith('image/')) {
//       console.log('File is not an image.', file.type, file);
//       return;
//     }
  
//     const reader = new FileReader();
//     reader.addEventListener('load', (event) => {
//       img.src = event.target.result;
//     });
//     reader.readAsDataURL(file);
//   }


encode_btn.onclick = async function user(){
    // python -> javascript
    // 1. encode
    console.log(img)
    // 2. download
  
    const res = await eel.app()();
 

    
}

// TODO
// Login/Logout by Google Authentic, No database needed
// secret key
// database??
