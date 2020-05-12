Reveal.initialize({
  dependencies: [
    {src: '/static/node_modules/reveal.js-plugins/chart/Chart.min.js'},
    {src: '/static/node_modules/reveal.js-plugins/chart/plugin/chart/csv2chart.js'},
  ]
});
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
      type: 'line',
      data: {
	labels: ['2000','2001','2002','2003','2004','2005','2006','2007','2008'],
	datasets: [{
	  label: 'My First dataset',
	  borderColor: 'rgb(255, 99, 132)',
	  data: [66.4,79.7,91.4,109.4,101.0,104.4,118.7,116.6,114.9]
	}]
      },
      options: {
	legend: {
	  display: false,
	},
	tooltips: {
	  mode: 'index',
	  axis: 'y'
	},
      }
});

