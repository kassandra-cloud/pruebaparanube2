document.getElementById('grupos').addEventListener('change', function () {
    const grupoId = this.value; // Obtiene el ID del grupo seleccionado
    const permisosDiv = document.getElementById('permisos-grupo');
    const listaPermisos = document.getElementById('lista-permisos');
    const verMasBtn = document.getElementById('ver-mas');

    // Limpiar la lista de permisos antes de agregar nuevos
    listaPermisos.innerHTML = '';
    verMasBtn.style.display = 'none'; // Ocultar el botón "Ver más" inicialmente

    if (grupoId) {
        // Hacer la solicitud AJAX para obtener los permisos del grupo
        fetch(`/api/permisos-grupo/${grupoId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    permisosDiv.style.display = 'block'; // Mostrar el contenedor de permisos
                    const permisos = data.permisos;
                    const maxPermisos = 1; // Número máximo de permisos visibles inicialmente

                    // Mostrar solo los primeros 4 permisos
                    permisos.slice(0, maxPermisos).forEach(permiso => {
                        const li = document.createElement('li');
                        li.textContent = permiso.name; // Mostrar el nombre del permiso
                        li.className = 'list-group-item';
                        listaPermisos.appendChild(li);
                    });

                    // Mostrar el botón "Ver más" si hay más de 4 permisos
                    if (permisos.length > maxPermisos) {
                        verMasBtn.style.display = 'inline';
                        verMasBtn.onclick = () => {
                            // Mostrar todos los permisos
                            listaPermisos.innerHTML = '';
                            permisos.forEach(permiso => {
                                const li = document.createElement('li');
                                li.textContent = permiso.name;
                                li.className = 'list-group-item';
                                listaPermisos.appendChild(li);
                            });
                            verMasBtn.style.display = 'none'; // Ocultar el botón "Ver más"
                        };
                    }
                } else {
                    permisosDiv.style.display = 'none';
                    alert(data.error || 'Error al obtener permisos.');
                }
            })
            .catch(error => {
                permisosDiv.style.display = 'none';
                console.error('Error al obtener permisos:', error);
            });
    } else {
        permisosDiv.style.display = 'none'; // Ocultar el contenedor si no se selecciona un grupo
    }
});
document.getElementById('grupos').addEventListener('change', function () {
    const grupoId = this.value; // Obtiene el ID del grupo seleccionado
    const permisosDiv = document.getElementById('permisos-grupo');
    const listaPermisos = document.getElementById('lista-permisos');
    const verMasBtn = document.getElementById('ver-mas');

    // Limpiar la lista de permisos antes de agregar nuevos
    listaPermisos.innerHTML = '';
    verMasBtn.style.display = 'none'; // Ocultar el botón "Ver más" inicialmente

    if (grupoId) {
        // Hacer la solicitud AJAX para obtener los permisos del grupo
        fetch(`/api/permisos-grupo/${grupoId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    permisosDiv.style.display = 'block'; // Mostrar el contenedor de permisos
                    const permisos = data.permisos;
                    const maxPermisos = 4; // Número máximo de permisos visibles inicialmente

                    // Mostrar solo los primeros 4 permisos
                    permisos.slice(0, maxPermisos).forEach(permiso => {
                        const li = document.createElement('li');
                        li.textContent = permiso.name; // Mostrar el nombre del permiso
                        li.className = 'list-group-item';
                        listaPermisos.appendChild(li);
                    });

                    // Mostrar el botón "Ver más" si hay más de 4 permisos
                    if (permisos.length > maxPermisos) {
                        verMasBtn.style.display = 'inline';
                        verMasBtn.onclick = () => {
                            // Mostrar todos los permisos
                            listaPermisos.innerHTML = '';
                            permisos.forEach(permiso => {
                                const li = document.createElement('li');
                                li.textContent = permiso.name;
                                li.className = 'list-group-item';
                                listaPermisos.appendChild(li);
                            });
                            verMasBtn.style.display = 'none'; // Ocultar el botón "Ver más"
                        };
                    }
                } else {
                    permisosDiv.style.display = 'none';
                    alert(data.error || 'Error al obtener permisos.');
                }
            })
            .catch(error => {
                permisosDiv.style.display = 'none';
                console.error('Error al obtener permisos:', error);
            });
    } else {
        permisosDiv.style.display = 'none'; // Ocultar el contenedor si no se selecciona un grupo
    }
});

function generarPassword() {
    fetch("/generar_password/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('password').value = data.password;
    })
    .catch(error => console.error('Error:', error));
}
