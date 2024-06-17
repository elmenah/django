// Función para obtener un usuario aleatorio
async function getRandomUser() {
    const apiUrl = 'https://randomuser.me/api/';
    try {
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            const user = data.results[0];
            // Construir la representación HTML del usuario
            const userHtml = `
                <div class="user">
                    <img src="${user.picture.large}" alt="Avatar">
                    <p><strong>Nombre:</strong> ${user.name.first} ${user.name.last}</p>
                    <p><strong><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></strong></p>
                    
                </div>
            `;
            // Mostrar los datos del usuario en el contenedor
            document.getElementById('userContainer').innerHTML += userHtml;
        } else {
            console.error('Error al obtener usuario aleatorio:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
// Llama a getRandomUser tres veces para obtener tres usuarios
getRandomUser();
getRandomUser();