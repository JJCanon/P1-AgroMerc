import csv
import os

def generar_html():
    # Obtén la ruta absoluta del archivo CSV
    csv_path = os.path.join(os.path.dirname(__file__), 'public', 'data', 'personas.csv')
    
    html_content = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AgroMerc Personas</title>
        <link rel="stylesheet" href="../public/styles/global.css">
    </head>
    <body>
        <header>
            <div class="logo">
                <img src="../public/img/AgroMerc.jpg" alt="AgroMerc Logo">
                <h1>AgroMerc</h1>
            </div>
            <nav>
                <a href="/home">Home</a>
                <a href="/about">About</a>
            </nav>
        </header>

        <main>
            <h2>Buscar Persona:</h2>
            <div class="search-bar">
                <label for="search">Buscar Persona:</label>
                <input type="text" id="search" placeholder="Escribe un nombre...">
                <label for="category">Categoría:</label>
                <select id="category">
                    <option value="todos">Todos</option>
                    <option value="proveedores">Proveedores</option>
                    <option value="clientes">Clientes</option>
                </select>
                <button>Buscar</button>
            </div>

            <section class="person-grid">
    '''

    # Leer los datos desde el CSV
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
          print(row)  # Esto imprimirá cada fila como un diccionario para depuración
          html_content += f'''
           <div class="person-card">
            <img src="../public/img/{row['imagen']}" alt="Foto de {row['nombre']}">
            <h3>{row['nombre']}</h3>
            <p style="color: #333;">Compras Realizadas: {row['compras']}</p>
            <p style="color: #333;">Proveedores Utilizados: {row['proveedores']}</p>
            <p style="color: #333;">Registrado desde: {row['registro']}</p>
        </div>
        '''

    html_content += '''
            </section>
        </main>
    </body>
    </html>
    '''

    with open('../templates/home.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generar_html()
