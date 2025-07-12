document.getElementById("rut_numeros").addEventListener("input", function () {
    const rutNumeros = this.value.replace(/\./g, "").replace(/\s/g, ""); // Eliminar puntos y espacios
    const rutDV = document.getElementById("rut_dv");

    if (!rutNumeros || isNaN(rutNumeros)) {
        rutDV.value = ""; // Limpiar el DV si no hay RUT válido
        return;
    }

    let suma = 0;
    let multiplicador = 2;

    for (let i = rutNumeros.length - 1; i >= 0; i--) {
        suma += parseInt(rutNumeros[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const resto = suma % 11;
    const dv = 11 - resto;

    rutDV.value = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();
});
