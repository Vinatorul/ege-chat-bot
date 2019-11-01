function showhelp() {
    var help = document.getElementById("help");
    if (help.style.display == "block") {
        help.setAttribute("style", "display:none");
    }
    else {
	var help_button = document.getElementById("help_button");
        help.setAttribute("style", "display:block");
	var top = help_button.offsetTop	- help.clientHeight - 50;
	help.setAttribute("style", "display:block; top:" + top + "px");
    }
}
