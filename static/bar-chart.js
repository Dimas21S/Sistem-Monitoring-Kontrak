const lokasiCanvas = document.getElementById(
    'lokasiKontrakChart'
);

let lokasiChart = null;

if (lokasiCanvas) {

    const lokasiCtx = lokasiCanvas.getContext('2d');

    lokasiChart = new Chart(lokasiCtx, {

        type: 'bar',

        data: {
            labels: lokasiLabels,
            datasets: [{
                label: 'Jumlah Kontrak',
                data: lokasiCounts,
                borderWidth: 0,
                borderRadius: 6,
                barThickness: 35
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    display: false
                }
            },

            scales: {
                y: {
                    beginAtZero: true,

                    ticks: {
                        precision: 0
                    }
                },

                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}