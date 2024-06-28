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
});

document.addEventListener('DOMContentLoaded', function () {
    mostrarProductosCarrito();
});

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