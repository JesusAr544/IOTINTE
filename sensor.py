from dato import Data
from arreglo import Arreglo

class Sensor(Arreglo):
    def __init__(self, nombre=None, unidad_de_medida=None):
        if nombre is None and unidad_de_medida is None:
            super().__init__()
            self.isarreglo = True
        else:
            self.isarreglo = False
            self.nombre = nombre
            self.unidad_de_medida = unidad_de_medida
            self.datos = Data()

    def __str__(self):
        if self.isarreglo:
            result = ""
            for elemento in self.elementos:
                if isinstance(elemento, Sensor):
                    result += f"nombre:{elemento.nombre} - unidad_de_medida:{elemento.unidad_de_medida} - datos:{elemento.datos}\n"
            return result
        else:
            return f"{self.nombre} - {self.unidad_de_medida} - datos:{self.datos}"

    def deserealizar(self, data):
        new_sensors = Sensor()
        for sensor in data:
            new_dates = Data()
            for dataS in sensor['datos']:
                new_date = Data(dataS['dato'], dataS['datatime'])
                new_dates.agregar_elemento(new_date)

            new_sensor = Sensor(sensor['nombre'], sensor['unidad_de_medida'])
            new_sensor.datos = new_dates
            new_sensors.agregar_elemento(new_sensor)
        return new_sensors

    def serializar(self):
        if self.isarreglo:
            result = []
            for elemento in self.elementos:
                if isinstance(elemento, Sensor):
                    result.append(elemento.serializar())
            return result
        else:
            return {
                "nombre": self.nombre,
                "unidad_de_medida": self.unidad_de_medida,
                "datos": self.datos.serializar()
            }
