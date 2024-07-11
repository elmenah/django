document.addEventListener('DOMContentLoaded', function () {
    const botonesComprar = document.querySelectorAll('.btn-comprar');

    botonesComprar.forEach(boton => {
        boton.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const nombre = this.getAttribute('data-nombre');
            const precio = this.getAttribute('data-precio');
            const cantidad = document.querySelector('#cantidad' + id).value;

            const producto = {
                id: id,
                nombre: nombre,
                precio: precio,
                cantidad: cantidad
            };

            let productosComprados = JSON.parse(localStorage.getItem('productosComprados')) || [];

            // Añadir el producto a la lista
            productosComprados.push(producto);

            // Guardar la lista actualizada en local storage
            localStorage.setItem('productosComprados', JSON.stringify(productosComprados));

            alert('Producto agregado al carrito');
        });
    });

    mostrarProductosCarrito();
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.btn-primary').addEventListener('click', function () {
        const productosComprados = JSON.parse(localStorage.getItem('productosComprados')) || [];

        fetch('/actualizar_stock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Obtener el token CSRF
            },
            body: JSON.stringify({ productos: productosComprados })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pago realizado con éxito');
                
                // Mostrar el botón "Imprimir Boleta" después del pago
                mostrarBotonBoleta(productosComprados);
            } else {
                alert(data.message);
            }
        });
    });

    mostrarProductosCarrito();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function mostrarProductosCarrito() {
    const listaProductos = JSON.parse(localStorage.getItem('productosComprados')) || [];

    const listaProductosHTML = listaProductos.map(producto => `
        <div class="producto">
            <h4>${producto.nombre}</h4>
            <p>Precio: $${parseFloat(producto.precio).toFixed(0)}</p>
            <p>Cantidad: ${producto.cantidad}</p>
        </div>
    `).join('');

    document.getElementById('lista-productos').innerHTML = listaProductosHTML;
    mostrarResumenCarrito(listaProductos);
}

function mostrarResumenCarrito(productos) {
    let totalProductos = 0;
    let totalCarrito = 0;

    productos.forEach(producto => {
        totalProductos += parseInt(producto.cantidad);
        totalCarrito += parseInt(producto.cantidad) * parseFloat(producto.precio);
    });

    const resumenHTML = `
        <h4>Resumen del Carrito</h4>
        <p>Total de Productos: ${totalProductos}</p>
        <p>Total del Carrito: $${totalCarrito.toFixed(0)}</p>
    `;

    document.getElementById('resumen-carrito').innerHTML = resumenHTML;
}

function vaciarCarrito() {
    localStorage.removeItem('productosComprados');
    document.getElementById('lista-productos').innerHTML = '<p class="producto">El carrito está vacío.</p>';
    document.getElementById('resumen-carrito').innerHTML = `
        <h4>Resumen del Carrito</h4>
        <p>Total de Productos: 0</p>
        <p>Total del Carrito: $0</p>
    `;
}

function mostrarBotonBoleta(productosComprados) {
    const botonBoleta = document.createElement('button');
    botonBoleta.className = 'btn btn-secondary mt-3';
    botonBoleta.innerText = 'Imprimir Boleta';
    botonBoleta.id = 'botonboleta';
    botonBoleta.addEventListener('click', function () {
        const productosHTML = generarProductosHTML(productosComprados);
        generarBoleta(productosHTML);
        
        // Vaciar el carrito después de generar la boleta
        vaciarCarrito();
    });

    document.querySelector('.card-body').appendChild(botonBoleta);
}

