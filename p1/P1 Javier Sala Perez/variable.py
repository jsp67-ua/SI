# Clase para variables como en la traza dada y explicado en clase
# despues de todo lo del tablero han de crearse variables con ej.
# * h1:
# - Posición: (0, 0)
# - Longitud: 2
# - Orientación: horizontal
# - Dominio: ["LO", "OS", "LA", "EL", "LE", "AL"]
# - Restricciones: [(mi_celda: 0, var: v1, su_celda: 0),
#                  (mi_celda: 1, var: v2, su_celda: 0)]

class Variable:
    def __init__(self, nombre, fila, columna, longitud, orientacion, dominio, restricciones):
        self.nombre = nombre
        self.fila = fila
        self.columna = columna
        self.longitud = longitud
        self.orientacion = orientacion
        self.dominio = dominio
        self.restricciones = []
        self.valor = None
        self.podados = []
        self.dominioOriginal = dominio

    def addRestriccion(self, restriccion):
        self.restricciones.append(restriccion)

    def addDominio(self, dominio):
        self.dominio.append(dominio)

    def getNombre(self):
        return self.nombre

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    def getLongitud(self):
        return self.longitud

    def getOrientacion(self):
        return self.orientacion

    def getDominio(self):
        return self.dominio

    def getRestricciones(self):
        return self.restricciones

    def setDominio(self, dominio):
        self.dominio = dominio

    def setValor(self, valor):
        self.valor = valor

    def getValor(self):
        return self.valor

    def setPodados(self, podados):
        self.podados = podados

    def getPodados(self):
        return self.podados

    def getDominioOriginal(self):
        return self.dominioOriginal

    def setDominioOriginal(self, dominio):
        self.dominio.append(dominio)

    def __str__(self):
        return f"Nombre {self.nombre} Posición: ({self.fila}, {self.columna}) Tipo: {self.orientacion} Dominio: {self.dominio} Restricciones: {self.restricciones}"
