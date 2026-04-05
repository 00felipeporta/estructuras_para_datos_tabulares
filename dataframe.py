from series import Series

# Estructura bidimensional de datos, organizada en filas y columnas.
class DataFrame:
    #########################################################################
    #                               INICIALIZACION                          #
    #########################################################################
    def __init__(self, data):
        
        # Inicializamos self._data como diccionario vacio
        self._data = {}                        

        #----------------------- Si data es un diccionario --------------------------------#
        if isinstance(data, dict):            
            # Verificamos que no haya nombres repetidos
            if len(data.keys()) != len(set(data.keys())): # 
                raise ValueError("Los nombres de las columnas no pueden repetirse.")
            
            # Iteramos por data.items()
            for nombre_col, valor in data.items():

                #------------------ Si los valores son Series -------------------------------- #
                if isinstance(valor, Series): 
                    
                    # Copiamos la serie original para no modificarla ni que haya problemas si es modificada
                    copia = valor.clone()
                    copia.rename(nombre_col) # La renombramos
                    self._data[nombre_col] = copia # Guardamos en self._data los valores con su nombre
                
                # -----------------Si los valores son list------------------------------------ #
                elif isinstance(valor, list):
                    self._data[nombre_col] = Series(valor, name = nombre_col) # Convertimos a Series
                else:
                    raise TypeError("Los valores del diccionario tienen que ser listas o instancias de Series")
        
        # --------------------- Si data es list --------------------------------------------#
        
        elif isinstance(data, list):
            # Si son todas series
            if all(isinstance(x, Series) for x in data):
                # Armamos una lista con nombres
                nombres = [x.name for x in data]
                if len(nombres) != len(set(nombres)):
                    raise ValueError("Los nombres de las Series no pueden repetirse.")

                for x in data:
                    # Copiamos la serie original para no modificarla ni que haya problemas si es modificada
                    self._data[x.name] = x.clone()                
            else:
                raise TypeError("Los elementos de la lista tienen que ser ser Series")    
        
        else:
            raise TypeError("data tiene que ser list o dict")

        # En todos los casos, verificamos que todas las columnas tengan la misma longitud
        longitudes = [len(s) for s in self._data.values()] # Armamos una lista con todas las longitudes

        if len(set(longitudes)) != 1: # Cuando le aplicamos set deberia quedar un solo numero (Series no admite listas vacias)
            raise ValueError("Todas las columnas tienen que tener la misma longitud.")

    ###############################################################
    #                     ATRIBUTOS                               #
    ###############################################################
    
    # Lista con los nombres de las columnas, en orden
    @property 
    def columns(self):
        return list(self._data.keys())

    # Lista con los dtypes de las columnas, en orden 
    @property
    def dtypes(self):
        lista_dtypes = [s.dtype for s in self._data.values()]
        return lista_dtypes

    # Cantidad de filas
    @property
    def height(self):
        # Devuelve la cantidad de filas tomando de referencia la longitud de la primera columna que encontremos      
        columna = list(self._data.keys())[0]
        return len(self._data[columna])

    # Cantidad de columnas
    @property
    def width(self):
        return len(self._data)    
    
    # Dimensión de la tabla (filas, columnas)
    @property
    def shape(self):
        return (self.height, self.width)

    # Diccionario que mapea las columnas a sus tipos
    @property
    def schema(self):
        tipos_columna = {}
        for clave, valor in self._data.items():
            tipos_columna[clave] = valor.dtype
        return tipos_columna
    
    ######################################################################
    #                            METODOS                                 #
    ######################################################################
    # Devuelve un nuevo DataFrame con las primeras n filas.
    def head(self, n=5):      
        # Inicializamos un dict vacio  
        primeras_filas = {}

        for nombre, serie in self._data.items():
            # Hacemos uso del metodo head() de Series
            primeras_filas[nombre] = serie.head(n)
        return DataFrame(primeras_filas)

    # Devuelve un nuevo DataFrame con las últimas n filas.
    def tail(self, n=5):
        # Inicializamos un dict vacio  
        ultimas_filas = {}

        for nombre, serie in self._data.items():
            # Hacemos uso del metodo tail() de Series
            ultimas_filas[nombre] = serie.tail(n)
        return DataFrame(ultimas_filas)

    # Devuelve un nuevo DataFrame con solo las columnas indicadas.
    def select(self, *columns):
        # Inicializamos un dict vacio
        nuevas_columnas = {}
        for columna in columns:
            # Validamos que la columna exista
            if columna not in self._data:
                raise KeyError(f"La columna '{columna}' no existe.")
            nuevas_columnas[columna] = self._data[columna]
        return DataFrame(nuevas_columnas)
        
        
    # Devuelve un DataFrame con las filas que cumplen todas las condiciones.
    # predicates es una tupla de tuplas (columna, f)
    def filter(self, *predicates):
    # Si no hay predicados, devolvemos el DataFrame completo
        if not predicates:
            return self

        # Guardamos los indices de las filas que cumplen la condicion
        filas_validas = []
                
        # Evaluamos todas las filas
        for i in range(self.height):
            # Inicializamos cumple_todo como True
            cumple_todo = True
            # Nos fijamos en cada columna si hay alguna fila que no cumpla
            for (columna, f) in predicates:
                # Guardamos el valor para comparar
                valor = self._data[columna]._data[i]
                # Si no se cumple cambiamos cumple_todo a False y pasamos a la siguiente fila
                if not f(valor):
                    cumple_todo = False
                    break
            if cumple_todo:
                filas_validas.append(i)

        # Armamos el nuevo diccionario con las filas que cumplen la condicion
        nuevo = {}
        for nombre, serie in self._data.items():
            nuevo[nombre] = Series([serie._data[i] for i in filas_validas], name = nombre)
        
        # Devolvemos un nuevo DataFrame con las filas que cumplen la condicion
        return DataFrame(nuevo)

    # Elimina todas las filas que contengan valores nulos.    
    def drop_nulls(self):
        # Inicializamos lista vacia
        lista = []

        # Mantenemos las filas donde no hay None
        for columna in self._data.keys():
            lista.append((columna, lambda x: x is not None))

        return self.filter(*lista)
    
    # Devuelve un nuevo DataFrame con las filas ordenadas según la columna name. Por defecto, descending es False.
    def sort(self, name, descending=False):
        # Valida que la columna exista
        if name not in self._data:
            raise KeyError(f"La columna '{name}' no existe.")

        # Obtiene el orden de los índices basado en la columna elegida
        # Utiliza el método argsort() de la clase Series
        indices_ordenados = self._data[name].argsort(descending=descending)

        # Crea un nuevo diccionario para el nuevo DataFrame
        nuevo_data = {}
        for col_nombre, serie in self._data.items():
            # Reorganiza los datos de cada serie según los índices obtenidos
            datos_reordenados = [serie._data[i] for i in indices_ordenados]
            
            # Crea una nueva Serie con los datos en el nuevo orden
            # Mantiene el nombre y el dtype original
            nuevo_data[col_nombre] = Series(
                data=datos_reordenados, 
                name=col_nombre, 
                dtype=serie.dtype
            )

        # Devuelve una nueva instancia de DataFrame
        return DataFrame(nuevo_data)
        
    #############################################################################
    #                           METODOS ESPECIALES                              #
    #############################################################################
    # Devuelve la cantidad de filas del DataFrame.
    def __len__(self):
        return self.height

    # Devuelve la Series asociada a la columna name.
    def __getitem__(self, name):
        # Si no existe una columna con ese nombre se genera error
        # if not name in self._data:
            # raise TypeError("No existe columna con ese nombre")
        return self._data[name]

    # Agrega o sobreescribe la columna name con la Series value. 
    def __setitem__(self, name, value):
        # Verificamos que value sea una Serie
        if isinstance(value, Series) and len(value) == self.height:
            # Cambiamos el contenido de esa columna. Si no existe se crea
            self._data[name] = value
        else: 
            raise ValueError("La nueva columna tiene que ser una Serie y ser del mismo largo que el dataframe")
        return self

    # Representación textual del DataFrame.   
    def __repr__(self):
        if not self._data:
            return f"DataFrame vacío\nshape: {self.shape}"

        nombres = self.columns
        num_filas = self.height
        
        # Determina qué índices de filas mostrar
        if num_filas > 10:
            indices_mostrar = list(range(5)) + ["sep"] + list(range(num_filas - 5, num_filas))
        else:
            indices_mostrar = list(range(num_filas))

        # Calcula el ancho de cada columna
        anchos = {}
        for col in nombres:
            # Buscamos el largo máximo entre: el nombre, los valores y los puntos suspensivos "..."
            largo_max_valores = max(len(str(x)) for x in self._data[col]._data)
            largo_nombre = len(col)
            anchos[col] = max(largo_max_valores, largo_nombre, 3) # El 3 es por "..."

        # Líneas decorativas
        linea_superior = "┌" + "┬".join("─" * (anchos[c] + 2) for c in nombres) + "┐"
        linea_separadora = "├" + "┼".join("─" * (anchos[c] + 2) for c in nombres) + "┤"
        linea_inferior = "└" + "┴".join("─" * (anchos[c] + 2) for c in nombres) + "┘"

        # Formato de cabecera
        cabecera = "│ " + " │ ".join(f"{col:<{anchos[col]}}" for col in nombres) + " │"

        # Formateo de filas (incluyendo la fila de separación si aplica)
        filas_formateadas = []
        for idx in indices_mostrar:
            if idx == "sep":
                # Fila de puntos suspensivos
                celdas_sep = [f"{'...':<{anchos[col]}}" for col in nombres]
                filas_formateadas.append("│ " + " │ ".join(celdas_sep) + " │")
            else:
                celdas = []
                for col in nombres:
                    valor = str(self._data[col]._data[idx])
                    celdas.append(f"{valor:<{anchos[col]}}")
                filas_formateadas.append("│ " + " │ ".join(celdas) + " │")

        # Ensamblaje final
        salida = [f"shape: {self.shape}"]
        salida.append(linea_superior)
        salida.append(cabecera)
        salida.append(linea_separadora)
        salida.extend(filas_formateadas)
        salida.append(linea_inferior)

        return "\n".join(salida)
        
###################################### # fin DataFrame # #########################################