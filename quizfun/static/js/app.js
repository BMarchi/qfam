function resetForm() {
    var form = document.getElementById("question-form");
    form.reset();
}

function countdown() {
    var seconds;
    var temp;
    seconds = document.getElementById('countdown').innerHTML;
    seconds = parseInt(seconds, 10);
 
    if (seconds == 1) {
        seconds--;
        temp = document.getElementById('countdown');
        temp.innerHTML = seconds;
        noTime();
        return;
    }
 
    seconds--;
    temp = document.getElementById('countdown');
    temp.innerHTML = seconds;
    timeoutMyOswego = setTimeout(countdown, 1000);
}

function goIndex() {
    window.location.href = '/';
    return false;
}