// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}


// Pie Chart Example
var ctxPie = document.getElementById("myPieChart");
var pieChartConfig = {
  type: 'doughnut',
  data: {
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#F4D03F', '#85929E'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#D4AC0D', '#34495E'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: true
    },
    cutoutPercentage: 80,
  }
};

var myPieChart = new Chart(ctxPie, pieChartConfig);

$( function() {
    var foundObjects = {};
    var previous = null;
    setInterval(function() {
        $.get( "objects.txt?" + "q=" + (new Date()).getTime(), function( data ) {
            if( data !== previous && data.length > 0) {
                var objects = data.split(',');
                objects.forEach(function(foundItem) {
                    if (foundItem in foundObjects)
                        foundObjects[foundItem]++;
                    else
                        foundObjects[foundItem] = 1;
                });
                
                var distinctObjectCount = Object.keys(foundObjects).length; 
                
                var labels = [];
                var counts = [];
                
                if(distinctObjectCount > 5) {
                    // sort and only use 5 most common objects

                    var sortedKeys = Object.keys(foundObjects).sort(function(a,b){ 
                        return foundObjects[a] - foundObjects[b]
                    }).reverse();

                    labels = sortedKeys.slice(0, 5);

                    for (var i = 0; i < 5; i++) {
                      counts.push(foundObjects[labels[i]]);
                    }

                } 
                else {
                    labels = Object.keys(foundObjects);
                    counts = Object.values(foundObjects);
                }
                
                myPieChart.data.labels = labels;
                myPieChart.data.datasets[0].data = counts;
                myPieChart.update();
                
                $("#number-of-martians").text(foundObjects["Alien"]);
                $("#distinct-objects").text(distinctObjectCount);
                
                $( "#raw-data" ).prepend( "<p>[" + new Date().toISOString() + "]  " + data + "</p>");
                previous = data;
            }
        });
    }, 1000);
});



