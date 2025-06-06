// chart_previsions.js

// Charger la liste des villes (à coder selon ta source ou un fichier statique)
const villes = ["Douala", "Yaounde", "Bafoussam"];
const selectVille = document.getElementById('choix-ville');
const ctxTemp = document.getElementById('chart-temp').getContext('2d');
let chartTemp;

// Initialisation du menu déroulant
villes.forEach(ville => {
  const opt = document.createElement('option');
  opt.value = ville;
  opt.textContent = ville;
  selectVille.appendChild(opt);
});

// Fonction pour afficher les prévisions
async function afficherPrevisions(ville) {
  const resp = await fetch(`/api/previsions/${ville}`);
  const data = await resp.json();

  // Extraire labels (heures) et valeurs (température)
  const labels = data.map(pt => pt.date);
  const tempData = data.map(pt => pt.temperature);

  // Si un chart existe déjà, le détruire
  if (chartTemp) chartTemp.destroy();

  // Créer le graphique
  chartTemp = new Chart(ctxTemp, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Température (°C)',
        data: tempData,
        tension: 0.3
      }]
    },
    options: {
      scales: {
        x: { display: true, title: { display: true, text: 'Date & Heure' } },
        y: { display: true, title: { display: true, text: 'Température (°C)' } }
      }
    }
  });
}

// Événement de changement de ville
selectVille.addEventListener('change', e => afficherPrevisions(e.target.value));

// Afficher les prévisions pour la première ville au chargement
window.onload = () => afficherPrevisions(villes[0]);