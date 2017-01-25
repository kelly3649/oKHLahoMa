/* upload button etc stuff */
var filenoodle = document.getElementById("noot");
var labelnoodle = document.getElementById("file-label");
var formnoodle = document.getElementById("datform");

filenoodle.onchange = function() {
    loadPhoto();
    //labelnoodle.innerHTML = this.value.substr(12);
    filethings = document.getElementById("file-things");
    labelnoodle.innerHTML = "Browse";
};

var loadPhoto = function() {

    var file = document.getElementById("noot").files[0];
    var reader = new FileReader();
    reader.onload = function(imgfile) {
	document.getElementById("lul").value = imgfile.target.result;

	var caption = document.createElement("TEXTAREA");
	caption.setAttribute("id", "caption");
	caption.setAttribute("name", "caption");
	caption.setAttribute("rows", "3");
	caption.setAttribute("cols", "40");
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
	filter.setAttribute("id", "filterLabel");
	filter.setAttribute("for", "filterCheckbox");
	filter.innerHTML = "Use Mystery Filter of the Day: ";
	filter.appendChild(filterCheckbox);

	var spotifyCheckbox = document.createElement("INPUT");
	spotifyCheckbox.setAttribute("id", "spotifyCheckbox");
	spotifyCheckbox.setAttribute("type", "checkbox");
	spotifyCheckbox.setAttribute("name", "spotify");
	spotifyCheckbox.setAttribute("value", "spotify");

	var spotify = document.createElement("LABEL");
	spotify.setAttribute("id", "spotifyLabel");
	spotify.setAttribute("for", "spotifyCheckbox");
	spotify.innerHTML = "Search Spotify: ";
	spotify.appendChild(spotifyCheckbox);

	if (formnoodle.childElementCount == 1) {
	    formnoodle.innerHTML = formnoodle.innerHTML += "<br>";
	    formnoodle.appendChild(caption);
	    formnoodle.innerHTML = formnoodle.innerHTML += "<br>";
	    formnoodle.innerHTML = formnoodle.innerHTML += "<br>";
	    formnoodle.appendChild(filter);
	    formnoodle.innerHTML = formnoodle.innerHTML += "<br>";
	    formnoodle.appendChild(spotify);
	    formnoodle.innerHTML = formnoodle.innerHTML += "<br>";
	    formnoodle.innerHTML = formnoodle.innerHTML += "<br>";
	    formnoodle.appendChild(submitButton);
	}

	console.log(formnoodle.innerHTML);
	
	document.getElementById("thatimage").setAttribute("src", document.getElementById("lul").value);

    };
    reader.readAsDataURL(file);

};

var clear = function(){
    if (formnoodle.childElementCount > 1) {
	var caption = document.getElementById("caption");
	caption.parentNode.removeChild(caption);
	
	var filterCheckbox = document.getElementById("filterCheckbox");
	filterCheckbox.parentNode.removeChild(filterCheckbox);

	var filter = document.getElementById("filterLabel");
	filter.parentNode.removeChild(filter);
	
	var spotifyCheckbox = document.getElementById("spotifyCheckbox");
	spotifyCheckbox.parentNode.removeChild(spotifyCheckbox);
	
	var spotify = document.getElementById("spotifyLabel");
	spotify.parentNode.removeChild(spotify);

	var submitButton = document.getElementById("submitButton");
	submitButton.parentNode.removeChild(submitButton);

	formnoodle.innerHTML = formnoodle.innerHTML.replace(/<br>/g, ""); //regex
	
	document.getElementById("lul").value = "";
	document.getElementById("thatimage").setAttribute("src", "");
	labelnoodle.innerHTML = "Browse";
	


    }
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
