
from random import uniform
from tkinter import filedialog
from math import exp, log, sqrt
import numpy as np
import openpyxl
import pandas as pd
import os
import errno
from scipy.interpolate import interp2d

class Funtions:

    # CONSTRUCTOR
    def __init__(self):
        pass

    # METODO PARA GENERAR PESOS
    def GenerarBasesRadiales(self, min, max, row, col):
        return np.random.uniform(min, max, [row, col])

    # MEDOTO PARA OBTENER LA FUNCION SOMA
    def DistanciaEuclidiana(self, entradas, matrizBasesRadiales):
        distanciasEuclidianas = []
        for basesRadiales in matrizBasesRadiales:
            sumatoria = []
            for entrada, baseRadial in zip(entradas, basesRadiales):
                sumatoria.append(pow((entrada - baseRadial), 2))
            distanciasEuclidianas.append(pow(sum(sumatoria), 0.5))
        return distanciasEuclidianas

    # METODO PARA OBTENER LA FUNCION SIGMOIDE
    def FuncionBaseRadial(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(pow(distanciaEuclidiana, 2) * log(distanciaEuclidiana))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION GAUSSIANA
    def FuncionGaussiana(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(exp(-pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION TANGENTE HIPERBOLICA
    def FuncionMulticuadratica(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(sqrt(1 + pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION GAUSSIANA
    def FuncionMulticuadraticaInversa(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(1 / sqrt(1 + pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

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

    # METODO PARA OBTENER EL ERROR PATRON
    def ErrorG(self, errorLineal):
        error = 0
        for salida in errorLineal:
            error += np.abs(salida)
        return error / len(errorLineal)

    def ActualizarPesos(self, pesos, entradas, error, rata):
        for i in range(len(pesos)):
            for j in range(len(pesos[0])):
                pesos[i][j] += (entradas[i] * error[j] if isinstance(error, list) else error * rata)
        return pesos

    def ActualizarUmbrales(self, umbrales, error, rata):
        for i in range(len(umbrales)):
            umbrales[i] += (rata * error[i] if isinstance(error, list) else error * 1)
        return umbrales
    
    def _ActualizarPesos(self, pesos, entradas, error, rata, rataDinamica, _pesos):
        for i in range(len(pesos)):
            for j in range(len(pesos[0])):
                pesos[i][j] += (entradas[i] * error[j] if isinstance(error, list) else error * rata) + (rataDinamica * (pesos[i][j] - _pesos[i][j]))
        return pesos

    def _ActualizarUmbrales(self, umbrales, error, rata, rataDinamica, _umbrales):
        for i in range(len(umbrales)):
            umbrales[i] += (rata * error[i] if isinstance(error, list) else error * 1) + (rataDinamica * (umbrales[i] - _umbrales[i]))
        return umbrales

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
            neuronas = pd.read_excel(ruta, sheet_name='Config').to_numpy()[0][1]
            error = pd.read_excel(ruta, sheet_name='Config').to_numpy()[0][2]
        
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
            

if __name__ == '__main__':
    # fn = Funtions()
    # (ejercicio, matrix, entradas, salidas, pesos, umbrales, config, funcionActivacion, delta) = fn.Leer_Datos(filedialog.askopenfilename())
    # print(ejercicio, matrix, entradas, salidas, pesos, umbrales, config, funcionActivacion, delta)
    # # print(np.zeros(3))
    # # print(list(range(len([3,4,5]))))
    # thislist = [1, 2, 3]
    # xd = [4, 3]
    # print(['W' + str(x+1) for x in thislist] + ['YD' + str(x+1) for x in xd])
    # a = np.array([[1, 2], [3, 4]])
    # b = np.array([[5], [6]])
    # print(np.concatenate((a, b), axis=1))
    x = [[1, -0.08, -0.16], [1, -0.08, -0.08], [1, 0.03, 0.34], [1, -0.16, -0.08]]
    y = [[1], [1], [0], [0]]
    print(np.linalg.lstsq(np.array(x), np.array(y), rcond=-1)[0])
    x = [[ 1, -0.0866434, -0.16182117], [ 1, -0.0866434, -0.0866434 ], [ 1,  0.03220683, 0.3486618 ], [ 1, -0.16182117, -0.0866434 ]]
    print(np.linalg.lstsq(np.array(x), np.array(y), rcond=-1)[0])
    