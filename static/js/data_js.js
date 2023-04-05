
function on_left() {
    const url = 'http://127.0.0.1:5000/json-view_table';
    var left = document.getElementById('left');               // получаем доступ к элементу input с id = "left"
    var _startLeft = left.dataset.startLeft;           // получаем значение атрибута data-start-left

    var count = document.getElementById('count_lines'); // получаем доступ к элементу input с id = "count_lines"
    var _countLines = count.dataset.countLines;  // получаем значение атрибута data-countLines

    const data = {
                countLines: parseInt(_countLines),
                startLeft: parseInt(_startLeft),
                startRight: 0
                };
    var bodyElement = document.body;
    var response = fetch(url,{
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify(data)
    })
    .then((response) => response.text())
    .then((text) => {
        bodyElement.innerHTML = text,
        console.log('Success:', response)
        })
    .catch((error) => {console.log('Error:') });
}

function on_right() {
    var url = 'http://127.0.0.1:5000/json-view_table';

    var right = document.getElementById('right');            // получаем доступ к элементу input с id = "right"
    var _startRight = right.dataset.startRight;        // получаем значение атрибута data-star-right

    var count = document.getElementById('count_lines'); // получаем доступ к элементу input с id = "count_lines"
    var _countLines = count.dataset.countLines;  // получаем значение атрибута data-countLines

    var data = {
                countLines: parseInt(_countLines),
                startRight: parseInt(_startRight),
                startLeft: 0
                };
    var bodyElement = document.body;
    var response = fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify(data)
    })
    .then((response) => response.text())
    .then((text) => {
        bodyElement.innerHTML = text,
        console.log('Success:', response)
        })
    .catch((error) => {console.log('Error:') });
}

function get_data() {
    var url = 'http://127.0.0.1:5000/json-view_table';

    var count = document.getElementById('count_lines'); // получаем доступ к элементу input с id = "count_lines"
    var _countLines = count.value;  // получаем значение атрибута value

    if (Number.isInteger(parseInt(_countLines))) {

    var data = {
                countLines: parseInt(_countLines),
                startRight: 0,
                startLeft: 0
                };
    var bodyElement = document.body;
    var response = fetch(url, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json; charset=utf-8'},
                        body: JSON.stringify(data)
                        })
    .then((response) => response.text())
    .then((text) => {
        bodyElement.innerHTML = text,
        console.log('Success:', response)
        })
    .catch((error) => {console.log('Error:') });
    } else { alert ("Введите число!");}
}