function generarProductosHTML(productos) {
    const productosAgrupados = {};

    productos.forEach(producto => {
        const nombre = producto.nombre;
        const cantidad = parseInt(producto.cantidad);

        if (productosAgrupados[nombre]) {
            productosAgrupados[nombre].cantidad += cantidad;
        } else {
            productosAgrupados[nombre] = { ...producto, cantidad };
        }
    });

    let total = 0;

    Object.values(productosAgrupados).forEach(producto => {
        const precioNumerico = parseFloat(producto.precio.replace(/[^\d.]/g, ''));
        const totalProducto = precioNumerico * producto.cantidad;
        total += totalProducto;
    });

    const plantillaHTML = `
<!doctype html>
<html>

<head>
    <meta charset="utf-8">

    <style>
        .invoice-box {
            max-width: 800px;
            padding: 30px;
            border: 1px solid #eee;
            box-shadow: 0 0 10px rgba(0, 0, 0, .15);
            font-size: 16px;
            line-height: 24px;
            font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
            color: #555;
        }

        .invoice-box table {
            width: 100%;
            line-height: inherit;
            text-align: left;
        }

        .invoice-box table td {
            padding: 5px;
            vertical-align: top;
        }

        .invoice-box table tr td:nth-child(2) {
            text-align: right;
        }

        .invoice-box table tr.top table td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.top table td.title {
            font-size: 45px;
            line-height: 45px;
            color: #333;
        }

        .invoice-box table tr.information table td {
            padding-bottom: 40px;
        }

        .invoice-box table tr.heading td {
            background: #eee;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }

        .invoice-box table tr.details td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.item td {
            border-bottom: 1px solid #eee;
        }

        .invoice-box table tr.item.last td {
            border-bottom: none;
        }

        .invoice-box table tr.total td:nth-child(2) {
            border-top: 2px solid #eee;
            font-weight: bold;
        }

        @media only screen and (max-width: 600px) {
            .invoice-box table tr.top table td {
                width: 100%;
                display: block;
                text-align: center;
            }

            .invoice-box table tr.information table td {
                width: 100%;
                display: block;
                text-align: center;
            }
        }

        .rtl {
            direction: rtl;
            font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        }

        .rtl table {
            text-align: right;
        }

        .rtl table tr td:nth-child(2) {
            text-align: left;
        }
    </style>
</head>

<body>
    <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">
            <tr class="top">
                <td colspan="2">
                    <table>
                        <tr>
                            <td class="title">
                                <img src="Imagenes/logo terraza.png" style="width:100%; max-width:200px;">
                            </td>
                            <td>
                                <br>
                                Nro Pedido #: 123<br>
                                Fecha: ${new Date().toLocaleDateString()}<br>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>

            <tr class="information">
                <td colspan="2">
                    <table>
                        <tr>
                            <td>
                                Direccion: <br>
                                2540 Av. Carlos Alessandri, <br>
                                Algarrobo, Valparaiso
                            </td>

                            <td>
                                Contacto:<br>
                                John Doe<br>
                                info@laterraza.cl
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>

            <tr class="heading">
                <td>
                    Metodo de Pago
                </td>

                <td>
                    Check #
                </td>
            </tr>

            <tr class="details">
                <td>
                    Efectivo
                </td>
                <td>
                    1000
                </td>
            </tr>

            <tr class="heading">
                <td>
                    Producto
                </td>

                <td>
                    Precio
                </td>
            </tr>

            ${Object.values(productosAgrupados).map(producto => `
                <tr class="item">
                    <td>${producto.nombre} (${producto.cantidad})</td>
                    <td>$${(parseFloat(producto.precio.replace(/[^\d.]/g, '')) * producto.cantidad).toFixed(0)}</td>
                </tr>
            `).join('')}

            <tr class="total">
                <td></td>
                <td>
                   Total: $${total.toFixed(0)}
                </td>
            </tr>
        </table>
    </div>
</body>

</html>
`;

    return plantillaHTML;
}

// Función para generar la boleta utilizando la API de YakPDF
async function generarBoleta(productosHTML) {
    const url = "https://yakpdf.p.rapidapi.com/pdf";

    const options = {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "X-RapidAPI-Key": "d458b48b79msha5e0ed9c2e730c8p156c8djsn7aea9ce631bb",
            "X-RapidAPI-Host": "yakpdf.p.rapidapi.com",
        },
        body: JSON.stringify({
            source: {
                html: productosHTML,
            },
            pdf: {
                format: "A4",
                scale: 1,
                printBackground: true,
            },
            wait: {
                for: "navigation",
                waitUntil: "load",
                timeout: 2500,
            },
        }),
    };

    try {
        const response = await fetch(url, options);
        const blob = await response.blob();
        const pdfUrl = URL.createObjectURL(blob);
        window.open(pdfUrl, "_blank");
    } catch (error) {
        console.error(error);
    }
}
