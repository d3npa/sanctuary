function adaptStylesheets() {
    var width = document.getElementsByTagName("html")[0].clientWidth;
    if (width <= 1000) {
        // console.log("Thin detected");
        document.styleSheets[1].disabled = true;
        document.styleSheets[2].disabled = false;
    } else {
        // console.log("Wide mode");
        document.styleSheets[1].disabled = false;
        document.styleSheets[2].disabled = true;
    }
}

window.onresize = function(event) {
    adaptStylesheets();
}

adaptStylesheets();
