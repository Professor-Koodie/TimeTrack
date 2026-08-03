const pieData = JSON.parse('{{ pie_chart_json|escapejs }}');

const ctxPie = document.getElementById('pieChart').getContext('2d');
new Chart(ctxPie, {
    type: 'pie',
    data: pieData,
    options: { responsive: true }
});

function openPieFullscreen() {
    const modal = new bootstrap.Modal(document.getElementById('pieModal'));
    modal.show();

    const ctxPieFull = document.getElementById('pieChartFullscreen').getContext('2d');
    new Chart(ctxPieFull, {
        type: 'pie',
        data: pieData,
        options: { responsive: true }
    });
}
