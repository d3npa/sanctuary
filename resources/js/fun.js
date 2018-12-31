function htmlDecode(input){
    // https://css-tricks.com/snippets/javascript/unescape-html-in-js/
    var e = document.createElement('div');
    e.innerHTML = input;
    return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

function rollingData(div, data, delimiter="\n", delay=25, callback=null) {
    // 与えた配列の内容を一字ごとに出力する
    div.removeAttribute("hidden");
    div.innerHTML = (data[0] == delimiter) ? delimiter : "";
    data = data.split(delimiter);
    function update(data) {
        string = data.shift();
        if (string == null) {
            // div.innerHTML = htmlDecode(div.innerHTML);
            if (callback != null) callback();
            return;
        }
        setTimeout(function () {
            div.innerHTML += string + delimiter;
            update(data);
        }, delay);
    }
    update(data);

}
