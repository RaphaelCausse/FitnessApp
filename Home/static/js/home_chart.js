
const ctx = document.getElementById('ptichart');
const today = new Date(); // Obtient la date actuelle
const lastFifteenDays = []; // Initialise un tableau vide

// Boucle pour ajouter les dates des 15 derniers jours dans le tableau
for (let i = 1; i <= 15; i++) {
  const date = new Date(today.getFullYear(), today.getMonth(), today.getDate() - i); // Obtient la date du jour précédent
  const day = date.getDate().toString().padStart(2, '0'); // Obtient le jour du mois en deux chiffres
  const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Obtient le mois en deux chiffres
  const formattedDate = `${day}/${month}`; // Combine le jour et le mois dans une chaîne de caractères au format "jj/mm"
  lastFifteenDays.push(formattedDate); // Ajoute la date formatée dans le tableau
}

// TODO Recup les calories sur les 15 derniers jours, depuis Activity et Food, avec requete ajax

// Preparation de la requete ajax avec les donnes a envoyer
let formData = new FormData()

// Envoi requete ajax au server
// const request = new Request('/social/update/', {method: 'POST', body: formData})
// fetch(request)
// .then(response => response.json())
// .then(result => {
//     console.log(result);
// })

new Chart(ctx, {
  type: 'bar',
  data: {
    labels: lastFifteenDays,
    datasets: [{
      label:"Calories",
      data: [0,0,0,0,0,234,0,245,0,1230,0,0,0,0,0],
      backgroundColor: [
        'rgb(242, 151, 0,0.3)',
      ],
      borderColor: [
        'rgb(242, 151, 0,0.6)',
      ],
      borderWidth: 2,
      maxBarThickness: 60,
      borderRadius: 5,
      minBarLength: 10,
  }]
  },
  options: {
    maintainAspectRatio: false,
    scales: {
      
      y: {
        beginAtZero: true,
        gridLines: {
          display: false
        }
      }
    }
  }
});