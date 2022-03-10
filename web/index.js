btn = document.getElementById('calculate');
scheme = document.getElementById('scheme-shooser')

implicitFlag = false

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

scheme.onchange = function() {
    implicitFlag = !implicitFlag
    console.log(implicitFlag)
    // eel.change_scheme()
}

eel.expose(getScheme)
function getScheme() {
    if (implicitFlag) {
        return '1'
    } else {
        return '0'
    }
}