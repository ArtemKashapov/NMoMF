btn = document.getElementById('calculate');
scheme = document.getElementById('scheme-shooser')

implicitFlag = false

btn.addEventListener('click', run);
function run() {
    params = {
        'I': document.getElementById('I').value,
        'K': document.getElementById('K').value,
        'l': document.getElementById('l').value,
        'T': document.getElementById('T').value,
        'c': document.getElementById('c').value,
        'k': document.getElementById('k').value,
        'R': document.getElementById('R').value,
        'alpha': document.getElementById('alpha').value,
    }
    console.log(params)
    eel.run(params)
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
    if (implicitFlag) {
        document.body.setAttribute('class', 'change')
    } else {
        document.body.setAttribute('class', '')
    }
}

eel.expose(getScheme)
function getScheme() {
    if (implicitFlag) {
        return '1'
    } else {
        return '0'
    }
}