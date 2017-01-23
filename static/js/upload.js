/* upload button etc stuff */
var filenoodle = document.getElementById("noot");
var labelnoodle = document.getElementById("file-label");

filenoodle.onchange = function() {
    loadPhoto();
    //labelnoodle.innerHTML = this.value.substr(12);
    filethings = document.getElementById("file-things");
    labelnoodle.innerHTML = "Browse";
};

var loadPhoto = function() {
    var formnoodle = document.getElementById("datform");
    var file = document.getElementById("noot").files[0];
    var reader = new FileReader();
    reader.onload = function(imgfile) {
	document.getElementById("lul").value = imgfile.target.result;

	var caption = document.createElement("INPUT");
	caption.setAttribute("id", "caption");
	caption.setAttribute("name", "caption");
	caption.setAttribute("type", "text");
	caption.setAttribute("placeholder", "caption");

	var submitButton = document.createElement("INPUT");
	submitButton.setAttribute("id", "submitButton");
	submitButton.setAttribute("type", "submit");
	submitButton.setAttribute("value", "upload");
	submitButton.className += "btn btn-default";

	if (formnoodle.childElementCount < 3) {
	    formnoodle.appendChild(caption);
	    formnoodle.appendChild(submitButton);
	}
	document.getElementById("thatimage").setAttribute("src", document.getElementById("lul").value);

    };
    reader.readAsDataURL(file);

};

var clear = function(){
    var formnoodle = document.getElementById("datform");
    if (formnoodle.childElementCount >= 3) {
	var caption = document.getElementById("caption");
	caption.parentNode.removeChild(caption);
	var submitButton = document.getElementById("submitButton");
	submitButton.parentNode.removeChild(submitButton);
    }
    document.getElementById("lul").value = "";
    document.getElementById("thatimage").setAttribute("src", "");
    labelnoodle.innerHTML = "Browse";
};

/* modal stuff */

var modal = document.getElementById('myModal');
var btn = document.getElementById("upload");
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    clear();
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
	clear();
        modal.style.display = "none";
    }
}
