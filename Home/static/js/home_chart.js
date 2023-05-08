
const ctx = document.getElementById('ptichart');

//Recup les calories sur les 15 derniers jours, depuis Activity et Food, avec requete ajax

let chart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [],
    datasets: [{
      label:"Calories",
      data: [],
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


let formData = new FormData()
formData.append("dates", [])
formData.append("calories", [])
// Envoi requete ajax au server
const request = new Request('/home/ajax', {method: 'POST', body: formData})
fetch(request)
.then(response => response.json())
.then(result => {
    // Chart des calories
    chart.data.labels = result.dates
    chart.data.datasets[0].data = result.calories
    chart.update()
})