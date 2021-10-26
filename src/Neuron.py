from numpy import array, zeros
from copy import deepcopy
from Funtions import Funtions
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox as MessageBox
import tkinter.ttk as ttk

class Neuron:

    # CONSTRUCTOR
    def __init__(self, ejercicio, entradas, salidas, basesRadiales):
        self.functions = Funtions()
        self.Ejercicio = ejercicio
        self.Entradas = entradas
        self.Salidas = salidas
        self.BasesRadiales = basesRadiales

    def Entrenar(self, error_maximo, funcionSalida, frame):

        ###################################
        frameBarra = tk.Frame(frame, width=470, height=50, background="#fafafa")
        frameBarra.place(relx=.15, rely=0)
        barra = ttk.Progressbar(frameBarra, maximum=100)
        barra.place(relx=.01, rely=.05, width=460)
        #####################################

        return