var ctx = document.getElementById('canvas').getContext('2d');
var chart = new Chart(ctx, {
type: 'line',
data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
    label: 'Votre Poids (KG)',
    data: [70, 75, 86, 78, 70, 68, 62, 64, 65, 69, 70, 78],
    backgroundColor: [
        'rgb(112, 44, 246,0.3)',
      ],
    borderColor: [
        'rgb(112, 44, 246,0.6)',
      ],
    tension: 0.1
    },{
    label: 'Votre Objectif (KG)',
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
      label: 'Votre Objectif (KG)',
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