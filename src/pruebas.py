from math import *
from re import findall
from numpy import array, random

def validar_funtion(patrones, min, max, funtion = '(2*x + 3*y + 72)/6', count = 0):

    print(any([carac in ['(', '*', '+', '-', '/', ',', ')'] for carac in findall('[^a-z A-Z 0-9]', funtion)]))

    if funtion.islower():
        funtion_aux = funtion.replace('exp', '')
        funtion_aux = funtion_aux.replace('sqrt', '')
        funtion_aux = funtion_aux.replace('sin', '')
        funtion_aux = funtion_aux.replace('cos', '')
        funtion_aux = funtion_aux.replace('tan', '')
        funtion_aux = funtion_aux.replace('log', '')
        if len(findall('[a-w]', funtion_aux)) == 0:
            flag = False
            for carac in findall('[^a-z A-Z 0-9]', funtion):
                if carac in ['(', '*', '+', '-', '/', ',', ')']:
                    flag = True
                else:
                    flag = False
                    return('Solo se permiten caracteres especiales como "(, *, +, -, /, )"', None, None)
            if flag:
                if 'x' in funtion:
                    count += 1
                if 'y' in funtion:
                    count += 1
                if 'z' in funtion:
                    count += 1
                entradas = random.uniform(min, max, [patrones, count])
                salidas = []
                for entrada in entradas:
                    if len(entrada) == 1:
                        x = entrada[0]
                        salidas.append([eval(funtion)])
                    if len(entrada) == 2:
                        x = entrada[0]
                        y = entrada[1]
                        salidas.append([eval(funtion)])
                    if len(entrada) == 3:
                        x = entrada[0]
                        y = entrada[1]
                        z = entrada[2]
                        salidas.append([eval(funtion)])
                return (None, entradas, array(salidas))
            else:
                return('La Funcion ingresada no cumple los paramtros de una funcion establedida para el programa', None, None)
        else:
            return('No se permiten variables que no sean x, y & z', None, None)
    else:
        return('No se permiten variables MAYUSCULAS', None, None)
        
(mensage, entradas, salidas) = validar_funtion(5, 1, 5)
if not mensage:
    print(entradas)
    print(salidas)
else:
    print(mensage)