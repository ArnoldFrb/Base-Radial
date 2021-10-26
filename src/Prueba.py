# METODO PARA OBTENER LA FUNCION ESCALON DE HEAVISIDE
def FunciónEscalonHeaviside(salidaSoma):
    yr = []
    for x in salidaSoma:
        yr.append(1 if x >= 0 else 0)
    return yr


# METODO PARA OBTENER LA FUNCION RAMPA
def FuncionRampa(self, salidaSoma, entrada, rampa):
    yr = []
    for x in salidaSoma:
        yr.append(-1 if x < -1 else 1 if x >
                  1 else entrada if rampa else x)
    return yr


# METODO PARA OBTENER LA FUNCION LINEAL
def FuncionLineal(self, salidaSoma):
    yr = salidaSoma
    return yr


# METODO PARA OBTENER LA FUNCION SIGNO
def FuncionSigno(self, salidaSoma):
    yr = []
    for x in salidaSoma:
        yr.append(-1 if x < 0 else 1 if x > 0 else 0)


def FuncionSalida(self, funcionSalida, salidaSoma, entrada, rampa):
    switcher = {
        'ESCALON': self.FunciónEscalonHeaviside(salidaSoma),
        'LINEAL': self.FuncionLineal(salidaSoma),
        'SIGMOIDE': self.FuncionSigmoide(salidaSoma),
        'RAMPA': self.FuncionRampa(salidaSoma, entrada, rampa)
    }
    return switcher.get(funcionSalida, "ERROR")

# Tener en cuenta que hay dos algoritmos de entrenamiento regla delta y regla delta modificada
