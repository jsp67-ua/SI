import pygame
import tkinter
import random
import string
import copy
import time
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from pygame.locals import *
from variable import *
import sys

sys.setrecursionlimit(500000)


GREY = (190, 190, 190)
NEGRO = (100, 100, 100)
BLANCO = (255, 255, 255)

MARGEN = 5  # ancho del borde entre celdas
MARGEN_INFERIOR = 60  # altura del margen inferior entre la cuadrícula y la ventana
TAM = 60  # tamaño de la celda
FILS = 5  # número de filas del crucigrama
COLS = 6  # número de columnas del crucigrama

LLENA = '*'
VACIA = '-'


#########################################################################
# Detecta si se pulsa el botón de FC
#########################################################################
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if pos[0] >= anchoVentana//4-25 and pos[0] <= anchoVentana//4+25 and pos[1] >= altoVentana-45 and pos[1] <= altoVentana-19:
        return True
    else:
        return False

#########################################################################
# Detecta si se pulsa el botón de AC3
#########################################################################


def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0] >= 3*(anchoVentana//4)-25 and pos[0] <= 3*(anchoVentana//4)+25 and pos[1] >= altoVentana-45 and pos[1] <= altoVentana-19:
        return True
    else:
        return False

#########################################################################
# Detecta si se pulsa el botón de reset
#########################################################################


def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0] >= (anchoVentana//2)-25 and pos[0] <= (anchoVentana//2)+25 and pos[1] >= altoVentana-45 and pos[1] <= altoVentana-19:
        return True
    else:
        return False

#########################################################################
# Detecta si el ratón se pulsa en la cuadrícula
#########################################################################


def inTablero(pos):
    if pos[0] >= MARGEN and pos[0] <= (TAM+MARGEN)*COLS+MARGEN and pos[1] >= MARGEN and pos[1] <= (TAM+MARGEN)*FILS+MARGEN:
        return True
    else:
        return False

#########################################################################
# Busca posición de palabras de longitud tam en el almacen
#########################################################################


def busca(almacen, tam):
    enc = False
    pos = -1
    i = 0
    while i < len(almacen) and enc == False:
        if almacen[i].tam == tam:
            pos = i
            enc = True
        i = i+1
    return pos

#########################################################################
# Crea un almacen de palabras
#########################################################################


def creaAlmacen():
    f = open('d0.txt', 'r', encoding="utf-8")
    lista = f.read()
    f.close()
    listaPal = lista.split()
    almacen = []

    for pal in listaPal:
        pos = busca(almacen, len(pal))
        if pos == -1:  # no existen palabras de esa longitud
            dom = Dominio(len(pal))
            dom.addPal(pal.upper())
            almacen.append(dom)
        # añade la palabra si no está duplicada
        elif pal.upper() not in almacen[pos].lista:
            almacen[pos].addPal(pal.upper())

    return almacen

#########################################################################
# Imprime el contenido del almacen
#########################################################################


def imprimeAlmacen(almacen):
    for dom in almacen:
        print(dom.tam)
        lista = dom.getLista()
        for pal in lista:
            print(pal, end=" ")
        print()


#########################################################################
# Recorrer tablero y devuelve lista de variables
#########################################################################
def recorreTablero(tablero):
    variables = []
    restricciones = []
    contador_var_v = 1

    # Recorrer horizontalmente
    for fila in range(tablero.getAlto()):
        palabra = []  # Lista de letras de la palabra
        for col in range(tablero.getAncho()):
            celda = tablero.getCelda(fila, col)
            # print(col)
            # le resto uno para no salirme y luego se lo sumo a nombre y longitud

            # Sumamos letra a palabra
            if celda != '*' and col != tablero.getAncho() - 1:
                # print(celda)
                # print("test1")
                palabra.append(celda)

                # palabra.remove("*")
            # Llegamos a un bloqueo y tenemos palabra
            elif celda == '*':
                if palabra:
                    # print(celda)
                    # print("test2")
                    # +1 para incluir la celda actual
                    nombre = 'h' + str(len(variables) + 1)
                    # +1 para incluir la celda actual
                    longitud = len(palabra)
                    orientacion = "horizontal"
                    dominio = []
                    restricciones = []
                    var = Variable(nombre, fila, col-len(palabra),
                                   longitud, orientacion, dominio, restricciones)
                    variables.append(var)
                palabra = []
            # Final tablero y tenemos palabra
            elif palabra:
                # print(celda)
                # print("test2")
                # +1 para incluir la celda actual
                nombre = 'h' + str(len(variables) + 1)
                # +1 para incluir la celda actual

                longitud = len(palabra)+1
                orientacion = "horizontal"
                dominio = []
                restricciones = []
                var = Variable(nombre, fila, col-len(palabra),
                               longitud, orientacion, dominio, restricciones)
                variables.append(var)
                palabra = []
            # crear variable si la celda anterior *
            elif (tablero.getCelda(fila, col-1) == "*"):
                # print(celda)
                # print("test2")
                # +1 para incluir la celda actual
                nombre = 'h' + str(len(variables) + 1)
                # +1 para incluir la celda actual
                longitud = len(palabra)+1
                orientacion = "horizontal"
                dominio = []
                restricciones = []
                var = Variable(nombre, fila, col-len(palabra),
                               longitud, orientacion, dominio, restricciones)
                variables.append(var)
                palabra = []

    # Recorrer verticalmente
    for col in range(tablero.getAncho()):
        palabra = []
        for fila in range(tablero.getAlto()):
            celda = tablero.getCelda(fila, col)
            # le resto uno para no salirme y luego se lo sumo a nombre y longitud
            if celda != '*' and fila != tablero.getAlto() - 1:
                palabra.append(celda)
            # Llegamos a un bloqueo y tenemos palabra
            elif celda == '*':
                if palabra:
                    nombre = 'v' + str(contador_var_v)
                    contador_var_v += 1
                    longitud = len(palabra)
                    orientacion = "vertical"
                    dominio = []
                    restricciones = []
                    var = Variable(nombre, fila-len(palabra), col,
                                   longitud, orientacion, dominio, restricciones)
                    variables.append(var)
                palabra = []
            # Final tablero y tenemos palabra
            elif palabra:
                nombre = 'v' + str(contador_var_v)
                contador_var_v += 1
                longitud = len(palabra)+1
                orientacion = "vertical"
                dominio = []
                restricciones = []
                var = Variable(nombre, fila-len(palabra), col,
                               longitud, orientacion, dominio, restricciones)
                variables.append(var)
                palabra = []
            # crear variable si la celda anterior *
            elif (tablero.getCelda(fila-1, col) == "*"):
                nombre = 'v' + str(contador_var_v)
                contador_var_v += 1
                longitud = len(palabra)+1
                orientacion = "vertical"
                dominio = []
                restricciones = []
                var = Variable(nombre, fila-len(palabra), col,
                               longitud, orientacion, dominio, restricciones)
                variables.append(var)
                palabra = []

    # restricciones
    # 1º recorrremos verticales y comprobamos si variable v
    for var_v in variables:
        if var_v.getOrientacion() == "vertical":
            # 2º recorremos horizontales y comprobamos si variable h
            for var_h in variables:
                if var_h.getOrientacion() == "horizontal":
                    # 3º la fila máxima de la vertical debe ser mayor o igual que la fila de la horizontal
                    # Y su fila mínima debe ser menor o igual que la horizontal
                    # Y la columna máxima de la horizontal debe ser mayor o igual que la columna de la vertical
                    # Y la columna mínima de la horizontal...
                    # fMv>=fh Y fmv <= fh Y cMh >= cv Y cMh <= cv
                    # Por tanto: fmv <= fh <= fMv(fv+lv) Y cv <= ch <= cMh(ch+lh)
                    if (var_v.getFila() <= var_h.getFila() <= var_v.getFila() + var_v.getLongitud() and
                            var_h.getColumna() <= var_v.getColumna() <= var_h.getColumna() + var_h.getLongitud()):

                        # 4ª celada sera filaV-filaH y columnaV-columnaH
                        fila_cruce_h = var_h.getFila() - var_v.getFila()
                        columna_cruce_v = var_v.getColumna() - var_h.getColumna()

                        restriccion_h= ("(mi_celda: " + str(columna_cruce_v) + ", var: " + str(var_v.nombre) + ", su_celda: " + str(fila_cruce_h)+")")
                        
                        restriccion_v = ("(mi_celda: " + str(fila_cruce_h) + ", var: " + str(var_h.nombre) + ", su_celda: " + str(columna_cruce_v)+")")
                        var_h.addRestriccion(restriccion_h)
                        var_v.addRestriccion(restriccion_v)

    # Dominios
    # Pasos 1º busco almacen el dominio de long adecuada
    #      2º ver si cada palabra del dominio y cada leta de esa palabra coinciden y si sí, añadir
    # Localizar la celda del tablero que corresponde a una posición de la variable se hace con la información que tienes en la variable:
    # posición en el tablero (fila, col), horientación y longitud.
    # CORRECCIÓN
    # Solo meto todos los dominios (de su tamaño) si la palabra tiene las celdas vacias
    # Si esta completa su dominio solo tendra esa palabra (si existe)
    # si esta semicompleta cuadraremos las letas que se pueda ej. E_ -> ES, EN, EL, etc
    almacen = creaAlmacen()

    empt = False
    semi = False
    control = False
    letras_p = ""

    for var in variables:
        for palabra in almacen:
            if palabra.tam == var.getLongitud():
                for pal in palabra.getLista():
                    # print(pal)
                    letras_p = ""
                    empt = False
                    semi = False
                    control = False
                    # recorro todas las celdas de la palabra
                    for i in range(len(pal)):

                        # Solo meto todos los dominios (de su tamaño) si la palabra tiene las celdas vacias
                        # Si esta completa su dominio solo tendra esa palabra (si existe)
                        # si esta semicompleta cuadraremos las letas que se pueda ej. E_ -> ES, EN, EL, etc
                        if (tablero.getCelda(var.getFila() + (i if var.getOrientacion() == "vertical" else 0), var.getColumna() + (i if var.getOrientacion() == "horizontal" else 0)) == VACIA) and control == False:
                            empt = True

                        else:
                            control = True
                            empt = False

                        # guardamos todas las letras de las celdas de la palabra
                        # print(celda)
                        celda = tablero.getCelda(var.getFila() + (i if var.getOrientacion(
                        ) == "vertical" else 0), var.getColumna() + (i if var.getOrientacion() == "horizontal" else 0))
                        letras_p += celda
                        # print('Letras celda', letras_p)
                        # print('Letras palabra', pal)

                        # si letras_p == pal y
                        # print('Letras celda', letras_p, pal)
                        if len(letras_p) == len(pal) and len(pal) == var.getLongitud() and celda != '-' and letras_p != '-' and letras_p == pal:
                            # print('Letras celda', letras_p)
                            var.addDominio(letras_p)
                            letras_p = ""

                    # si esta semicompleta cuadraremos las letas que se pueda ej. E_ -> ES, EN, EL, etc
                    if len(letras_p) == len(pal) and len(pal) == var.getLongitud() and empt == False and semi == False:
                        #print('entra con: ', letras_p,
                        #      'y', pal, 'y', var.nombre)

                        for j in range(len(pal)):
                            # letras_p += celda
                            if letras_p[j] == pal[j] or letras_p[j] == '-':
                                semi = True

                            else:
                                semi = False
                                break

                    if empt:
                        var.addDominio(pal)
                        letras_p = ""

                    if semi:
                        var.addDominio(pal)
                        letras_p = ""

                    # if todas las letras == dominio añadir

    return variables

# Finalmente, después de inicializar todos los dominios, retornar la lista de variables

#########################################################################
# Forward Checking
#########################################################################
    """ITERACIÓN 1:

Variable seleccionada: h1

Asignamos "LO" a la variable seleccionada.
Recorremos todas las variables sin asignar y eliminamos "LO" del resto de dominios para no permitir palabras repetidas:
- Ningún dominio queda vacío.
Recorremos restricciones de h1:
- Restricción h1.restricciones[0]: eliminamos ["OS", "EL", "AL"] del dominio de var==v1 porque no tienen la letra h1.valor[h1.mi_celda==0] == 'L' en su posición su_celda==0.
- Restricción h1.restricciones[0]: eliminamos ["LA", "EL", "LE", "AL"] del dominio de v2 porque no tienen la letra h1.valor[mi_celda==1] == 'O' en su posición su_celda=0.

Dominios de las variables no asignadas después de la asignación de la variable seleccionada:
h2: ["OS", "LA", "EL", "LE", "AL"]
v1: ["LA", "LE"]
v2: ["OS"]

Ningún dominio ha quedado vacío, así que pasamos a la siguiente variable.
    """


"""
funcion FC(i variable): booleano
    para cada a € factibles[i] hacer
        Xi ← a
        si i=N solución retorna CIERTO
        sino
            si forward (i,a)
                si FC(i+1) retorna CIERTO
            Restaurar (i)
    retorna FALSO
funcion forward(i variable, a valor): booleano
    para toda j=i+1 hasta N hacer
        Vacio ← CIERTO
        para cada b € factibles[j] hacer
            si (a,b) € Rij vacio ←FALSO
            sino eliminar b de factible[j]
                Añadir b a podado[j]
        si vacio retorna FALSO
    retorna CIERTO
    
procedimiento restaura(i variable)
    para toda j=i+1 hasta N hacer
        para todo b € podado[j] hacer
            si Xi responsable filtrado b
                Eliminar b de podado[j]
                Añadir b a factible[j]
"""

# funcion FC(i variable): booleano


def forwardChecking(i, variables,count):
    #print("Itero")
    control = False
    dominios_temp = []
    count += 1

    # si i=N solución retorna CIERTO
    if (i == len(variables)):
            control = True
            print("Solución encontrada")
            print("Solución: ")
            for var in variables:
                print (var.getNombre(), ":", var.getValor())
            
            return control
    
        
    # para cada a € factibles[i] hacer

    var = variables[i]

    for a in var.getDominio():
        #print("Asignando valor", a, "a", var.getNombre())     
        # Xi ← a
        variables[i].setValor(a)
        #print(a)
        # sino

          
        
        #creamos lista temporal de todos los dominios
        
        """for var in variables:
            dominios_temp.append(var.getDominio())"""

        # print(dominios)
        # si forward (i,a)
        for var in variables:
                dominios_temp.append(copy.deepcopy(var.getDominio()))
        if forward(i, a, variables):
            """print(variables[i].getNombre(), "dominio: ", variables[i].getDominio(
            ), "valor: ", variables[i].getValor())"""
            # si FC(i+1) retorna CIERTO
            
            if (forwardChecking(i+1, variables,count)):
                #print(control)
                return TRUE
                
            
        if(restaura(i, variables, dominios_temp)) :
                    #borramos el ultimo dominio asignado
                    #print("Restauramos", variables[i].getNombre(), "con dominio", dominios_temp[i])
                    
                    
                    return forwardChecking(i, variables,count+1)
                    
                        
                    #print(control)
                    #return FALSE                
                #restaura(i, variables, dominios_temp)
        else:
            control = False
            
        
    return control

# funcion forward(i variable, a valor): booleano


def forward(i, a, variables):
    var_act = variables[i]
    vacio = TRUE
    # para toda j=i+1 hasta N hacer
    #TURORÍA "mejora de eficiencia eliminando bucles"
    
    # recorrer las variables j que tienen restricción con la variable i.
    #recorremos restricciones de i
    
    #Elimino de todas las variables el dominio asignado a la variable seleccionada
    for var in variables:
        for dominio in var.getDominio():
            if dominio == a:
                var.getDominio().remove(dominio)
                var.getPodados().append(dominio)
                vacio = FALSE
    

    #Y aqui recorremos las restricciones de la variable seleccionada para eliminar los dominios que no coincidan
    for restriccion in var_act.getRestricciones():
        #vamos directos a las variables que tienen restricciones con la variable i
        
        variable_rest = restriccion[restriccion.find(
            "var:")+5:restriccion.find("su_celda:")-2]
        for vars in variables:
            if vars.getNombre() == variable_rest:
                var_rest = vars
                # break
        # celda de la variable al curzarse
        celda = (int(restriccion[restriccion.find(
            "su_celda:")+10:restriccion.find(")")]))
        celda2 = int(restriccion[restriccion.find(
            "mi_celda:")+10:restriccion.find("var:")-2])
        
        for dominio in var_rest.getDominio() + var_act.getDominio():
            # si no cuadra la primera letra borramos
            if celda < len(dominio) and celda2 < len(dominio):
                if dominio[celda] != '#' and dominio[celda2] != '#' and dominio[celda] != a[celda2] and dominio in var_rest.getDominio():
                    #print("Eliminamos",
                    #      dominio, "de", var_rest.getNombre())
                    var_rest.getDominio().remove(dominio)
                    # Añadir b a podado[j]
                    var_rest.getPodados().append(dominio)
                    
                    vacio = FALSE
                    # print(vacio)

                        # contador += 1
        # pasamos todos a podamos menos el que hemos asignado

    variables[i].getDominio().clear()
    variables[i].getDominio().append(a)
        # si vacio retorna FALSO
        # print("Vacío: ", vacio)
    if vacio == TRUE:
        return FALSE
    
    return TRUE
# procedimiento restaura(i variable)


def restaura(i, variables, dominios_temp):
    # Recupera el valor de la variable actual
    valor_actual = variables[i].getValor()
    
    #
    for j, var in enumerate(variables):
        if j < len(dominios_temp):
            #print("Restauramos", var.getNombre(), "con dominio", dominios_temp[j])
            var.setDominio(dominios_temp[j])
                 
            
    #comprobamos si hay dominios vacios
    for var in variables:
        if not var.getDominio():
            #print("No hay solución")
            return FALSE
    
    #print("Eliminamos", valor_actual, "de", variables[i].getNombre())
    variables[i].getDominio().remove(valor_actual)
    
    
    return TRUE
    
    
    


#########################################################################
# Principal
#########################################################################
def main():
    root = tkinter.Tk()  # para eliminar la ventana de Tkinter
    root.withdraw()  # se cierra
    pygame.init()

    reloj = pygame.time.Clock()

    anchoVentana = COLS*(TAM+MARGEN)+MARGEN
    altoVentana = MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN

    dimension = [anchoVentana, altoVentana]
    screen = pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1: Crucigrama")

    botonFC = pygame.image.load("botonFC.png").convert()
    botonFC = pygame.transform.scale(botonFC, [50, 30])

    botonAC3 = pygame.image.load("botonAC3.png").convert()
    botonAC3 = pygame.transform.scale(botonAC3, [50, 30])

    botonReset = pygame.image.load("botonReset.png").convert()
    botonReset = pygame.transform.scale(botonReset, [50, 30])

    almacen = creaAlmacen()
    game_over = False
    tablero = Tablero(FILS, COLS)
    # autorellenarTableroAleatorio(tablero)
    # cargarTableroDesdeLista(tablero, datos_tablero)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONUP:
                # obtener posición y calcular coordenadas matriciales
                pos = pygame.mouse.get_pos()
                variables = recorreTablero(tablero)
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    tiempo_inicio = time.time()
                    print("FC")
                    # llama a recorrer tablero
                    
                    """
                    print("Variables encontradas:")
                    for var in variables:
                        print(
                            f"Nombre: {var.nombre},Posición {var.fila , var.columna}, Orientación: {var.orientacion}, Longitud: {var.longitud}, restricciones: {var.restricciones}, Dominio: {var.dominio}")
                        for i in range(var.getLongitud()):
                            fila = var.getFila() + (i if var.getOrientacion() == "vertical" else 0)
                            columna = var.getColumna() + (i if var.getOrientacion() == "horizontal" else 0)
                            contenido_celda = tablero.getCelda(fila, columna)
                            print(contenido_celda, end="")
                        print()"""

                    # print(tablero)
                    # aquí llamar al forward checking
                    res = forwardChecking(0, variables,0)
                    tiempo_fin = time.time()
                    tiempo_transcurrido = tiempo_fin - tiempo_inicio
                    print("Tiempo de ejecución: ", tiempo_transcurrido)
                    if res == FALSE:
                        MessageBox.showwarning("Alerta", "No hay solución")
                    if res== TRUE:
                        print("\n" + "Variables despues de aplicar el FC:")
                        for var in variables:
                            print(
                                f"Nombre: {var.nombre}, Valor: {var.valor}")
                            print()

                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):
                    print("AC3")
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):
                    tablero.reset()
                elif inTablero(pos):
                    colDestino = pos[0]//(TAM+MARGEN)
                    filDestino = pos[1]//(TAM+MARGEN)
                    if event.button == 1:  # botón izquierdo
                        if tablero.getCelda(filDestino, colDestino) == VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button == 3:  # botón derecho
                        c = askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())

        # código de dibujo
        # limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(
            screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana], 0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col) == VACIA:
                    pygame.draw.rect(screen, BLANCO, [
                                     (TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col) == LLENA:
                    pygame.draw.rect(
                        screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else:  # dibujar letra
                    pygame.draw.rect(screen, BLANCO, [
                                     (TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente = pygame.font.Font(None, 70)
                    texto = fuente.render(
                        tablero.getCelda(fil, col), True, NEGRO)
                    screen.blit(texto, [(TAM+MARGEN)*col +
                                MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])
        # pintar botones
        screen.blit(botonFC, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        # actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over == True:  # retardo cuando se cierra la ventana
            pygame.time.delay(500)

    pygame.quit()


if __name__ == "__main__":
    main()
