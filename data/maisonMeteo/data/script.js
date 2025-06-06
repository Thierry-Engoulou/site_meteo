document.addEventListener("DOMContentLoaded", () => {
    const dateActuelle = new Date();

    let jour = dateActuelle.getDate();
    let mois = dateActuelle.getMonth() + 1; 
    let annee = dateActuelle.getFullYear();
    let heure = String(dateActuelle.getHours()).padStart(2, '0');
    let minute = String(dateActuelle.getMinutes()).padStart(2, '0');
    let seconde = String(dateActuelle.getSeconds()).padStart(2, '0');

    document.getElementById('jour').innerHTML = jour;
    document.getElementById('mois').innerHTML = mois;
    document.getElementById('annee').innerHTML = annee;
    document.getElementById('heure').innerHTML = heure;
    document.getElementById('minute').innerHTML = minute;
    document.getElementById('seconde').innerHTML = seconde;
});
function actualiser(){
    const dateActuelle = new Date();

    let jour = dateActuelle.getDate();
    let mois = dateActuelle.getMonth() + 1; 
    let annee = dateActuelle.getFullYear();
    let heure = String(dateActuelle.getHours()).padStart(2, '0');
    let minute = String(dateActuelle.getMinutes()).padStart(2, '0');
    let seconde = String(dateActuelle.getSeconds()).padStart(2, '0');

    document.getElementById('jour').innerHTML = jour;
    document.getElementById('mois').innerHTML = mois;
    document.getElementById('annee').innerHTML = annee;
    document.getElementById('heure').innerHTML = heure;
    document.getElementById('minute').innerHTML = minute;
    document.getElementById('seconde').innerHTML = seconde;
}
setInterval(actualiser,500);




setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("press").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "pression", true);
    xhttp.send();
},500);


setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("hum").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "humidite", true);
    xhttp.send();
},500);

setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("air").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "air", true);
    xhttp.send();
},500);

setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("vent").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "vent", true);
    xhttp.send();
},500);


setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("temp").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "temperature", true);
    xhttp.send();
},500);

setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("uv").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "intensite", true);
    xhttp.send();
},500);

setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            valueT = this.responseText;
            document.getElementById("pluie").innerHTML = valueT;
        }
    };
    xhttp.open("GET", "pluie", true);
    xhttp.send();
},500);