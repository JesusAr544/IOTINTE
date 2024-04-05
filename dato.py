from arreglo import Arreglo


class Data(Arreglo):
    def __init__(self, fecha=None, dato=None, hora=None):
        if fecha is None and dato is None:
           super().__init__()
           self.isarreglo = True
        else:
            self.isarreglo = False
            self.fecha = fecha
            self.dato = dato
            self.hora = hora

    def __str__(self) -> str:
        if self.isarreglo:
            result = ""
            for elemento in self.elementos:
                if isinstance(elemento, Data):
                    result += f"{elemento.fecha} - {elemento.dato} - {elemento.hora}\n"
            return "["+result+"]"
        else:
            return f"{self.fecha} - {self.dato} - {self.hora}"




    def serializar(self):
        if self.isarreglo:
            result = []
            for elemento in self.elementos:
                if isinstance(elemento, Data):
                    result.append(elemento.serializar())
            return result
        else:
            return {
                "fecha": self.fecha,
                "dato": self.dato,
                "hora": self.hora
            }
    
    def deserealizar(self, datas):
        new_datas = Data()
        for data in datas:
            new_data = Data(data['fecha'], data['dato'], data['hora'])
            new_datas.agregar_elemento(new_data)
        return new_datas
        
    


if __name__ == "__main__":

    ping = Data()


    dato1 = Data("2021-10-10", 100, "10:00")
    dato2 = Data("2021-10-11", 200, "11:00")
   
    ping.agregar_elemento(dato1)
    ping.agregar_elemento(dato2)

    print(ping)

    ping.eliminar_elemento(dato1)

    ping_serializado = ping.serializar()

    print(ping_serializado)





