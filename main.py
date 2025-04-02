# Importar las clases principales del framework Flask
from flask import Flask, render_template, request, redirect

# Importar módulos para trabajar con variables de entorno del archivo .env
import os
from dotenv import load_dotenv

# Importar clase para capturar errores HTTP estándar (por ejemplo: 404, 405)
from werkzeug.exceptions import HTTPException

# Importar clases propias del proyecto (modelo y controlador)
from modelo.Entidad import Entidad
from control.ControlEntidad import ControlEntidad

# Importar blueprints que agrupan rutas específicas de cada módulo
from vista.vistaRol import vistaRol 
from vista.home import home 

# Cargar el archivo .env y permitir que sobrescriba las variables del sistema si ya existen
# Esto es necesario cuando PowerShell o el entorno virtual ya tienen variables cargadas previamente
load_dotenv(override=True)

# Verificar en consola los valores cargados desde el archivo .env
# Esto ayuda a confirmar que se están leyendo correctamente y que no hay valores antiguos en memoria
print("Verificación de variables cargadas desde .env:")
print("SERV:", os.getenv("SERV"))
print("USUA:", os.getenv("USUA"))
print("PASSW:", os.getenv("PASSW"))
print("BDAT:", os.getenv("BDAT"))
print("PORT:", os.getenv("PORT"))

# Crear la aplicación Flask
app = Flask(__name__)

# Definir una clave secreta para la gestión de sesiones
# Se obtiene del archivo .env o se usa una por defecto si no se encuentra
app.secret_key = os.getenv("SECRET_KEY", "clave_insegura")

# Registrar los módulos de rutas que se han definido como blueprints
app.register_blueprint(vistaRol)
app.register_blueprint(home)

# Definir la ruta principal de la aplicación ('/') y una ruta alternativa ('/inicio')
@app.route('/', methods=['GET', 'POST'])
@app.route('/inicio', methods=['GET', 'POST']) 
def inicio():
    # Inicializar variables del formulario
    correo = ""
    contrasena = ""
    mensaje_bot = ""
    
    # Verificar si se está enviando el formulario (método POST)
    if request.method == 'POST':
        # Mostrar la página de inicio pasando el correo como parámetro
        return render_template('home.html', ema=correo)
    
    # En caso de ser un acceso normal (GET), también se muestra la misma plantilla
    return render_template('home.html', ema=correo)

# Definir la ruta para cerrar sesión. Redirige nuevamente al inicio
@app.route('/cerrarSesion')
def cerrarSesion():
    return redirect('inicio')

# Manejar errores HTTP comunes como 404 (no encontrado), 405 (método no permitido), etc.
@app.errorhandler(HTTPException)
def manejar_errores_http(error):
    # Crear un mensaje personalizado con los detalles del error HTTP
    mensaje = f"Error HTTP {error.code}: {error.name} - {error.description}"
    
    # Mostrar el mensaje en consola (útil para el programador)
    print(mensaje)
    
    # Retornar el mensaje como texto plano y el código de estado correspondiente
    return mensaje, error.code

# Manejar cualquier otro tipo de error no previsto (errores en código, lógica, etc.)
@app.errorhandler(Exception)
def manejar_excepcion_general(error):
    # Crear un mensaje personalizado con la descripción del error inesperado
    mensaje = f"Error inesperado: {str(error)}"
    
    # Mostrar el mensaje en consola para facilitar la depuración
    print(mensaje)
    
    # Retornar el mensaje como texto plano y el código de error interno del servidor
    return mensaje, 500

# Ejecutar la aplicación solo si este archivo se ejecuta directamente
if __name__ == '__main__':
    # Leer la variable FLASK_DEBUG del entorno y convertirla a booleano
    # Si no está definida, se asume que es false (modo producción)
    modo_debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    
    # Leer el puerto desde el entorno si está definido, o usar el puerto 5000 por defecto
    puerto = int(os.getenv("FLASK_RUN_PORT", 5000))

    # Iniciar el servidor en el puerto especificado y con el modo debug según configuración
    # En modo producción, FLASK_DEBUG debe estar en false y se recomienda usar un servidor WSGI (como gunicorn o waitress)
    app.run(debug=modo_debug, port=puerto)
