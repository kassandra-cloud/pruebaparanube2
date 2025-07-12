   // Datos ficticios
   const performanceData = {
    labels: ['Hace 5 min', 'Hace 4 min', 'Hace 3 min', 'Hace 2 min', 'Hace 1 min', 'Ahora'],
    datasets: [{
        label: 'Tiempo de Respuesta (ms)',
        data: [150, 140, 130, 120, 115, 110],
        borderColor: '#007bff',
        backgroundColor: 'rgba(0, 123, 255, 0.2)',
        tension: 0.4
    }]
};

// Configuración de la gráfica
const config = {
    type: 'line',
    data: performanceData,
    options: {
        responsive: true,
        plugins: {
            legend: { display: true },
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
};

// Renderizar la gráfica
const ctx = document.getElementById('performanceChart').getContext('2d');
new Chart(ctx, config);

// Simulación de actualización de métricas
function actualizarMetricas() {
    $('#response-time').text(`${Math.floor(Math.random() * 50) + 100}ms`);
    $('#processing-speed').text(`${Math.floor(Math.random() * 5) + 10} imágenes/s`);
    $('#uptime').text(`${(99 + Math.random()).toFixed(2)}%`);
}

setInterval(actualizarMetricas, 5000); // Actualiza cada 5 segundos

function actualizarTabla() {
    $.get('/api/flujo-pacientes/', function (data) {
        const pacientes = data.pacientes;
        const tableBody = $("#pacientes-table");
        tableBody.empty();

        pacientes.forEach(paciente => {
            const row = `
                <tr>
                    <td>${paciente.nombre}</td>
                    <td>${paciente.apellido}</td>
                    <td>${paciente.edad}</td>
                    <td>${paciente.estado}</td>
                    <td>${paciente.tiempo_ingreso}</td>
                    <td>${paciente.tiempo_actualizacion}</td>
                </tr>
            `;
            tableBody.append(row);
        });
    });
}

setInterval(actualizarTabla, 5000); // Actualiza cada 5 segundos
actualizarTabla(); // Carga inicial