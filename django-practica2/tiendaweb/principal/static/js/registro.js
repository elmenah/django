

    
function calcularEdad(fechaNacimiento) {
    var hoy = new Date();
    var fechaNac = new Date(fechaNacimiento);
    var edad = hoy.getFullYear() - fechaNac.getFullYear();
    var mes = hoy.getMonth() - fechaNac.getMonth();

    if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
        edad--;
    }

    return edad;
}

function registrarCuenta() {
    
    var usuario = document.getElementById("usuario").value;
    var email = document.getElementById("correo").value;
    var fechaNacimiento = document.getElementById("fecha").value;
    var contraseña = document.getElementById("exampleInputPassword1").value;
    var repetirContraseña = document.getElementById("exampleInputPassword2").value;

    // Valida que se ingresen todos los campos
    if ( !usuario || !email || !fechaNacimiento || !contraseña || !repetirContraseña) {
        alert("Por favor, completa todos los campos.");
        return false;
    }

    // Esto Valida la edad mínima (18 años en este ejemplo)
    var edad = calcularEdad(fechaNacimiento);
    if (edad < 18) {
        alert("Debes tener al menos 18 años para registrarte.");
        return false;
    }

    // Valida el correo electrónico
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Por favor, ingresa un correo electrónico válido.");
        return false;
    }

    // Valida la longitud de la contraseña
    if (contraseña.length < 8) {
        alert("La contraseña debe tener al menos 8 caracteres.");
        return false;
    }

    // Esto Valida que las contraseñas coincidan
    if (contraseña !== repetirContraseña) {
        alert("Las contraseñas no coinciden.");
        return false;
    }

    
    }

    
