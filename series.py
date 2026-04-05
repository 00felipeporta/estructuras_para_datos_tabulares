# Clase Series
class Series:
    # Creamos un diccionario privado que mapea str con tipos validos
    _mapeo = {
            "str": str,
            "float": float,
            "int": int,
            "bool": bool,
    }
    
    # name  
    @property
    def name(self):
        return self._name

    # Validamos name
    @name.setter
    def name(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser un str")
        self._name = valor

    # dtype
    @property
    def dtype(self):
        return self._dtype
    
    # Validamos dtype
    @dtype.setter
    def dtype(self, valor):
        # si dtype es None es valido
        if valor is None:
            self._dtype = None
            self._tipo = None # Almacenamos el tipo que corresponde a dtype en vez del string
        # Verificamos que sea str y sea de un tipo valido
        elif isinstance (valor, str) and valor in Series._mapeo:
            self._dtype = valor
            self._tipo = Series._mapeo[valor]
        else:
            raise TypeError("dtype tiene que ser 'int', 'float', 'str' o 'bool'")            
    
    # Indica la longitud de la serie
    @property
    def len(self):
        return len(self._data)

    ######################################################################################
    #                                METODOS DE CLASE                                    #
    ######################################################################################

    # Segun el tipo de x y el dtype, devuelve x, x convertido o error
    def _validador(self, x):
        # Si es None lo devolvemos directamente
        if x is None:
            return x
        # Si es del mismo tipo lo devolvemos
        if type(x) is self._tipo:
            return x
        # Si x es numerico (int o float) pero no de dtype (esa posibilidad estaria en el if anterior), lo convertimos
        if (self._tipo in (int, float)) and (type(x) in (int, float)):
            return self._tipo(x)
        # Si no se cumple nada de eso, hay un error
        raise TypeError("El valor tiene que ser compatible con el dtype.")

    # Devuelve una nueva lista solo con los valores no None
    def _filtrador(self):
        return [x for x in self._data if x is not None]
    
    # Verifica que la serie sea numerica (int o float) y la devuelve sin None
    def _es_numerico(self):
        # Validamos que el dtype sea numerico (int o float)
        if self._tipo not in (int, float):
            raise TypeError("Este método solo puede aplicarse a series de tipo 'int' o 'float'.")
        # Filtramos los nulos
        numericos = self._filtrador()
        return numericos
   
    # Metodos auxiliares para comparacion
    # Realiza comparaciones y devuelve serie de booleanos
    def _operar(self, other, operacion, aritmetico = False):
        # Creamos lista vacia para almacenar los resultados
        datos_nuevos = []
        # Verificamos que self sea una serie numerica
        if self._es_numerico():   
            # Verificamos que other sea numerico
            if type(other) is int or type(other) is float:            
                if aritmetico:
                    # Opero los elementos uno por uno y queda none en caso de que al menos uno sea none
                    datos_nuevos += [None if i is None else operacion(i, other) for i in self._data]                    
                    return Series(datos_nuevos)
                # Si la operacion es una comparacion
                else:
                    # Devolvemos lista con el resultado de las comparaciones. Si hay un None es falso
                    datos_nuevos += [False if i is None else operacion(i, other) for i in self._data]
                    return Series(datos_nuevos, dtype = "bool")
            #Verificamos que other tambien sea una serie numerica y que ambas tengan el mismo largo
            elif isinstance(other, Series) and other._es_numerico() and len(self) == len(other):
                if aritmetico:
                    # Opero los elementos uno por uno y queda none en caso de que al menos uno sea none
                    datos_nuevos += [None if a is None or b is None else operacion(a, b) for a, b in zip(self._data, other._data)]
                    return Series(datos_nuevos)
                else:
                    # Comparo uno por uno. Si a o b es None la comparacion da falso
                    datos_nuevos += [False if a is None or b is None else operacion(a, b) for a, b in zip(self._data, other._data)]
                    return Series(datos_nuevos, dtype = "bool")
            else: 
                raise TypeError("Las listas deben ser del mismo tamaño")
    
    #############################################################################################################
    #                                               init                                                        #
    #############################################################################################################
    def __init__(self, data, name = "", dtype = None):   
    
        self.name = name
        self.dtype = dtype
        
        # Verificamos que lo que se introduzca como data sea una lista o tupla
        if not isinstance(data, list):
            raise TypeError("Data debe ser una lista.")
        # Si todos los elementos son None se produce un error
        if all(x is None for x in data):
            raise TypeError("No pueden ser todos elementos None")
        
        
        if self.dtype is None:
            #------------------ Si no se definio ningun dtype---------------------
            # Si todos los elementos que no son None son del mismo tipo (y es valido) los asignamos a self._data y le asignamos el dtype y tipo correspondientes
            tipos_data = list(set(type(x) for x in data if x is not None)) # Convertimos a lista para utilizar indexado despues
            if len(tipos_data) == 1 and tipos_data[0] in Series._mapeo.values():
                self.dtype = tipos_data[0].__name__ # str
                self._data = data 
                                        
            # Verificamos si hay solo int y float mezclados (ademas de posibles None)
            elif all(x is None or type(x) in (int, float) for x in data):
                
                # Evaluamos el tipo del primer elemento y lo dejamos vigente
                for x in data:
                    if x is not None:
                        self.dtype = type(x).__name__ # tipo = int o float
                        break
                
                # Si el primer elemento es int convertimos los float a int 
                # Si el primer elemento es float convertimos los int a float
                self._data = [self._tipo(x) if x is not None else None for x in data]
            
            # Si no se cumple ninguna de las condiciones anteriores:
            else:
                raise TypeError("Los datos que no son None tienen que ser todos del mismo tipo. Solo se puede mezclar int y float")

        else:
            #------------------ Si el usuario ingresó un dtype no None ---------------------           
            # Si todos los elementos son del mismo tipo asignamos data a self._data
            # Hacemos la comparacion de esta manera y no con isinstance porque si se puede interpretar que los enteros son booleanos
            if self._tipo in [bool, str] and all(x is None or type(x) is self._tipo for x in data): 
                self._data = data
                
            # Verificamos si hay solo int, float o None
            elif self._tipo in [int, float] and all(x is None or type(x) is int or type(x) is float for x in data):
                # Asignamos a data los elementos ya convertidos al tipo vigente               
                self._data = [self._tipo(x) if x is not None and type(x) is not self._tipo else x for x in data]
            
            # Si no se cumplen esas condiciones se produce error
            else:
                raise TypeError(
                    "Los datos que no son None tienen que ser todos del mismo tipo y coincidentes con dtype.\n Sólo se pueden mezclar int y float."
                )

#####################################################################################
#                          METODOS PARA MANIPULAR DATOS                             #
#####################################################################################

    # Devuelve una nueva serie, idéntica a la original
    def clone(self):
        return Series(
            data = self._data, 
            name = self.name,
            dtype = self.dtype,
        )
    # Devuelve una nueva serie con los primeros n valores
    def head(self, n=5):
        return Series(
            data = self._data[:n], 
            name = self.name,
            dtype = self.dtype,
        )

    # Devuelve una nueva serie con los últimos n valores
    def tail(self, n=5):
            return Series(
            data = self._data[-n:], 
            name = self.name,
            dtype = self.dtype,
        )

    # Agrega el elemento x al final de la serie.
    def append(self, x):
        # Si se cumplen las condiciones devuelve la x compatible con el dtype o se genera error
        x = Series._validador(self, x)
        # Agregamos x a data
        self._data.append(x)

    # Extiende la serie con los elementos de la serie s.
    def extend(self, s):
        # Validamos que sean del mismo dtype o numerico, lo que agilizaria mucho en caso de haber una lista con muchisimos None
        if s._tipo is self._tipo or (s._tipo in (int, float) and self._tipo in (int, float)):
            for i in s._data:
                self._data.append(i)
            return self
        else: 
            raise TypeError("Las series tienen que ser de tipo compatible")
            
    # Devuelve una nueva serie con los elementos de la serie que al ser pasados a f devuelven un valor verdadero. 
    def filter(self, f):
        # Guardo una lista con los valores que cumplen la condicion
        lista = []
        lista  = [x for x in self._data if f(x)]
        return Series(data = lista)

    # Devuelve una nueva lista con los índices de los elementos que al ser pasados a f devuelven True
    def where(self, f):	
        lista = []
        lista  += (i for i in range(len(self._data)) if f(self._data[i]))
        return lista

    # Devuelve una serie de valores booleanos. Cada elemento será True si el elemento original es nulo.
    def is_null(self):
        return Series(
                    data = [x is None for x in self._data], 
                    dtype = "bool",
                )

    # Devuelve una serie de valores booleanos. Cada elemento será True si el original es no nulo.
    def is_not_null(self):
        return Series(
                    data = [x is not None for x in self._data], 
                    dtype = "bool",
                )
    # Reemplaza los valores nulos por x.
    def fill_null(self, x):
        # Si se cumplen las condiciones devuelve la x compatible con el dtype o se genera error
        x = Series._validador(self, x)
        self._data = [x if i is None else i for i in self._data]
        return self
    # Cambia el nombre de la serie por name.
    def rename(self, name):
        self.name = name
        return self

    # Ordena la serie. 
    def sort(self, descending = False, in_place = False):
        # descending determina si se ordena de forma ascendente (por defecto) o descendente. 
        # in_place determina si se modifica la serie in-place o si se devuelve una nueva (por defecto).
        lista = Series._filtrador(self) # Lista con valores no None
        lista = sorted(lista, reverse = descending) # Lista ordenada
        resultado = lista + [None] * (len(self) - len(lista)) # Agregamos los None siempre al final
        # Si in_place modificamos data
        if in_place:
            self._data =  resultado 
            return self
        # Si no es in_place devolvemos una nueva serie
        elif not in_place:
            return Series(resultado)

    # Devuelve una lista con los indices que ordenan a la serie. 
    def argsort(self, descending = False): # El parametro descending determina si se ordena de forma ascendente (por defecto) o descendente.
        # Guardamos los indices de los valores que no son None        
        indices = [i for i in range(len(self._data)) if self._data[i] is not None]
        
        # Guardamos los indices de los None
        indices_none = [i for i in range(len(self._data)) if self._data[i] is None]
        
        # Ordenamos los indices validos tomando de referencia sus valores
        indices.sort(key = lambda x: self._data[x], reverse = descending)
        
        # Devolvemos la lista con los Nones al final
        return indices + indices_none

#######################################################################################
#                             Métodos para calcular agregaciones                      #
#######################################################################################
    # Para todos los metodos verificamos primero estar trabajando con series numericas y filtramos los none
    # El valor más pequeño.
    def min(self):
        datos = self._es_numerico()
        return min(datos)

    # El valor más grande.
    def max(self):
        datos = self._es_numerico()
        return max(datos)

    # La suma de los elementos.
    def sum(self):
        datos = self._es_numerico()
        return sum(datos)

    # El promedio de los elementos.
    def mean(self):
        datos = self._es_numerico()
        n = len(datos)        
        total = sum(datos)
        return total / n

    # El producto de los elementos.
    def product(self):
        datos = self._es_numerico()      
        resultado = 1
        for x in datos:
            resultado *= x
        return resultado

    # La varianza.
    def var(self):
        datos = self._es_numerico()
        n = len(datos)           
        media = self.mean()
        
        # Suma de los cuadrados de las diferencias
        cuadrados_difrencias = sum([(x - media) ** 2 for x in datos])
        
        return cuadrados_difrencias / n 

    # El desvío estándar. Raiz cuadrada de la varianza
    def std(self):
        varianza = self.var()           
        return varianza ** 0.5

#######################################################################################
#                             METODOS ESPECIALES                                      #
#######################################################################################
#------------------------------- ARITMETICOS------------------------------------------#
    # Operaciones de comparacion
    def __eq__(self, other): # Igual a
        return self._operar(other, lambda a, b: a == b)
    def __gt__(self, other): # Mayor que
        return self._operar(other, lambda a, b: a > b)
    def __ge__(self, other):	# Mayor o igual que:
        return self._operar(other, lambda a, b: a >= b)
    def __lt__(self, other):	# Menor que
        return self._operar(other, lambda a, b: a < b)
    def __le__(self, other):	# Menor o igual que
        return self._operar(other, lambda a, b: a <= b)
    
    # Operaciones basicas
    def __add__(self, other):	# Suma
        return self._operar(other, lambda a, b: a + b, aritmetico = True)        
    def __sub__(self, other):  # Resta
        return self._operar(other, lambda a, b: a - b, aritmetico = True)        
    def __mul__(self, other): # Multiplicacion
        return self._operar(other, lambda a, b: a * b, aritmetico = True)        
    def __truediv__(self, other): # Division flotante
        return self._operar(other, lambda a, b: a / b, aritmetico = True)
    def __pow__(self, other): # Potencia
        return self._operar(other, lambda a, b: a ** b, aritmetico = True)        

#--------------------------------ACCESO E ITERACION-----------------------------------#
        
    # Representación textual
    def __repr__(self):
        # Si hay hasta 10 elementos aparecen todos
        elementos = ""
        if len(self._data) <= 10:
            for i in self._data:
                elementos += f"    {str(i)}\n"
        # Si hay mas de 10 elementos
        else:
            for i in self._data[:5]: # Primeros 5 elementos
                elementos += f"    {str(i)}\n"
            elementos += "    ...\n" # Puntos suspensivos del medio
            for i in self._data[-5:]: # Primeros 5 elementos
                elementos += f"    {str(i)}\n"
        mensaje = (
            f"Series: '{self.name}'\n"
            f"len: {len(self._data)}\n"
            f"dtype: {self.dtype}\n"
            f"[\n{elementos}]"
            )
        return mensaje
    
    # Longitud de la serie
    def __len__(self):
        return len(self._data)
    
    # Determina si item se encuentra en la serie
    def __contains__(self, item):
        return item in self._data

    # Obtiene el elemento en la posición index
    def __getitem__(self, index):
        return self._data[index]
    
    # Permite iterar sobre los elementos de la serie
    def __iter__(self):
        return iter(self._data)
        
###################################### # fin # #########################################