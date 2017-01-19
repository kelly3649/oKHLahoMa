var filenoodle = document.getElementById("noot");
var labelnoodle = document.getElementById("file-label");

filenoodle.onchange = function() {
    loadPhoto();
    labelnoodle.innerHTML = this.value.substr(12);
    filethings = document.getElementById("file-things");

};

var loadPhoto = function() {
    var formnoodle = document.getElementById("datform");
    var file = document.getElementById("noot").files[0];
    var reader = new FileReader();
    reader.onload = function(imgfile) {
	document.getElementById("lul").value = imgfile.target.result;
	var submitButton = document.createElement("INPUT");
	submitButton.setAttribute("type", "submit");
	submitButton.className += "btn btn-default";
	if (formnoodle.childElementCount < 3) {
	    formnoodle.appendChild(submitButton);
	}
	document.getElementById("thatimage").setAttribute("src", document.getElementById("lul").value);
    };
    reader.readAsDataURL(file);
};
