// Formulaire d'ajout de donnees
let form = document.querySelector("form")

let step1 = document.getElementById("step1")
let step2 = document.getElementById("step2")
let btnStep1 = document.getElementById("btn-step1")

btnStep1.addEventListener('click', function () {
  step1.classList.replace("d-block", "d-none")
  step2.classList.replace("d-none", "d-block")
  window.scrollTo(0, 0);
})

form.weight.addEventListener('input', function () {
  validate_weight()
})

function validate_weight() {
  let weight = document.getElementById("weight")

  if (weight.value == "" || weight.value <= 20) {
      if (weight.classList.contains("is-valid"))
          weight.classList.replace("is-valid", "is-invalid")
      else
          weight.classList.add("is-invalid")
      return false
  }
  if (weight.classList.contains("is-invalid"))
      weight.classList.replace("is-invalid", "is-valid")
  else
      weight.classList.add("is-valid")
  return true
}

// Graphique de donnees

// TODO Recup les donnees de poids, taille, objectif de poids avec requete ajax

// Preparation de la requete ajax avec les donnees a recuperer du serveur
let formData = new FormData()
formData.append("goal_weight", 0)


// Envoi requete ajax au server
// const request = new Request('/social/update/', {method: 'POST', body: formData})
// fetch(request)
// .then(response => response.json())
// .then(result => {
//     console.log(result);
// })

// Graphique de donnees, sur les 15 derniers jours

var ctx = document.getElementById('canvas').getContext('2d');
var chart = new Chart(ctx, {
type: 'line',
data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
    label: 'Votre Poids (kg)',
    data: [70, 75, 86, 78, 70, 68, 62, 64, 65, 69, 70, 78],
    backgroundColor: [
        'rgb(112, 44, 246,0.3)',
      ],
    borderColor: [
        'rgb(112, 44, 246,0.6)',
      ],
    tension: 0.1
    },{
    label: 'Votre Objectif (kg)',
    data: [75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75],
    backgroundColor: [
        'rgb(242, 151, 0,0.3)',
      ],
    borderColor: [
        'rgb(242, 151, 0,0.6)',
      ],
    tension: 0.1   
    }],
    options: {
      scales: {
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Poids (kg)'
          }
        }],
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Mois'
          }
        }]
      }     
    }
    }
});

var cv = document.getElementById('imc');
var chart = new Chart(cv, {
  type: 'line',
  data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [{
      label: 'Votre IMC',
      data: [24, 22, 19, 22, 23, 23.5, 23, 22.8, 22, 21.9, 21.5, 20.5],
      backgroundColor: [
          'rgb(112, 44, 246,0.3)',
        ],
      borderColor: [
          'rgb(112, 44, 246,0.6)',
        ],
      tension: 0.1
      },{
      label: 'Votre Objectif (kg)',
      data: [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
      backgroundColor: [
          'rgb(242, 151, 0,0.3)',
        ],
      borderColor: [
          'rgb(242, 151, 0,0.6)',
        ],
      tension: 0.1   
      }],
      options: {
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Poids (kg)'
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Mois'
            }
          }]
        }     
      }
      }
  });