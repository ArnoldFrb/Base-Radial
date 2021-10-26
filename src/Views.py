import random as rn
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Funtions import *
from Neuron import Neuron

class Views:

    def __init__(self, window):
        self.wind = window
        self.wind.title("PERCEPTRON MULTICAPA")
        self.wind.resizable(0,0)
        self.wind.geometry("1100x600")
        self.wind.winfo_screenheight()
        self.wind.winfo_screenwidth()
        self.capas = []
        self.capa = 1
        self.config = Funtions()

        frameMain = tk.Frame(master=self.wind, width=1100, height=600, background="#e3e3e3")
        frameMain.place(relx=.0, rely=.0)

        self.frameConfig = tk.Frame(frameMain, width=450, height=50, background="#fafafa")
        self.frameConfig.place(relx=.01, rely=.02)

        # FRAME PARA VISUALIZAR LA CONFIGURACION DE LA NEURONAL
        tk.Label(self.frameConfig, text="CONFIGURAR NEURONA", bg="#fafafa").place(relx=.01, rely=.001)

        self.btnData = tk.Button(self.frameConfig, text="Cargar Data", command= self.Event_btnData,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnData.place(relx=.01, rely=.4)

        tk.Label(self.frameConfig, text="ERROR:", bg="#fafafa").place(relx=.218, rely=.5)
        self.entErrorMaximo = tk.Entry(self.frameConfig, width=8)
        self.entErrorMaximo.place(relx=.32, rely=.5)
        self.entErrorMaximo.insert(0,0.001)

        tk.Label(self.frameConfig, text="NEURONAS:", bg="#fafafa").place(relx=.45, rely=.5)
        self.entNeuronas = tk.Entry(self.frameConfig, width=8)
        self.entNeuronas.place(relx=.61, rely=.5)
        self.entNeuronas.insert(0, 0)

        self.btnInicializar = tk.Button(self.frameConfig, text="Inicializar", state=tk.DISABLED, command= self.Event_btnInicializar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnInicializar.place(relx=.75, rely=.4)

        # FRAME PARA VISUALIZAR ENTRADAS, SALIDAS Y PATRONES
        self.frameConfigInicial = tk.Frame(frameMain, width=450, height=60, background="#fafafa")
        self.frameConfigInicial.place(relx=.01, rely=.115)

        tk.Label(self.frameConfigInicial, text="CONFIG ENTRENAMIENTO", bg="#fafafa").place(relx=.34, rely=.01)
        tk.Label(self.frameConfigInicial, text="ENTRADAS", bg="#fafafa").place(relx=.01, rely=.35)
        tk.Label(self.frameConfigInicial, text="SALIDAS", bg="#fafafa").place(relx=.21, rely=.35)
        tk.Label(self.frameConfigInicial, text="PATRONES", bg="#fafafa").place(relx=.4, rely=.35)

        self.cobBoxFuncionSalida = ttk.Combobox(self.frameConfigInicial)
        self.cobBoxFuncionSalida["values"] = ['BASE RADIAL', 'GAUSSIANA', 'MULTICUADRATICA', 'MC INVERSA']
        self.cobBoxFuncionSalida.place(relx=.63, rely=.35)
        self.cobBoxFuncionSalida.insert(0, "BASE RADIAL")

        # FRAME PARA VISUALIZAR LA MATRIZ DE DATOS
        self.frameData = tk.Frame(frameMain, background="#fafafa")
        self.frameData.place(relx=.01, rely=.227, width=450, height=194)

        # FRAME PARA CONFIGURACION DE LA SIMULACION
        self.frameConfigSimulacion = tk.Frame(frameMain, width=450, height=249, background="#fafafa")
        self.frameConfigSimulacion.place(relx=.01, rely=.564)

        tk.Label(self.frameConfigSimulacion, text="SIMULACION", bg="#fafafa").place(relx=.02, rely=.01)

        self.btnDataSimulacion = tk.Button(self.frameConfigSimulacion, text="Cargar Data", state=tk.DISABLED, command= self.Event_btnData,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnDataSimulacion.place(relx=.70, rely=.01)

        self.btnSimular = tk.Button(self.frameConfigSimulacion, text="Simular", state=tk.DISABLED, command= self.Event_btnData,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnSimular.place(relx=.875, rely=.01)

        self.frameSimulacionTabla = tk.Frame(self.frameConfigSimulacion, width=450, height=219, background="#fafafa")
        self.frameSimulacionTabla.place(relx=0, rely=.12)

        self.frameEntrenar = tk.Frame(frameMain, width=620, height=50, background="#fafafa")
        self.frameEntrenar.place(relx=.426, rely=.02)

        self.btnEntrenar = tk.Button(self.frameEntrenar, text="Entrenar", state=tk.DISABLED, command= self.Event_btnEntrenar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnEntrenar.place(relx=.01, rely=.4)

        self.btnDetener = tk.Button(self.frameEntrenar, text="Detener", state=tk.DISABLED, command= self.Event_btnDetener,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2, border=0)
        self.btnDetener.place(relx=.92, rely=.035)

        self.btnLimpiar = tk.Button(self.frameEntrenar, text="Limpiar", state=tk.DISABLED, command= self.Event_btnLimpiar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2, border=0)
        self.btnLimpiar.place(relx=.92, rely=.515)

        self.frameEntranamiento = tk.Frame(frameMain, width=620, height=228, background="#fafafa")
        self.frameEntranamiento.place(relx=.426, rely=.115)

        self.frameSimulacion = tk.Frame(frameMain, width=620, height=283, background="#fafafa")
        self.frameSimulacion.place(relx=.426, rely=.506)

    def Event_btnData(self):
        
        (ejercicio, matrix, entradas, salidas, basesRadiales, funcionActivacion, neuronas, error) = self.config.Leer_Datos(filedialog.askopenfilename())

        self.entErrorMaximo.delete(0, tk.END)
        self.entErrorMaximo.insert(0, error)
        self.entNeuronas.delete(0, tk.END)
        self.entNeuronas.insert(0, neuronas)
        self.cobBoxFuncionSalida.delete(0, tk.END)
        self.cobBoxFuncionSalida.insert(0, funcionActivacion)

        treeView = ttk.Treeview(self.frameData)
        self.CrearGrid(treeView, self.frameData)
        self.LlenarTabla(treeView, matrix)

        tk.Label(self.frameConfigInicial, text=str(len(entradas[0])), bg="#fafafa").place(relx=.15, rely=.35)
        tk.Label(self.frameConfigInicial, text=str(len(salidas[0])), bg="#fafafa").place(relx=.323, rely=.35)
        tk.Label(self.frameConfigInicial, text=str(len(matrix)), bg="#fafafa").place(relx=.54, rely=.35)

        self.entrenar = Neuron(ejercicio, entradas, salidas, basesRadiales)
        if len(basesRadiales) == 0:
            self.btnInicializar['state'] = tk.NORMAL
        else:
            self.btnEntrenar['state'] = tk.NORMAL

    def Event_btnInicializar(self):
        self.entrenar.BasesRadiales = self.config.GenerarBasesRadiales(
            self.entrenar.Entradas.min(),
            self.entrenar.Entradas.max(),
            int(self.entNeuronas.get()),
            len(self.entrenar.Entradas[0])
            )
        self.btnEntrenar['state'] = tk.NORMAL

    def Event_btnEntrenar(self):
        self.btnData['state'] = tk.DISABLED
        self.btnInicializar['state'] = tk.DISABLED
        self.btnEntrenar['state'] = tk.DISABLED
        self.btnDetener['state'] = tk.NORMAL
        self.btnLimpiar['state'] = tk.DISABLED

        self.entrenar.Entrenar(float(self.entErrorMaximo.get()), self.cobBoxFuncionSalida.get(), self.frameEntrenar)
        # self.Graficar(self.frameEntranamiento, grafica)
        
        self.btnLimpiar['state'] = tk.NORMAL
        self.btnDetener['state'] = tk.DISABLED

    def Event_btnDetener(self):
        self.entrenar.flag = True

    def Event_btnLimpiar(self):
        self.entrenar.BasesRadiales = []
        self.btnLimpiar['state'] = tk.DISABLED
        self.btnData['state'] = tk.NORMAL
        self.btnInicializar['state'] = tk.NORMAL

    def LlenarTabla(self, treeView, Matriz):
        treeView.delete(*treeView.get_children())
        treeView["column"] = list(Matriz.columns)
        treeView["show"] = "headings"

        for column in treeView["columns"]:
            treeView.column(column=column, width=10, anchor='center')
            treeView.heading(column=column, text=column)

        Matriz_rows1 = Matriz.to_numpy().tolist()
        for row in Matriz_rows1:
            treeView.insert("", "end", values=row)

    def CrearGrid(self, treeView, frame):
        style = ttk.Style(frame)
        style.configure(treeView, rowheight=100, highlightthickness=0, bd=0)  
        treeView.place(relheight=1, relwidth=1)

    def Graficar(self, frame, data):
        fig = Figure(figsize=(5, 4), dpi=100)
        if np.array(data).ndim == 2:
            fig.add_subplot(111).plot([fila[0] for fila in data], 'o', [fila[1] for fila in data], '^')
        else:
            fig.add_subplot(111).plot(data, 'o')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(relwidth=1, relheight=1)

if __name__ == '__main__':
    winw = tk.Tk()
    Views(winw)
    winw.mainloop()