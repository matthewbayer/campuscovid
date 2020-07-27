var ctxL = document.getElementById("lineChart").getContext('2d');
var schooldata = JSON.parse(document.querySelector('#schooldata').dataset.school);

var july1 = new Date().setFullYear(2020, 6, 1);
var days_since_july1 = Math.round((new Date() - july1) / 86400000);
var data = new Array(days_since_july1 + 1).fill(0);
var date_labels = [];
var start = new Date()
start.setFullYear(2020, 6, 1);
for (i = 0; i < data.length; i++) {
  date_str = new Date(start).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
  date_labels.push(date_str);
  start.setDate(start.getDate() + 1);
}

console.log(data);
console.log(date_labels);

schooldata.Events.forEach(function (obj) {
  var dates = obj.Date.split("/");
  var month = dates[0];
  var day = dates[1];
  var year = dates[2];
  var date = new Date().setFullYear(parseInt(year, 10) + 2000,
    parseInt(month, 10) - 1, // months start at 0
    parseInt(day, 10));
  var days_since_july1 = Math.round((date - july1) / 86400000);
  data[days_since_july1] += obj["New Cases"];
});

var cumsum = 0;
var total_cases = new Array(days_since_july1).fill(0);
for (i = 0; i < data.length; i++) {
  cumsum += data[i];
  total_cases[i] = cumsum;
}

console.log(date_labels);

var myLineChart = new Chart(ctxL, {
  type: 'line',
  data: {
    labels: date_labels,
    datasets: [{
      label: "New Daily Cases",
      data: data,
      backgroundColor: [
        'rgba(105, 0, 132, .2)',
      ],
      borderColor: [
        'rgba(200, 99, 132, .7)',
      ],
      borderWidth: 2
    },
    {
      label: "Total Cases",
      data: total_cases,
      backgroundColor: [
        'rgba(0, 137, 132, .2)',
      ],
      borderColor: [
        'rgba(0, 10, 130, .7)',
      ],
      borderWidth: 2
    }
    ]
  },
  options: {
    responsive: true,
  }
});
/*var myLineChart = new Chart(ctxL, {
  type: 'scatter',

  data: {
    labels: ["1", "2", "3"],
    data: [4, 5, 6],

  },
  options: {
    responsive: true,
  }
});*/
/*  type: 'scatter',
  data: {
    datasets: [{
      labels: ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
      label: "New Cases per day",
      data: data,
      backgroundColor: [
        'rgba(105, 0, 132, .2)',
      ],
      borderColor: [
        'rgba(200, 99, 132, .7)',
      ],
      borderWidth: 2,
      //showLine: true
    }
    ],
    options: {
      responsive: true,
      scales: {
        xAxes: [{
          //type: 'time',
          time: {
            min: Date.parse('2020/07/01 00:00:00'),
            max: Date.parse('2020/08/01 00:00:00'),
            parser: 'YYYY-MM-DD HH:mm:ss'
          },
          //  unit: 'millisecond',
          //  distribution: "linear",
          //  minunit: "day",
          //displayFormats: { month: "MMM YYYY" }
          //},
          ticks: {
            source: "data",
            userCallback: function (value, index, values) {
              console.log(new Date(value).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }));
              return new Date(value).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
              //return new Date(value).toLocaleDateString("DD/MM/YY", { day: "long", month: 'short', year: 'numeric' });
            }
          }
        }]
      }
    }
  }
}
);*/