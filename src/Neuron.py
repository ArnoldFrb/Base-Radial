from numpy import linalg, append, ones
from pandas.core.frame import DataFrame
from Funtions import Funtions
import tkinter as tk
import tkinter.ttk as ttk

class Neuron:

    # CONSTRUCTOR
    def __init__(self, ejercicio, entradas, salidas, basesRadiales):
        self.functions = Funtions()
        self.Ejercicio = ejercicio
        self.Entradas = entradas
        self.Salidas = salidas
        self.BasesRadiales = basesRadiales
        self.vsErrores = []

    def Entrenar(self, error_maximo, funcionActivacion):

        # CALCULO DE LA DISTANCIA EUCLIDIANA
        distanciasEuclidianas = []
        for entradas in self.Entradas:
            distanciasEuclidianas.append(self.functions.DistanciaEuclidiana(entradas, self.BasesRadiales))

        # CALCULO DE LA FUNCION DE ACTIVACION
        fa = self.functions.FuncionActivacion(funcionActivacion, distanciasEuclidianas)
        
        # MATRIZ DE INTERPOLACION
        matriz = append(ones((len(fa), 1)), fa, axis=1)
        interp = linalg.lstsq(matriz, self.Salidas, rcond=-1)[0]
        
        # ECUACION DE BASE RADIAL
        salidas = self.functions.EcuacionBaseRadial(matriz, interp)
        
        # ERROR LINEAL
        (errorLineal, entrenamiento) = self.functions.ErrorLineal(self.Salidas, salidas)

        # ERROR GENERAL DEL ENTRANMIENTO
        errorGeneral = self.functions.ErrorG(errorLineal)

        # MATRIZ DE SALIDAS YD & YR
        self.vsErrores.append([error_maximo, errorGeneral])

        return (errorGeneral <= error_maximo, entrenamiento, self.vsErrores, matriz, errorGeneral)