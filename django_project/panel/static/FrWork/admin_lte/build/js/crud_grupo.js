function toggleAllPermissions(selectAllCheckbox) {
    // Obtener todos los checkboxes de permisos
    const checkboxes = document.querySelectorAll('.permiso-checkbox');
    
    // Establecer todos los checkboxes como seleccionados o deseleccionados dependiendo del estado de "Seleccionar todo"
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = selectAllCheckbox.checked;
    });
}

function toggleAllPermissions(selectAllCheckbox) {
    const checkboxes = document.querySelectorAll('.permiso-checkbox');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = selectAllCheckbox.checked;
    });
}
