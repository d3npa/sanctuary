function htmlDecode(input){
    // https://stackoverflow.com/a/7394787
    var txt = document.createElement("textarea");
    txt.innerHTML = input;
    return txt.value;
}

closeTag = 0;
function rollingData(div, data, delimiter="\n", delay=25, callback=null) {
    // 与えた配列の内容を一字ごとに出力する
    div.removeAttribute("hidden");
    div.innerHTML = (data[0] == delimiter) ? delimiter : "";
    data = data.split(delimiter);
    function update(data) {
        string = data.shift();
        if (string == null) {
            if (callback != null) callback();
            return;
        }
        setTimeout(function () {
            div.innerHTML += string + delimiter;
            if (delimiter == "") {
                // 打つ途中にリンクをパースする
                if (string.includes("<")) {
                    closeTag = 1;
                }
                else if (string.includes("/") && closeTag == 1) {
                    closeTag = 2;
                }
                else if (string.includes(">") && closeTag == 2) {
                    div.innerHTML = htmlDecode(div.innerHTML);
                    closeTag = 0;
                }
                else if (closeTag != 2)
                    closeTag = 0;
            }
            else
                div.innerHTML = htmlDecode(div.innerHTML);
            update(data);
        }, delay);
    }
    update(data);
}

themes = ["amber", "green", "white", "pink"];
function changeColor(color) {
    if (themes.includes(color)) {
        document.cookie = "color=" + color;
        setColor(color);
    }
}

function setColor(color) {
    if (themes.includes(color)) {
    	for (var i = 3; i < document.styleSheets.length; i++)
            document.styleSheets[i].disabled = true;
        document.styleSheets[themes.indexOf(color) + 3].disabled = false;
        //document.getElementById("theme").setAttribute("href", "/css/theme-" + color + ".css");
    }
    else {
        setColor("green");
    }
}

setColor((document.cookie != "") ? document.cookie.split("=")[1] : "green");
