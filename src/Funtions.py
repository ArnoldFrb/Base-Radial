
from random import uniform
from math import exp, log, sqrt
import numpy as np
import openpyxl
import pandas as pd
import os
import errno
class Funtions:

    # CONSTRUCTOR
    def __init__(self):
        pass

    # METODO PARA BASES RADIALES
    def GenerarBasesRadiales(self, min, max, row, col):
        return np.random.uniform(min, max, [row, col])

    # MEDOTO PARA OBTENER LA DISTABCIA EUCLIDIANA
    def DistanciaEuclidiana(self, entradas, matrizBasesRadiales):
        distanciasEuclidianas = []
        for basesRadiales in matrizBasesRadiales:
            sumatoria = []
            for entrada, baseRadial in zip(entradas, basesRadiales):
                sumatoria.append(pow((entrada - baseRadial), 2))
            distanciasEuclidianas.append(pow(sum(sumatoria), 0.5))
        return distanciasEuclidianas

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION BASE RADIAL
    def FuncionBaseRadial(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(pow(distanciaEuclidiana, 2) * log(distanciaEuclidiana))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION GAUSSIANA
    def FuncionGaussiana(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(exp(-pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION MULTICUADRATICA
    def FuncionMulticuadratica(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(sqrt(1 + pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION MULTICUADRATICA INVERSA
    def FuncionMulticuadraticaInversa(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(1 / sqrt(1 + pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA CALCULAR LAS SALIDAS
    def CalcularSalida(self, funcionesActivacion, interp):
        salida = []
        for funcionActivacion in funcionesActivacion:
            sumatoria = []
            for fa, ip in zip(funcionActivacion, interp):
                sumatoria.append(fa*ip[0])
            salida.append(sum(sumatoria))
        return salida
                

    # NOMBRE DE LA FUNCION ACTIVACION
    def FuncionActivacion(self, funcionActivacion, distanciasEuclidianas):
        switcher = {
            'BASERADIAL': self.FuncionBaseRadial(distanciasEuclidianas),
            'GAUSSIANA': self.FuncionGaussiana(distanciasEuclidianas),
            'MULTICUADRATICA': self.FuncionMulticuadratica(distanciasEuclidianas),
            'MC_INVERSA': self.FuncionMulticuadraticaInversa(distanciasEuclidianas),
        }
        return switcher.get(funcionActivacion, "ERROR")

    # METODO PARA OBTENER EL ERROR LINAL
    def ErrorLineal(self, salidas, _salida):
        error = []
        entrenamiento = []
        for salida, _salida in zip(salidas, _salida):
            entrenamiento.append([salida[0], _salida])
            error.append(salida[0] - _salida)
        return (error, entrenamiento)

    # METODO PARA OBTENER EL ERROR G
    def ErrorG(self, errorLineal):
        error = 0
        for salida in errorLineal:
            error += np.abs(salida)
        return error / len(errorLineal)

    # METODO PARA LEER ARCHIVOS XLSX E INICIALIZAR LA CONFIGURACION DE LA NEURONA
    def Leer_Datos(self, ruta):
        entradas = []
        salidas = []

        ejercicio = os.path.basename(os.path.splitext(ruta)[0])

        workbook = openpyxl.load_workbook(ruta)

        matriz = pd.read_excel(ruta, sheet_name='Matriz')
        for i in range(len(matriz.columns)):
            entradas.append([fila[i] for fila in matriz.to_numpy()]) if 'X' in matriz.columns[i] else salidas.append([fila[i] for fila in matriz.to_numpy()])

        matrizBaseRadiales = []
        funcionActivacion = 'BASERADIAL'
        neuronas = int(uniform(1, 9))
        error = 0.001

        if 'Config' in workbook.sheetnames:
            matrizBaseRadiales = pd.read_excel(ruta, sheet_name='Bases Radiales').to_numpy()
            funcionActivacion = pd.read_excel(ruta, sheet_name='Config').to_numpy()[0][0]
            neuronas = pd.read_excel(ruta, sheet_name='Config').to_numpy()[0][2]
            error = pd.read_excel(ruta, sheet_name='Config').to_numpy()[0][1]
        
        return (ejercicio, matriz, np.array(entradas).transpose(), np.array(salidas).transpose(), matrizBaseRadiales, funcionActivacion, neuronas, error)

    def GuardarResultados(self, ejercicio, entrenamiento, entradas, salidas, basesRadiales, funcionSalida, error, neuronas):
        
        dfMatrix = pd.DataFrame(np.concatenate((np.array(entradas), np.array(salidas)), axis=1), columns=['X' + str(x+1) for x in range(len(entradas[0]))] + ['YD' + str(x+1) for x in range(len(salidas[0]))])
        dfBasesRadiales = pd.DataFrame(basesRadiales, columns=['BR' + str(x+1) for x in range(len(basesRadiales[0]))])
        dfConfig = pd.DataFrame([[funcionSalida, error, neuronas]], columns=['Func Activacion', 'Error Maximo', 'Neuronas'])

        try:
            os.mkdir('src/DATA/' + entrenamiento)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        try:
            os.mkdir('src/DATA/'+ entrenamiento +'/' + funcionSalida)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        raiz = 'src/DATA/'+ entrenamiento +'/' + funcionSalida + '/' + ejercicio + '.xlsx' if 'out' == entrenamiento else 'src/DATA/'+ entrenamiento +'/' + funcionSalida + '/' + ejercicio + ' - ' + error + '.xlsx'

        with pd.ExcelWriter(raiz) as writer: # pylint: disable=abstract-class-instantiated
            dfMatrix.to_excel(writer, sheet_name='Matriz', index=False)
            dfBasesRadiales.to_excel(writer, sheet_name='Bases Radiales', index=False)
            dfConfig.to_excel(writer, sheet_name='Config', index=False)