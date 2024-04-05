from sensor import Sensor
from arreglo import Arreglo

class Room(Arreglo):
    def __init__(self, id_usuario=None, nombre=None, descripcion=None,id_room=None):
        if id_usuario is None and nombre is None and descripcion is None:
            super().__init__()
            self.isarreglo = True
        else:
            self.id_usuario = id_usuario
            self.id_room = id_room
            self.nombre = nombre
            self.descripcion = descripcion
            self.sensores = Sensor()  # Mantenemos Sensor() como un Arreglo para contener múltiples sensores
            self.isarreglo = False

    def __str__(self):
        if self.isarreglo:
            result = ""
            for elemento in self.elementos:
                if isinstance(elemento, Room):
                    result += f"id_usuario:{elemento.id_usuario} - nombre:{elemento.nombre} - descripcion:{elemento.descripcion} - sensores:{elemento.sensores}\n"
            return result
        else:
            return f"id_usuario:{self.id_usuario} - nombre:{self.nombre} - descripcion:{self.descripcion} - sensores:{self.sensores}"

    def serializar(self):
        if self.isarreglo:
            result = []
            for elemento in self.elementos:
                if isinstance(elemento, Room):
                    result.append(elemento.serializar())
            return result
        else:
            return {
                "id_room": self.id_room,
                "id_usuario": self.id_usuario,
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "sensores": self.sensores.serializar()
            }

    def deserealizar(self, data):
        from dato import Data
        new_rooms = Room()
        for room in data:
            new_sensores = Sensor()
            for sensor_data in room['sensores']:
                new_sensor = Sensor(sensor_data['nombre'], sensor_data['unidad_de_medida'])
                new_dates = Arreglo()
                for dataS in sensor_data['datos']:
                    new_date = Data(dataS['fecha'], dataS['dato'])
                    new_dates.agregar_elemento(new_date)
                new_sensor.datos = new_dates
                new_sensores.agregar_elemento(new_sensor)

            new_room = Room(room['id_usuario'], room['nombre'], room['descripcion'])
            new_room.sensores = new_sensores
            new_rooms.agregar_elemento(new_room)
        return new_rooms

if __name__ == "__main__":

    from dato import Data
    rooms = Room()

    # Crear un objeto Room
    room1 = Room(1, "Sala", "Sala de estar", 1)

    # Crear un objeto Sensor
    sensor1 = Sensor("Temperatura", "°C")
    sensor2 = Sensor("Humedad", "%")
    sensor3 = Sensor("Luz", "Lux")
    sensor4 = Sensor("Magnetico", "Boolean")
    sensor5 = Sensor("Gas", "Boolean")
    sensor6 = Sensor("Voltaje", "volts")


    # Crear objetos Data
    data1 = Data("2021-10-10", 30, "10:00")
    data2 = Data("2021-10-11", 40, "11:00")
    data3 = Data("2021-10-12", 50, "12:00")
    data4 = Data("2021-10-13", 60, "13:00")
    data5 = Data("2021-10-14", 70, "14:00")
    data6 = Data("2021-10-15", 80, "15:00")
    data7 = Data("2021-10-16", 90, "16:00")
    data8 = Data("2021-10-17", 100, "17:00")
    data9 = Data("2021-10-18", 110, "18:00")
    data10 = Data("2021-10-19", 120, "19:00")
    data11 = Data("2021-10-20", 130, "20:00")
    data12 = Data("2021-10-21", 140, "21:00")
    data13 = Data("2021-10-22", 150, "22:00")
    data14 = Data("2021-10-23", 160, "23:00")
    data15 = Data("2021-10-24", 170, "24:00")
    data16 = Data("2021-10-25", 180, "25:00")
    data17 = Data("2021-10-26", 190, "26:00")
    data18 = Data("2021-10-27", 200, "27:00")
    data19 = Data("2021-10-28", 210, "28:00")
    data20 = Data("2021-10-29", 220, "29:00")


    # Agregar data alos sensores
    sensor1.datos.agregar_elemento(data1)
    sensor1.datos.agregar_elemento(data2)
    sensor1.datos.agregar_elemento(data3)
    sensor1.datos.agregar_elemento(data4)
    sensor2.datos.agregar_elemento(data5)
    sensor2.datos.agregar_elemento(data6)
    sensor2.datos.agregar_elemento(data7)
    sensor2.datos.agregar_elemento(data8)
    sensor3.datos.agregar_elemento(data9)
    sensor3.datos.agregar_elemento(data10)
    sensor3.datos.agregar_elemento(data11)
    sensor3.datos.agregar_elemento(data12)
    sensor4.datos.agregar_elemento(data13)
    sensor4.datos.agregar_elemento(data14)
    sensor4.datos.agregar_elemento(data15)
    sensor4.datos.agregar_elemento(data16)
    sensor5.datos.agregar_elemento(data17)
    sensor5.datos.agregar_elemento(data18)
    sensor5.datos.agregar_elemento(data19)
    sensor5.datos.agregar_elemento(data20)
    sensor6.datos.agregar_elemento(data1)
    sensor6.datos.agregar_elemento(data2)
    sensor6.datos.agregar_elemento(data3)


    
    

    # Agregar sensor1 al room1
    room1.sensores.agregar_elemento(sensor1)
    room1.sensores.agregar_elemento(sensor2)
    room1.sensores.agregar_elemento(sensor3)
    room1.sensores.agregar_elemento(sensor4)
    room1.sensores.agregar_elemento(sensor5)
    room1.sensores.agregar_elemento(sensor6)

    # Agregar room1 a rooms
    rooms.agregar_elemento(room1)

    print(rooms)
    print(rooms.serializar())
    print(rooms.deserealizar(rooms.serializar()))