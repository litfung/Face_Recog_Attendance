var boxHeight = document.getElementById('capture-video').clientHeight;
var lv=document.getElementById("live-video").style.height =boxHeight+"px" ;
setInterval(function() {
	var boxHeight = document.getElementById('capture-video').clientHeight;
	var lv=document.getElementById("live-video").style.height =boxHeight+"px" ;
}, 100);
const hdConstraints = {
	video: {width: {min: 1280}, height: {min: 720}}
};
const captureVideoButton = document.querySelector('#screenshot .capture-button');
const screenshotButton = document.querySelector('#screenshot-button');
const img = document.querySelector('#screenshot img');
const video = document.querySelector('#screenshot video');
const btUp=document.querySelector('#bt_upload');
const frm=document.querySelector('#form-id');
const download=document.querySelector('#dl-btn-box');
const canvas = document.createElement('canvas');
frm.style.display="none";
screenshotButton.style.display="none";
download.style.display="none";

captureVideoButton.onclick = function() {
	
	navigator.mediaDevices.getUserMedia(hdConstraints).
	then(handleSuccess).catch(handleError);
};

screenshotButton.onclick = video.onclick = function() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    // Other browsers will fall back to image/png
    img.src = canvas.toDataURL('image/png');
    var imageDataURL = canvas.toDataURL('image/png');
    document.querySelector('#dl-btn').href = imageDataURL;
    download.style.display="flex";
    frm.style.display="flex";
};

function handleSuccess(stream) {
	captureVideoButton.style.display="none";
	screenshotButton.disabled = false;
	screenshotButton.style.display="block";
    video.srcObject = stream;
}

function handleError(error) {
	console.error('Error: ', error);
}

function prepareImg() {
   var imageDataURL = canvas.toDataURL('image/png');
   document.getElementById('inp_img').value = imageDataURL
}