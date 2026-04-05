from series import Series

# Estructura bidimensional de datos, organizada en filas y columnas.
class DataFrame:
    #########################################################################
    #                               INICIALIZACION                          #
    #########################################################################
    def __init__(self, data):
        self._data = {}                        

        if isinstance(data, dict):            
            if len(data.keys()) != len(set(data.keys())): 
                raise ValueError("Los nombres de las columnas no pueden repetirse.")
            
            for nombre_col, valor in data.items():
                if isinstance(valor, Series): 
                    copia = valor.clone()
                    copia.rename(nombre_col)
                    self._data[nombre_col] = copia 
                elif isinstance(valor, list):
                    self._data[nombre_col] = Series(valor, name = nombre_col)
                else:
                    raise TypeError("Los valores del diccionario tienen que ser listas o instancias de Series")
        
        elif isinstance(data, list):
            if all(isinstance(x, Series) for x in data):
                nombres = [x.name for x in data]
                if len(nombres) != len(set(nombres)):
                    raise ValueError("Los nombres de las Series no pueden repetirse.")

                for x in data:
                    self._data[x.name] = x.clone()                
            else:
                raise TypeError("Los elementos de la lista tienen que ser ser Series")    
        
        else:
            raise TypeError("data tiene que ser list o dict")

        longitudes = [len(s) for s in self._data.values()] 

        if len(set(longitudes)) != 1: 
            raise ValueError("Todas las columnas tienen que tener la misma longitud.")

    ###############################################################
    #                     ATRIBUTOS                               #
    ###############################################################
    
    @property 
    def columns(self):
        return list(self._data.keys())

    @property
    def dtypes(self):
        return [s.dtype for s in self._data.values()]

    @property
    def height(self):
        columna = list(self._data.keys())[0]
        return len(self._data[columna]) # Usa el __len__ de Series

    @property
    def width(self):
        return len(self._data)    
    
    @property
    def shape(self):
        return (self.height, self.width)

    @property
    def schema(self):
        return {clave: valor.dtype for clave, valor in self._data.items()}
    
    ######################################################################
    #                            METODOS                                 #
    ######################################################################

    def head(self, n=5):      
        return DataFrame({nombre: serie.head(n) for nombre, serie in self._data.items()})

    def tail(self, n=5):
        return DataFrame({nombre: serie.tail(n) for nombre, serie in self._data.items()})

    def select(self, *columns):
        nuevas_columnas = {}
        for columna in columns:
            if columna not in self._data:
                raise KeyError(f"La columna '{columna}' no existe.")
            nuevas_columnas[columna] = self._data[columna]
        return DataFrame(nuevas_columnas)
        
    def filter(self, *predicates):
        if not predicates:
            return self

        filas_validas = []
        for i in range(self.height):
            cumple_todo = True
            for (columna, f) in predicates:
                # CAMBIO: Se usa self._data[columna][i] en vez de ._data[i]
                valor = self._data[columna][i] 
                if not f(valor):
                    cumple_todo = False
                    break
            if cumple_todo:
                filas_validas.append(i)

        nuevo = {}
        for nombre, serie in self._data.items():
            # CAMBIO: Se usa serie[i] en vez de serie._data[i]
            nuevo[nombre] = Series([serie[i] for i in filas_validas], name = nombre)
        
        return DataFrame(nuevo)

    def drop_nulls(self):
        lista = [(columna, lambda x: x is not None) for columna in self._data.keys()]
        return self.filter(*lista)
    
    def sort(self, name, descending=False):
        if name not in self._data:
            raise KeyError(f"La columna '{name}' no existe.")

        indices_ordenados = self._data[name].argsort(descending=descending)

        nuevo_data = {}
        for col_nombre, serie in self._data.items():
            # CAMBIO: Se usa serie[i] en vez de serie._data[i]
            datos_reordenados = [serie[i] for i in indices_ordenados]
            nuevo_data[col_nombre] = Series(
                data=datos_reordenados, 
                name=col_nombre, 
                dtype=serie.dtype
            )

        return DataFrame(nuevo_data)
        
    #############################################################################
    #                           METODOS ESPECIALES                              #
    #############################################################################

    def __len__(self):
        return self.height

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        if isinstance(value, Series) and len(value) == self.height:
            self._data[name] = value
        else: 
            raise ValueError("La nueva columna tiene que ser una Serie y del mismo largo")
        return self

    def __repr__(self):
        if not self._data:
            return f"DataFrame vacío\nshape: {self.shape}"

        nombres = self.columns
        num_filas = self.height
        
        if num_filas > 10:
            indices_mostrar = list(range(5)) + ["sep"] + list(range(num_filas - 5, num_filas))
        else:
            indices_mostrar = list(range(num_filas))

        anchos = {}
        for col in nombres:
            # CAMBIO: Se itera directamente sobre la serie gracias a __iter__
            largo_max_valores = max(len(str(x)) for x in self._data[col])
            anchos[col] = max(largo_max_valores, len(col), 3)

        linea_sup = "┌" + "┬".join("─" * (anchos[c] + 2) for c in nombres) + "┐"
        linea_sep = "├" + "┼".join("─" * (anchos[c] + 2) for c in nombres) + "┤"
        linea_inf = "└" + "┴".join("─" * (anchos[c] + 2) for c in nombres) + "┘"

        cabecera = "│ " + " │ ".join(f"{col:<{anchos[col]}}" for col in nombres) + " │"

        filas_formateadas = []
        for idx in indices_mostrar:
            if idx == "sep":
                celdas_sep = [f"{'...':<{anchos[col]}}" for col in nombres]
                filas_formateadas.append("│ " + " │ ".join(celdas_sep) + " │")
            else:
                celdas = []
                for col in nombres:
                    # CAMBIO: Se usa self._data[col][idx] en vez de ._data[idx]
                    valor = str(self._data[col][idx])
                    celdas.append(f"{valor:<{anchos[col]}}")
                filas_formateadas.append("│ " + " │ ".join(celdas) + " │")

        salida = [f"shape: {self.shape}", linea_sup, cabecera, linea_sep]
        salida.extend(filas_formateadas)
        salida.append(linea_inf)

        return "\n".join(salida)