from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="empresa",
        user="postgres",
        password="abcd"
    )
    return conn

# Endpoint para listar empleados y clientes
@app.route('/listar', methods=['GET'])
def listar():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener empleados
    cursor.execute('SELECT * FROM empleados')
    empleados = cursor.fetchall()

    # Obtener clientes
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    # Convertir resultados a formato JSON
    return jsonify({
        'empleados': empleados,
        'clientes': clientes
    })

# Endpoint para modificar el salario de un empleado
@app.route('/modificar_salario/<int:id>', methods=['PUT'])
def modificar_salario(id):
    datos = request.json
    nuevo_salario = datos.get('salario')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Modificar salario
    cursor.execute("""
        UPDATE empleados SET salario = %s WHERE id = %s
    """, (nuevo_salario, id))

    # Guardar cambios y cerrar conexión
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Salario actualizado correctamente'})

# Endpoint para modificar el empleado que gestiona a un cliente
@app.route('/modificar_empleado_cliente/<int:id>', methods=['PUT'])
def modificar_empleado_cliente(id):
    datos = request.json
    nuevo_empleado_id = datos.get('empleado_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Modificar empleado que gestiona al cliente
    cursor.execute("""
        UPDATE clientes SET empleado_id = %s WHERE id = %s
    """, (nuevo_empleado_id, id))

    # Guardar cambios y cerrar conexión
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Empleado asignado correctamente'})

# Endpoint para insertar un empleado o un cliente
@app.route('/insertar', methods=['POST'])
def insertar():
    datos = request.json
    tipo = datos.get('tipo')  # 'empleado' o 'cliente'
    conn = get_db_connection()
    cursor = conn.cursor()

    if tipo == 'empleado':
        cursor.execute("""
            INSERT INTO empleados (nombre, apellidos, dni, fecha_nacimiento, salario)
            VALUES (%s, %s, %s, %s, %s)
        """, (datos['nombre'], datos['apellidos'], datos['dni'], datos['fecha_nacimiento'], datos['salario']))
    elif tipo == 'cliente':
        cursor.execute("""
            INSERT INTO clientes (nombre, apellidos, dni, fecha_nacimiento, empleado_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (datos['nombre'], datos['apellidos'], datos['dni'], datos['fecha_nacimiento'], datos['empleado_id']))

    # Guardar cambios y cerrar conexión
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Registro insertado correctamente'})

# Endpoint para eliminar un empleado o un cliente
@app.route('/eliminar/<tipo>/<int:id>', methods=['DELETE'])
def eliminar(tipo, id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if tipo == 'empleado':
        cursor.execute("DELETE FROM empleados WHERE id = %s", (id,))
    elif tipo == 'cliente':
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))

    # Guardar cambios y cerrar conexión
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Registro eliminado correctamente'})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)