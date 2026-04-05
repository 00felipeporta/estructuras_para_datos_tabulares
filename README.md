Custom DataFrame
Este proyecto es una implementación propia de estructuras de datos para manipular tablas en Python. No utiliza librerías externas, todo el comportamiento de las clases Series y DataFrame está construido desde cero utilizando la biblioteca estándar.

Está pensado para demostrar cómo gestionar tipos de datos, validaciones de longitud y operaciones de filtrado u ordenamiento manteniendo la integridad de las filas.

Funcionamiento técnico:

La clase Series:
Es la unidad básica. Maneja una lista de datos de un tipo específico (int, float, str o bool).

Soporta valores nulos (None) sin romper las operaciones.

Implementa métodos mágicos para que las series sean iterables y se puedan consultar por índice.

Incluye operaciones aritméticas vectorizadas y métodos de agregación.

La clase DataFrame:
Es un contenedor de objetos Series. Su principal responsabilidad es garantizar que todas las columnas tengan la misma altura y que las operaciones afecten a toda la fila por igual.

Acceso: Se puede acceder a las columnas como si fuera un diccionario.

Filtrado: Permite pasar funciones lambda para filtrar filas según condiciones específicas.

Ordenamiento: Al ordenar por una columna, el resto de las columnas se reordenan automáticamente para no perder la relación de los datos.

Visualización: El método __repr__ genera una tabla con bordes en la terminal. Si los datos son muchos, la tabla se corta automáticamente para mostrar solo el principio y el final.
