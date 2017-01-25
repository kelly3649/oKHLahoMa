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

	
	var filterCheckbox = document.createElement("INPUT");
	filterCheckbox.setAttribute("id", "filterCheckbox");
	filterCheckbox.setAttribute("type", "checkbox");
	filterCheckbox.setAttribute("name", "filter");
	filterCheckbox.setAttribute("value", "filter");

	var filter = document.createElement("LABEL");
	filter.setAttribute("for", "filterCheckbox");
	filter.innerHTML = "Use Filter: ";
	filter.appendChild(filterCheckbox);

	var spotifyCheckbox = document.createElement("INPUT");
	spotifyCheckbox.setAttribute("id", "spotifyCheckbox");
	spotifyCheckbox.setAttribute("type", "checkbox");
	spotifyCheckbox.setAttribute("name", "spotify");
	spotifyCheckbox.setAttribute("value", "spotify");

	var spotify = document.createElement("LABEL");
	spotify.setAttribute("for", "spotifyCheckbox");
	spotify.innerHTML = "Search Spotify: ";
	spotify.appendChild(spotifyCheckbox);

	if (formnoodle.childElementCount < 5) {
	    formnoodle.appendChild(caption);
	    formnoodle.appendChild(document.createElement("br"));
	    formnoodle.appendChild(filter);
	    formnoodle.appendChild(document.createElement("br"));
	    formnoodle.appendChild(spotify);
	    formnoodle.appendChild(document.createElement("br"));
	    formnoodle.appendChild(submitButton);
	}
	document.getElementById("thatimage").setAttribute("src", document.getElementById("lul").value);

    };
    reader.readAsDataURL(file);

};

var clear = function(){
    var formnoodle = document.getElementById("datform");
    if (formnoodle.childElementCount >= 4) {
	var caption = document.getElementById("caption");
	caption.parentNode.removeChild(caption);
	var submitButton = document.getElementById("submitButton");
	submitButton.parentNode.removeChild(submitButton);
	var filterCheckbox = document.getElementById("filterCheckbox");
	filterCheckbox.parentNode.removeChild(filterCheckbox);
    }
    document.getElementById("lul").value = "";
    document.getElementById("thatimage").setAttribute("src", "");
    labelnoodle.innerHTML = "Browse";
};



/* modal stuff */
/* everything related to modal is code written by w3schools */
/* http://www.w3schools.com/howto/howto_css_modals.asp */
var btn = document.getElementById("upload");
var btn_wrapper = document.getElementById("upload-wrapper");
var modal = document.getElementById('myModal');
var span = document.getElementsByClassName("close")[0];

console.log(btn_wrapper.className);
console.log(btn_wrapper.className.length);

if (btn_wrapper.className == "") { //button isn't disabled, user can upload
    /* When the user clicks on the button, open the modal */
    btn.onclick = function() {
	modal.style.display = "block";
    }

    /* When the user clicks on <span> (x), close the modal */
    span.onclick = function() {
	clear();
	modal.style.display = "none";
    }

    /* When the user clicks anywhere outside of the modal, close it */
    window.onclick = function(event) {
	if (event.target == modal) {
	    clear();
            modal.style.display = "none";
	}
    }

}/* end of modal stuff */
else { //button disabled
    btn.


}
