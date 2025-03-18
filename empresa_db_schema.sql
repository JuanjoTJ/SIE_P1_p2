-- Crear la tabla empleados
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,  -- SERIAL es equivalente a AUTOINCREMENT en PostgreSQL
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    fecha_nacimiento TEXT NOT NULL,
    salario REAL NOT NULL
);

-- Crear la tabla clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,  -- SERIAL es equivalente a AUTOINCREMENT en PostgreSQL
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    fecha_nacimiento TEXT NOT NULL,
    empleado_id INTEGER,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
);