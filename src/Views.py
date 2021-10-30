import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas.core.frame import DataFrame
from Funtions import *
from Neuron import Neuron
from tkinter import messagebox as MessageBox

class Views:

    def __init__(self, window):
        self.wind = window
        self.wind.title("BASE RADIAL")
        self.wind.resizable(0,0)
        self.wind.geometry("1100x600")
        self.wind.winfo_screenheight()
        self.wind.winfo_screenwidth()
        self.capas = []
        self.capa = 1
        self.config = Funtions()

        self.frameMain = tk.Frame(master=self.wind, width=1100, height=600, background="#e3e3e3")
        self.frameMain.place(relx=.0, rely=.0)

        self.frameConfig = tk.Frame(self.frameMain, width=450, height=50, background="#fafafa")
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
        self.frameConfigInicial = tk.Frame(self.frameMain, width=450, height=60, background="#fafafa")
        self.frameConfigInicial.place(relx=.01, rely=.115)

        tk.Label(self.frameConfigInicial, text="CONFIG ENTRENAMIENTO", bg="#fafafa").place(relx=.34, rely=.01)
        tk.Label(self.frameConfigInicial, text="ENTRADAS", bg="#fafafa").place(relx=.01, rely=.35)
        tk.Label(self.frameConfigInicial, text="SALIDAS", bg="#fafafa").place(relx=.21, rely=.35)
        tk.Label(self.frameConfigInicial, text="PATRONES", bg="#fafafa").place(relx=.4, rely=.35)

        self.cobBoxFuncionSalida = ttk.Combobox(self.frameConfigInicial)
        self.cobBoxFuncionSalida["values"] = ['BASERADIAL', 'GAUSSIANA', 'MULTICUADRATICA', 'MC_INVERSA']
        self.cobBoxFuncionSalida.place(relx=.63, rely=.35)
        self.cobBoxFuncionSalida.insert(0, "BASERADIAL")

        # FRAME PARA VISUALIZAR LA MATRIZ DE DATOS
        self.frameData = tk.Frame(self.frameMain, background="#fafafa")
        self.frameData.place(relx=.01, rely=.227, width=450, height=194)

        # FRAME PARA CONFIGURACION DE LA SIMULACION
        self.frameConfigSimulacion = tk.Frame(self.frameMain, width=450, height=249, background="#fafafa")
        self.frameConfigSimulacion.place(relx=.01, rely=.564)

        tk.Label(self.frameConfigSimulacion, text="BASES RADIALES", bg="#fafafa").place(relx=.01, rely=.01)

        self.frameBasesRadiales = tk.Frame(self.frameConfigSimulacion, width=450, height=100, background="#fafafa")
        self.frameBasesRadiales.place(relx=0, rely=.09)

        tk.Label(self.frameConfigSimulacion, text="MATRIZ INTERPOLACION", bg="#fafafa").place(relx=.01, rely=.51)

        self.frameSimulacionMatriz_1 = tk.Frame(self.frameConfigSimulacion, width=320, height=100, background="#fafafa")
        self.frameSimulacionMatriz_1.place(relx=0, rely=.6)

        self.frameSimulacionMatriz_2 = tk.Frame(self.frameConfigSimulacion, width=119, height=100, background="#fafafa")
        self.frameSimulacionMatriz_2.place(relx=.735, rely=.6)

        self.frameEntrenar = tk.Frame(self.frameMain, width=620, height=50, background="#fafafa")
        self.frameEntrenar.place(relx=.426, rely=.02)

        self.frameBarra = tk.Frame(self.frameEntrenar, width=470, height=50, background="#fafafa")
        self.frameBarra.place(relx=.15, rely=0)
        self.barra = ttk.Progressbar(self.frameBarra, mode="indeterminate")
        self.barra.place(relx=.01, rely=.05, width=460)

        self.lblNeuronas = tk.StringVar(value='Neuronas: 0')
        lbNeuronas = tk.Label(self.frameBarra, bg="#fafafa")
        lbNeuronas.place(relx=.15, rely=.6)
        lbNeuronas.config(textvariable=self.lblNeuronas)
        
        self.lblErrorG = tk.StringVar(value='Error G: 0')
        lberrorG = tk.Label(self.frameBarra, bg="#fafafa")
        lberrorG.place(relx=.65, rely=.6)
        lberrorG.config(textvariable=self.lblErrorG)

        self.btnEntrenar = tk.Button(self.frameEntrenar, text="Entrenar", state=tk.DISABLED, command= self.Event_btnEntrenar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnEntrenar.place(relx=.01, rely=.4)

        self.btnGuardar = tk.Button(self.frameEntrenar, text="Guardar", state=tk.DISABLED, command= self.Event_btnGuardar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2, border=0)
        self.btnGuardar.place(relx=.92, rely=.035)

        self.btnLimpiar = tk.Button(self.frameEntrenar, text="Limpiar", state=tk.DISABLED, command= self.Event_btnLimpiar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2, border=0)
        self.btnLimpiar.place(relx=.92, rely=.515)

        self.frameEntranamiento = tk.Frame(self.frameMain, width=620, height=228, background="#fafafa")
        self.frameEntranamiento.place(relx=.426, rely=.115)

        self.frameEntranamientoGrafica = tk.Frame(self.frameEntranamiento, width=450, height=228, background="#fafafa")
        self.frameEntranamientoGrafica.place(relx=0, rely=0)

        tk.Label(self.frameEntranamiento, text="YD VS YR", bg="#fafafa").place(relx=.825, rely=.01)

        self.frameEntranamientoTabla = tk.Frame(self.frameEntranamiento, width=161, height=205, background="#fafafa")
        self.frameEntranamientoTabla.place(relx=.74, rely=.1)

        self.frameSimulacion = tk.Frame(self.frameMain, width=620, height=283, background="#fafafa")
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
        self.entrenar.BasesRadiales = self.config.GenerarBasesRadiales(self.entrenar.Entradas.min(),
            self.entrenar.Entradas.max(), int(self.entNeuronas.get()), len(self.entrenar.Entradas[0]))
        
        treeView = ttk.Treeview(self.frameBasesRadiales)
        self.CrearGrid(treeView, self.frameBasesRadiales)
        self.LlenarTabla(treeView, DataFrame(self.entrenar.BasesRadiales, columns=['X' + str(x+1) for x in range(len(self.entrenar.BasesRadiales[0]))]))
        
        self.btnEntrenar['state'] = tk.NORMAL
        self.btnData['state'] = tk.DISABLED
        self.btnInicializar['state'] = tk.DISABLED

    def Event_btnEntrenar(self):

        self.barra.start()
        self.btnData['state'] = tk.DISABLED
        self.btnEntrenar['state'] = tk.DISABLED
        self.btnLimpiar['state'] = tk.DISABLED

        (flag, entrenamiento, vsErrores, interp, errorG) = self.entrenar.Entrenar(float(self.entErrorMaximo.get()), self.cobBoxFuncionSalida.get())

        treeView = ttk.Treeview(self.frameSimulacionMatriz_1)
        self.CrearGrid(treeView, self.frameSimulacionMatriz_1)
        self.LlenarTabla(treeView, DataFrame(interp, columns=['X0'] + ['FA' + str(i+1) for i in range(len(interp[0]) - 1)]))

        treeView = ttk.Treeview(self.frameSimulacionMatriz_2)
        self.CrearGrid(treeView, self.frameSimulacionMatriz_2)
        self.LlenarTabla(treeView, DataFrame(self.entrenar.Salidas, columns=['YD' + str(i+1) for i in range(len(self.entrenar.Salidas[0]))]))

        self.lblNeuronas.set('Neuronas: ' + str(len(self.entrenar.BasesRadiales)))
        self.lblErrorG.set('Error G: 0' + str(round(errorG, 7)))

        self.Graficar(self.frameEntranamientoGrafica, entrenamiento)

        treeView = ttk.Treeview(self.frameEntranamientoTabla)
        self.CrearGrid(treeView, self.frameEntranamientoTabla)
        self.LlenarTabla(treeView, pd.DataFrame(entrenamiento, columns=['YD', 'YR']))

        self.Graficar(self.frameSimulacion, vsErrores, False)
        
        self.barra.stop()

        self.btnInicializar['state'] = tk.NORMAL

        if flag:
            MessageBox.showinfo('EXITO!!!', 'Entrenamiento Exitoso.')
            self.btnInicializar['state'] = tk.DISABLED
            self.btnGuardar['state'] = tk.NORMAL
        else:
            MessageBox.showinfo('ERROR!!!', 'Entrenamiento Fallido.')
            self.entNeuronas.insert(0, int(self.entNeuronas.get()) + 1)
            self.entNeuronas.delete(1, tk.END)
            self.btnInicializar['state'] = tk.NORMAL
        
        self.btnLimpiar['state'] = tk.NORMAL

    def Event_btnGuardar(self):
        if MessageBox.askokcancel("Entramiento Exitoso.", "¿Desea guardar el entrenamiento?"):
            self.config.GuardarResultados(self.entrenar.Ejercicio, 'out', self.entrenar.Entradas, self.entrenar.Salidas, 
                                    self.entrenar.BasesRadiales, self.cobBoxFuncionSalida.get(), self.entErrorMaximo.get(), self.entNeuronas.get()
                                )
            MessageBox.showinfo('EXITO!', 'Se ha guardado el entranmiento sastifactoriamente.')
        
        self.btnGuardar['state'] = tk.DISABLED

    def Event_btnLimpiar(self):
        self.btnGuardar['state'] = tk.DISABLED
        self.entrenar.BasesRadiales = []
        self.entrenar.vsErrores = [[0.1, 0.1]]
        self.btnLimpiar['state'] = tk.DISABLED
        self.btnData['state'] = tk.NORMAL
        self.btnInicializar['state'] = tk.NORMAL

        self.frameBasesRadiales = tk.Frame(self.frameConfigSimulacion, width=450, height=100, background="#fafafa")
        self.frameBasesRadiales.place(relx=0, rely=.09)

        self.frameSimulacionMatriz_1 = tk.Frame(self.frameConfigSimulacion, width=320, height=100, background="#fafafa")
        self.frameSimulacionMatriz_1.place(relx=0, rely=.6)

        self.frameSimulacionMatriz_2 = tk.Frame(self.frameConfigSimulacion, width=119, height=100, background="#fafafa")
        self.frameSimulacionMatriz_2.place(relx=.735, rely=.6)

        self.frameEntranamientoGrafica = tk.Frame(self.frameEntranamiento, width=450, height=228, background="#fafafa")
        self.frameEntranamientoGrafica.place(relx=0, rely=0)

        self.frameEntranamientoTabla = tk.Frame(self.frameEntranamiento, width=161, height=205, background="#fafafa")
        self.frameEntranamientoTabla.place(relx=.74, rely=.1)

        self.frameSimulacion = tk.Frame(self.frameMain, width=620, height=283, background="#fafafa")
        self.frameSimulacion.place(relx=.426, rely=.506)

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

    def Graficar(self, frame, data, flag=True):
        fig = Figure(figsize=(5, 4), dpi=100)
        if flag:
            fig.add_subplot(111).plot([fila[0] for fila in data], 'o', [fila[1] for fila in data], '^')
        else:
            fig.add_subplot(111).plot([fila[0] for fila in data], '-',  [fila[1] for fila in data], '--')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(relwidth=1, relheight=1)

if __name__ == '__main__':
    winw = tk.Tk()
    Views(winw)
    winw.mainloop()