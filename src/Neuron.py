from numpy import linalg, append
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
        self.vsErrores = [[0.1, 0.1]]

    def Entrenar(self, error_maximo, funcionActivacion):

        distanciasEuclidianas = []
        for entradas in self.Entradas:
            distanciasEuclidianas.append(self.functions.DistanciaEuclidiana(entradas, self.BasesRadiales))

        activacion = self.functions.FuncionActivacion(funcionActivacion, distanciasEuclidianas)
        matriz = [[1], [1], [1], [1]]
        matriz = append(matriz, activacion, axis=1)
        interp = linalg.lstsq(matriz, self.Salidas, rcond=-1)[0]
        
        salidas = self.functions.CalcularSalida(matriz, interp)

        (errorLineal, entrenamiento) = self.functions.ErrorLineal(self.Salidas, salidas)

        errorG = self.functions.ErrorG(errorLineal)

        self.vsErrores.append([error_maximo, errorG])

        return (errorG <= error_maximo, entrenamiento, self.vsErrores, matriz, errorG)