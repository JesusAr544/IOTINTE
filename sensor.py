from dato import Data
from arreglo import Arreglo

class Sensor(Arreglo):
    def __init__(self,nombre = None, unidad_de_medida = None):
        if nombre is None and unidad_de_medida is None:
            super().__init__()
            self.isarreglo = True
        else:
            self.isarreglo = False
            self.nombre = nombre
            self.unidad_de_medida = unidad_de_medida
            self.datos = Data()

    def __str__(self) -> str:
        if self.isarreglo:
            result = ""
            for elemento in self.elementos:
                if isinstance(elemento, Sensor):
                    result += f"nombre:{elemento.nombre} - unidad_de_medida:{elemento.unidad_de_medida} - datos:{elemento.datos}\n"
            return result
        else:
            return f"{self.nombre} - {self.unidad_de_medida} - datos:{elemento.datos}"
        
    def deserealizar(self, data):
        new_sensors = Sensor()
        for sensor in data:
            new_dates = Data()
            for dataS in sensor['datos']:
                new_date = Data(dataS['fecha'], dataS['dato'])
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
    


if __name__ == "__main__":
    sensores = Sensor()


    # Crear un objeto Sensor
    sensor1 = Sensor("Temperatura", "°C")

    # Crear algunos datos para el sensor
    new_Datas = Data()
    new_Data = Data("2024-04-01", 25, "10:00")
    new_Datas.agregar_elemento(new_Data)
    new_Data = Data("2024-04-02", 27, "11:00")
    new_Datas.agregar_elemento(new_Data)
    new_Data = Data("2024-04-03", 23, "12:00")
    new_Datas.agregar_elemento(new_Data) 
   
    # Agregar los datos al sensor
    sensor1.datos = new_Datas

    # Agregar el sensor al arreglo de sensores
    sensores.agregar_elemento(sensor1)



    # Imprimir el objeto sensor
    print("Sensores:")
    print(sensores)

    # Serializar el objeto sensor
    sensores_serializado = sensores.serializar()

    print("Sensor 1 serializado:")
    print(sensores_serializado)
    print()

    # Deserializar el objeto sensor
    sensor2 = Sensor()
    sensor2 = sensor2.deserealizar(sensores_serializado)
    

    # Imprimir el objeto sensor deserializado
    print("Sensor 2 (deserializado desde Sensor 1):")
    print(sensor2)
