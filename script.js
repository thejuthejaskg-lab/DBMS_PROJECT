function addBook() {
    fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            id: document.getElementById("bid").value,
            title: document.getElementById("title").value,
            author: document.getElementById("author").value
        })
    })
    .then(res => res.json())
    .then(data => alert(data.status))
}

function getBook() {
    let id = document.getElementById("searchId").value
    fetch('/get/' + id)
        .then(res => res.json())
        .then(data => {
            if (data.status) {
                alert("Book not found")
            } else {
                alert(data.id + " | " + data.title + " | " + data.author)
            }
        })
}

function deleteBook() {
    fetch('/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            id: document.getElementById("searchId").value
        })
    })
    .then(res => res.json())
    .then(data => alert(data.status))
}

function loadBooks() {
    fetch('/list')
        .then(res => res.json())
        .then(data => {
            let list = document.getElementById("list")
            list.innerHTML = ""
            data.forEach(b => {
                let li = document.createElement("li")
                li.textContent = b.id + " - " + b.title + " - " + b.author
                list.appendChild(li)
            })
        })
}