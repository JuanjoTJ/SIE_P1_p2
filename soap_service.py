from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import psycopg2

# Función para conectar a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="empresa",
        user="postgres",
        password="ajedrez1"
    )
    return conn

class EmpresaService(ServiceBase):
    @rpc(_returns=Unicode)
    def listar(ctx):
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

        # Convertir resultados a cadena
        return f"Empleados: {empleados}\nClientes: {clientes}"

    @rpc(Integer, Float, _returns=Unicode)
    def modificar_salario(ctx, id, nuevo_salario):
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

        return "Salario actualizado correctamente"

    @rpc(Integer, Integer, _returns=Unicode)
    def modificar_empleado_cliente(ctx, id, nuevo_empleado_id):
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

        return "Empleado asignado correctamente"

    @rpc(Unicode, Unicode, Unicode, Unicode, Float, _returns=Unicode)
    def insertar_empleado(ctx, nombre, apellidos, dni, fecha_nacimiento, salario):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar empleado
        cursor.execute("""
            INSERT INTO empleados (nombre, apellidos, dni, fecha_nacimiento, salario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, dni, fecha_nacimiento, salario))

        # Guardar cambios y cerrar conexión
        conn.commit()
        cursor.close()
        conn.close()

        return "Empleado insertado correctamente"

    @rpc(Unicode, Unicode, Unicode, Unicode, Integer, _returns=Unicode)
    def insertar_cliente(ctx, nombre, apellidos, dni, fecha_nacimiento, empleado_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar cliente
        cursor.execute("""
            INSERT INTO clientes (nombre, apellidos, dni, fecha_nacimiento, empleado_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, dni, fecha_nacimiento, empleado_id))

        # Guardar cambios y cerrar conexión
        conn.commit()
        cursor.close()
        conn.close()

        return "Cliente insertado correctamente"

    @rpc(Unicode, Integer, _returns=Unicode)
    def eliminar(ctx, tipo, id):
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

        return "Registro eliminado correctamente"

# Configurar la aplicación SOAP
application = Application([EmpresaService], 'empresa.soap',
                         in_protocol=Soap11(validator='lxml'),
                         out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

# Ejecutar el servidor SOAP
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()