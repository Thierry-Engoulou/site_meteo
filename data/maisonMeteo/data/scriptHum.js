document.addEventListener("DOMContentLoaded", async function() {
    donneeT = await initialisation(); // Appeler la fonction
});

let donneeT=[];


async function initialisation() {
    return new Promise((resolve, reject) => {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    let value = this.responseText;
                    let valueT = separer(value);
                    let data = valueT.map(item => parseFloat(item)); // Assurez-vous que ce soit un tableau de nombres
                    resolve(data);
                } else {
                    reject("Erreur de chargement des données");
                }
            }
        };
        xhttp.open("GET", "Thumidite", true);
        xhttp.send();
    });
}


setInterval(function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let value1 = this.responseText;
            
            if (!isNaN(value1))
            {
                document.getElementById("Hum").innerHTML = value1;
                donneeT.shift(); // Retirer le premier élément
                donneeT.push(parseInt(value1)); // Ajouter la nouvelle valeur
                updateChart();
            }
           
        }
    };
    xhttp.open("GET", "humidite", true);
    xhttp.send();
}, 500);


function separer(text) {
    const segments = text.split(',');
    return segments;
  }


let graph1;


var ctx = document.getElementById('humidite').getContext('2d');
var data = {
    labels: ['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30',],
    datasets: [{
        label: 'Humidité',
        data: donneeT,
        borderColor: 'rgba(0, 0, 255, 1)',
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        fill: true
    }]
};

var options = {
    responsive: true,
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

var config = {
    type: 'line',
    data: data,
    options: options
};

graph1 = new Chart(ctx, config);

function updateChart() {
    graph1.data.datasets[0].data = donneeT;
    graph1.update();
}

