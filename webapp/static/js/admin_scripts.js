document.addEventListener("DOMContentLoaded", function() {
    const addWordForm = document.getElementById("addWordForm");
    const deleteWordForm = document.getElementById("deleteWordForm");
    const updateRegexForm = document.getElementById('updateRegexForm');
    const testRegexForm = document.getElementById("testRegexForm");
    const currentWordsDiv = document.getElementById("currentWords");
    const regexTestResultDiv = document.getElementById("regexTestResult");

   function updateCurrentWords() {
    fetch('/api/admin/words')
        .then(response => response.json())
        .then(data => {
            // 创建表格元素
            const table = document.createElement('table');
            table.style.borderCollapse = 'collapse';
            table.style.width = '100%';

            // 创建表头
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            const headers = ['Word', 'Regex', 'Type'];

            headers.forEach(headerText => {
                const th = document.createElement('th');
                th.textContent = headerText;
                th.style.border = '1px solid black';
                th.style.padding = '8px';
                th.style.backgroundColor = '#f2f2f2';
                headerRow.appendChild(th);
            });

            thead.appendChild(headerRow);
            table.appendChild(thead);

            // 创建表格主体
            const tbody = document.createElement('tbody');

            // 处理 data.words 中的元组
            data.words.forEach(item => {
                const row = document.createElement('tr');

                const wordCell = document.createElement('td');
                wordCell.textContent = item[0]; // 第一个元素为敏感词
                wordCell.style.border = '1px solid black';
                wordCell.style.padding = '8px';
                row.appendChild(wordCell);

                const regexCell = document.createElement('td');
                regexCell.textContent = item[1]; // 第二个元素为正则表达式
                regexCell.style.border = '1px solid black';
                regexCell.style.padding = '8px';
                row.appendChild(regexCell);

                const typeCell = document.createElement('td');
                typeCell.textContent = item[2]; // 第三个元素为类型
                typeCell.style.border = '1px solid black';
                typeCell.style.padding = '8px';
                row.appendChild(typeCell);

                tbody.appendChild(row);
            });

            table.appendChild(tbody);

            // 将表格添加到页面的指定位置
            currentWordsDiv.innerHTML = ''; // 清空之前的内容
            currentWordsDiv.appendChild(table);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

    addWordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const addWordInput = document.getElementById('addWordInput').value;

        fetch('/api/admin/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ word: addWordInput }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updateCurrentWords();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    deleteWordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const deleteWordInput = document.getElementById('deleteWordInput').value;

        fetch('/api/admin/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ word: deleteWordInput }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updateCurrentWords();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    updateRegexForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const word = document.getElementById('wordInput').value;
        const newRegex = document.getElementById('newRegexInput').value;

        fetch('/api/admin/update_regex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ word: word, new_regex: newRegex }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updateCurrentWords();  // 更新页面上显示的敏感词列表
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    testRegexForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const testRegexInput = document.getElementById('testRegexInput').value;

        fetch('/api/admin/test_regex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: testRegexInput }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.matched) {
                regexTestResultDiv.innerHTML = "Match found!";
            } else {
                regexTestResultDiv.innerHTML = "No match found.";
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    updateCurrentWords();
});
