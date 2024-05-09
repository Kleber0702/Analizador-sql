from flask import Flask, request, render_template
import mysql.connector
from lexer import lexer  # Importa el objeto lexer

app = Flask(__name__)

# Configuración de la conexión a MySQL
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = ''

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar las solicitudes de análisis de código
@app.route('/analizar', methods=['POST'])
def analizar_codigo():
    codigo = request.form.get('codigo')

    # Análisis léxico
    lexer.input(codigo)
    tokens = []
    errores = []  # Lista para almacenar mensajes de error léxico

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == 'PALABRA_RESERVADA_MAL_ESCRITA':
            errores.append(f"Error léxico: Palabra reservada mal escrita '{tok.value}' en la línea {lexer.lineno}")
        if tok.type == 'IDENTIFICADOR_ERRONEO':
            errores.append(f"Error léxico: El identificador no puede comenzar con un numero '{tok.value}' en la línea {lexer.lineno}")
        tokens.append((tok.type, tok.value))

    # Si hay errores léxicos, mostrarlos y no ejecutar la consulta SQL
    if errores:
        return render_template('index.html', tokens=tokens, mensaje="Consulta no ejecutada", errores=errores)

    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database='stockdb'  # Especifica la base de datos por defecto aquí
        )

        cursor = connection.cursor()

        # Dividir los comandos SQL por punto y coma
        comandos = codigo.split(';')

        for comando in comandos:
            if comando.strip():  # Ignorar comandos vacíos
                cursor.execute(comando)
                connection.commit()  # Confirmar los cambios en la base de datos

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        print("Consultas SQL generadas y ejecutadas con éxito:", comandos)
        return render_template('index.html', tokens=tokens, mensaje="Consultas ejecutadas con éxito")

    except mysql.connector.Error as error:
        # Si hay algún error al ejecutar la consulta, mostrar el error
        mensaje = f"Error al ejecutar la consulta SQL: {error}"
        return render_template('resultado.html', tokens=tokens, mensaje=mensaje)


if __name__ == '__main__':
    app.run(debug=True)
