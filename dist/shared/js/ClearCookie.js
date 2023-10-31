fetch('/clear_cookie', {
    method: 'POST',
    body: JSON.stringify({ new_value : 'None' }),
    headers: {
        'Content-Type' : 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    console.log(data.message)
})