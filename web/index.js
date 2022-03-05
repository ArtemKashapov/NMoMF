btn = document.getElementById('calculate');


btn.addEventListener('click', run);
function run() {
    eel.run()
}

eel.expose(setProgress)
function setProgress(progress) {
    let progressBar = document.getElementById('progress-bar')
    let progressVal = document.getElementById('progress-value')

    progressBar.setAttribute('style', "--i: " + progress + ";")
    progressVal.textContent = progress + "%"
}