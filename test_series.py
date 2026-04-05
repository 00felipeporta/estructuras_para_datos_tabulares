from series import Series

############ Pruebas para series #####################
# Crear una serie y verificar operaciones básicas de acceso y longitud:
s = Series([10, 20, 30, 40, 50], name="valores")
s.head(3)
s.tail(2)
len(s)

# Agregar y extender una serie, manteniendo el tipo de datos
s1 = Series([1, 2, 3])
s2 = Series([4, 5])
s1.append(6)
s1.extend(s2)
s1

# Filtrar valores según una condición y obtener sus índices:
s = Series([10, 25, 50, 75, 90, 100])
s.filter(lambda x: x < 60) # Una Series
s.where(lambda x: x % 25 == 0) # Una lista de enteros

# Detectar y reemplazar valores nulos:
s = Series([5, None, 15, None])
s.is_null() # Una Series de booleanos
s.is_not_null() # Otra Series de booleanos
s.fill_null(0) # Una series de enteros

# Ordenar y obtener índices de ordenamiento:
s = Series([42, 7, 100, 3])
s.sort() # Una serie de enteros
s.argsort() # Una lista de indices enteros

# Combinar filtrado y agregaciones:
s = Series([5, 10, 15, 20, 25, 30])
s.filter(lambda x: x > 10).mean() # Promedio de los valores mayores a 10
s.filter(lambda x: x > 10).sum() # Suma de los valores mayores a 10

# Iterar a través de la serie:
for x in Series(list("xyz")):
    print(x)

# Determinar si la serie contiene un valor:
s = Series(["a", "a", "a", None, "z"])
"a" in s


# -------------------------Ejemplos Series------------------------

# Ejemplo mínimo, donde se pasa una secuencia de enteros.
# Ejemplo 1
serie = Series([1, 2, 3, 4])
serie
# Series: ''
# len: 4
# dtype: int
# [
#     1
#     2
#     3
#     4
# ]

serie = Series([1.0, 2.0, 3.0], name="x")
serie
# Series: 'x'
# len: 3
# dtype: float
# [
#     1.0
#     2.0
#     3.0
# ]


serie = Series([1, 2, 3], name="cantidad", dtype="float")
serie
# Series: 'cantidad'
# len: 3
# dtype: float
# [
#     1.0
#     2.0
#     3.0
# ]


serie = Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
serie.head()
# Series: ''
# len: 5
# dtype: int
# [
#     1
#     2
#     3
#     4
#     5
# ]


serie = Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
serie.tail(3)
# Series: ''
# len: 3
# dtype: int
# [
#     8
#     9
#     10
# ]


serie = Series(list("ABCD"))
serie.clone()
# Series: ''
# len: 4
# dtype: str
# [
#     A
#     B
#     C
#     D
# ]


s1 = Series([True, True, False])
s1.append(False)
s1
# Series: ''
# len: 4
# dtype: bool
# [
#     True
#     True
#     False
#     False
# ]


s1 = Series([1, 2, 3])
s2 = Series([4, 5, 6])
s1.extend(s2)
s1
# Series: ''
# len: 6
# dtype: int
# [
#     1
#     2
#     3
#     4
#     5
#     6
# ]


s = Series([1, 20, 50, 2, 100, 3])
s.filter(lambda x: x < 20)
# Series: ''
# len: 3
# dtype: int
# [
#     1
#     2
#     3
# ]


s = Series([1, 20, 50, 2, 100, 3])
indices = s.where(lambda x: x < 20)

indices
# [0, 3, 5]

# En el ejemplo decia indices en vez de i
[s[i] for i in indices]
# [1, 2, 3]


s = Series([1, 20, 50, 2, 100, 3])
s.is_null()
# Series: ''
# len: 6
# dtype: bool
# [
#     False
#     False
#     False
#     False
#     False
#     False
# ]


s = Series([5, None, None, 10])
s.is_not_null()
# Series: ''
# len: 4
# dtype: bool
# [
#     True
#     False
#     False
#     True
# ]


s = Series([5, None, None, 10])
s.fill_null(-1)
# Series: ''
# len: 4
# dtype: int
# [
#     5
#     -1
#     -1
#     10
# ]


s = Series(list("xyz"))
s.rename("letras")
s
# Series: 'letras'
# len: 3
# dtype: str
# [
#     x
#     y
#     z
# ]


s = Series([128, 256.0, 42.5, 35])
s.sort()
# Series: ''
# len: 4
# dtype: float
# [
#     35.0
#     42.5
#     128.0
#     256.0
# ]


s = Series([128, 256.0, 42.5, 35])
s.sort(descending=True)
# Series: ''
# len: 4
# dtype: float
# [
#     256.0
#     128.0
#     42.5
#     35.0
# ]


s = Series([128, 256.0, 42.5, 35])
indices = s.argsort()
indices
# [3, 2, 0, 1]

[s[i] for i in indices] # Se utilizan los indices
# [35.0, 42.5, 128.0, 256.0]


s1 = Series([1, 4, 5, 2, 10, 6, 3, 7, 8, 9])
s2 = Series([True, True, False, True])

s1.min()     # 1
s1.max()     # 9
s1.sum()     # 55
s1.mean()    # 5.5
s1.product() # 3628800
s1.std()     # 2.87228
s1.var()     # 8.25



s = Series([5, 6, 7])
s * 3.0
# Series: ''
# len: 3
# dtype: float
# [
#     15.0
#     18.0
#     21.0
# ]


s1 = Series([10, 20, 30])
s2 = Series([5, 25, 28])
s1 > s2
# Series: ''
# len: 3
# dtype: bool
# [
#     True
#     False
#     True
# ]



len(s)
# 100

20 in s
# True

200 in s
# False


s = Series([-10, 10, -20, 20, -30, 30])
s[0] # -10
s[1] # 10


s = Series([-10, 10, -20, 20, -30, 30])
for s_i in s:
    if s_i > 0:
        print(s_i)
# 10
# 20
# 30