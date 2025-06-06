// ... (Votre code JavaScript existant pour les graphiques et les mises à jour en temps réel)

// Fonction pour récupérer et afficher les prévisions de précipitations
async function fetchPredictions() {
    try {
        const response = await fetch('/predictions');
        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }
        const predictions = await response.json();
        displayPredictions(predictions);
    } catch (error) {
        console.error('Erreur lors de la récupération des prévisions :', error);
        // Gérer l'erreur (par exemple, afficher un message à l'utilisateur)
        document.getElementById('predictions-container').innerHTML =
            '<p class="text-red-500">Impossible de récupérer les prévisions de précipitations.</p>';
    }
}

// Fonction pour afficher les prévisions dans le HTML
function displayPredictions(predictions) {
    const container = document.getElementById('predictions-container');
    container.innerHTML = ''; // Effacer le contenu précédent

    if (predictions && predictions.length > 0) {
        const ul = document.createElement('ul');
        ul.classList.add('list-disc', 'list-inside', 'space-y-2');
        predictions.forEach(day => {
            const li = document.createElement('li');
            li.classList.add('text-lg');
            li.textContent = `${day.day} : ${day.precipitation_risk}% de risque de précipitations`;
            ul.appendChild(li);
        });
        container.appendChild(ul);
    } else {
        container.innerHTML = '<p>Aucune prévision disponible.</p>';
    }
}

// Appeler la fonction pour récupérer les prévisions au chargement de la page
fetchPredictions();

// Mettre à jour les prévisions toutes les heures (par exemple)
setInterval(fetchPredictions, 3600000);
