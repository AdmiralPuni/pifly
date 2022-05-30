//change the nav button to active according to url


$(document).ready(function() {
	var url = window.location.pathname;
	var filename = url.substring(url.lastIndexOf('/')+1);
	if(filename==""){
        $("#nav-home").addClass("active");
	}
    else if(filename=="transaction"){
        $("#nav-transaction").addClass("active");
    }
});