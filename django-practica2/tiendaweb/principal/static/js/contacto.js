var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-0\-]+\.[a-zA-Z0-9\-\.]+$/;

$(document).ready(function () {
    $("#enviar").click(function () {
        var nombre = $("#nombre").val();
        var apellido = $("#apellido").val();
        var email = $("#email").val();
        var fono = $("#fono").val();
        var mensaje = $("#mensaje").val();

        if (nombre == "") {
            $("#mensajeNombre").fadeIn();
            return false;
        } else {
            $("#mensajeNombre").fadeOut();
        }

        if (apellido == "") {
            $("#mensajeApellido").fadeIn();
            return false;
        } else {
            $("#mensajeApellido").fadeOut();
        }

        if (email == "" || !expr.test(email)) {
            $("#mensajeEmail").fadeIn();
            return false;
        } else {
            $("#mensajeEmail").fadeOut();
        }

        if (fono == "" || !pattern.test(fono)) {
            $("#mensajeFono").fadeIn();
            return false;
        } else {
            $("#mensajeFono").fadeOut();
        }

        if (mensaje == "") {
            $("#mensajeTexto").fadeIn();
            return false;
        } else {
            $("#mensajeTexto").fadeOut();
        }

    });
});