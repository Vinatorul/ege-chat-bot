function showhelp() {
    var help = document.getElementById("help");
    if (help.style.display == "block") {
        help.setAttribute("style", "display:none");
    }
    else {
        help.setAttribute("style", "display:block");
    }
}