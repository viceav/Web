Highcharts.chart("container", {
  chart: {
    type: "pie",
    backgroundColor: "transparent",
  },
  title: {
    text: "Total de Contactos por Comuna",
    style: {
      color: "white",
    },
  },
  plotOptions: {
    pie: {
      dataLabels: {
        enabled: true,
        style: {
          color: "#ffffff",
        },
      },
    },
  },
  series: [{
    name: "Cantidad",
    colorByPoint: true,
    data: [],
  }],
});

fetch(
  "http://127.0.0.1:5000/contactos-por-comuna",
).then(
  (response) => response.json(),
).then(
  (data) => {
    // Get the chart by ID
    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "container",
    );

    // Update the chart with new data
    chart.update({
      series: [
        {
          data: data,
        },
      ],
    });
  },
).catch((error) => {
  console.error("Error: ", error);
});
