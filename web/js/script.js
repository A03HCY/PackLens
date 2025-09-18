function callPython() {
    const name = document.getElementById('nameInput').value;
    pywebview.api.greet(name).then(response => {
        document.getElementById('response').innerText = response;
    });
}
