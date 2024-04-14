from arreglo import Arreglo

class Data(Arreglo):
    def __init__(self, dato=None, datatime=None):
        if dato is None and datatime is None:
            super().__init__()
            self.isarreglo = True
        else:
            self.isarreglo = False
            self.dato = dato
            self.datatime = datatime

    def __str__(self):
        if self.isarreglo:
            result = ""
            for elemento in self.elementos:
                if isinstance(elemento, Data):
                    result += f" {elemento.dato} - {elemento.datatime}\n"
            return "[" + result + "]"
        else:
            return f"{self.dato} - {self.datatime}"

    def serializar(self):
        if self.isarreglo:
            result = []
            for elemento in self.elementos:
                if isinstance(elemento, Data):
                    result.append(elemento.serializar())
            return result
        else:
            return {
                "dato": self.dato,
                "datatime": self.datatime
            }

    def deserealizar(self, datas):
        new_datas = Data()
        for data in datas:
            new_data = Data(data['dato'], data['datatime'])
            new_datas.agregar_elemento(new_data)
        return new_datas
