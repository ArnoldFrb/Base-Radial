
from skimage.io import imread
from skimage.util import crop
from math import exp, log, sqrt
from shutil import copy
import numpy as np
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
    def EcuacionBaseRadial(self, funcionesActivacion, interp):
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
    def Leer_Datos(self, ruta_img, ruta_arc = 'E:/WORLD/PYTHOM/AraneaeIA/src/data/Araneae.xlsx'):
        img = imread(ruta_img, as_gray=True)
        if img.shape[1] < 800:
            return (False, None, None, None, None, None, None, None, None)
        a = img.shape[1]-800
        img = crop(img, ((0, 0), (int(a/2), a - int(a/2))), copy=False)
        array_img = np.apply_along_axis(sum, 0, img)

        entradas = []
        salidas = []

        matrizBaseRadiales = []
        funcionActivacion = 'BASERADIAL'
        neuronas = len(array_img)
        error = 0.001
        arañas = []

        ruta_img = [ruta_img, os.path.basename(os.path.splitext(ruta_img)[0]), os.path.basename(os.path.splitext(ruta_img)[1])]

        if os.path.exists(ruta_arc):
            matriz = pd.read_excel(ruta_arc, sheet_name='Matriz')
            aux_salidas = np.array([[row[len(matriz.columns) - 1]] for row in matriz.to_numpy()])
            aux_entradas = np.delete(matriz.to_numpy(), len(matriz.columns) - 1, axis=1)

            for e, s in zip(aux_entradas, aux_salidas):
                entradas.append(e)
                salidas.append(s)

            if array_img in np.array(entradas):                
                return (False, None, None, None, None, None, None, None, None)

            entradas.append(array_img)
            salidas.append([len(salidas) + 1])

            matrizBaseRadiales = pd.read_excel(ruta_arc, sheet_name='Bases Radiales').to_numpy()
            arañas = pd.read_excel(ruta_arc, sheet_name='Araneae').to_numpy().tolist()
            funcionActivacion = pd.read_excel(ruta_arc, sheet_name='Config').to_numpy()[0][0]
            neuronas = pd.read_excel(ruta_arc, sheet_name='Config').to_numpy()[0][2]
            error = pd.read_excel(ruta_arc, sheet_name='Config').to_numpy()[0][1]

        else:
            entradas.append(array_img)
            salidas.append([1])
        
        return (True, ruta_img, np.array(entradas), np.array(salidas), arañas, matrizBaseRadiales, funcionActivacion, neuronas, error)

    def GuardarResultados(self, arañas, entradas, salidas, basesRadiales, funcionSalida, error, neuronas):
        
        dfMatrix = pd.DataFrame(np.concatenate((np.array(entradas), np.array(salidas)), axis=1), columns=['X' + str(x+1) for x in range(len(entradas[0]))] + ['YD' + str(x+1) for x in range(len(salidas[0]))])
        dfArañas = pd.DataFrame(np.array(arañas), columns=['Codigo', 'Aranea', 'ruta'])
        dfBasesRadiales = pd.DataFrame(basesRadiales, columns=['BR' + str(x+1) for x in range(len(basesRadiales[0]))])
        dfConfig = pd.DataFrame([[funcionSalida, error, neuronas]], columns=['Func Activacion', 'Error Maximo', 'Neuronas'])

        try:
            os.mkdir('src/data')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with pd.ExcelWriter('src/data/Araneae.xlsx') as writer: # pylint: disable=abstract-class-instantiated
            dfMatrix.to_excel(writer, sheet_name='Matriz', index=False)
            dfArañas.to_excel(writer, sheet_name='Araneae', index=False)
            dfBasesRadiales.to_excel(writer, sheet_name='Bases Radiales', index=False)
            dfConfig.to_excel(writer, sheet_name='Config', index=False)
            
if __name__ == '__main__':
    print(np.ones((4, 1)))