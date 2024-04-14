import datetime
import json
import requests
import socket
from arreglo import Arreglo
from conexion import ConexionSocket
from sensor import Sensor
from dato import Data

class Room(Arreglo):
    def __init__(self, nombre=None, id_room=None):
        if nombre is None:
            super().__init__()
            self.isarreglo = True
            self.rooms_info = self.obtener_rooms_info()
            self.crearRoom()
        else:
            self.id_room = id_room
            self.nombre = nombre
            self.sensores = Sensor()
            self.isarreglo = False

    def obtener_rooms_info(self):
        if self.conexionA.is_conexion:
            return self.conexionA.obtener_habitaciones()
        else:
            return self.cargarRoomApi()

    def __str__(self):
        if self.isarreglo:
            result = ""
            for elemento in self.elementos:
                if isinstance(elemento, Room):
                    result += f"nombre:{elemento.nombre} - sensores:{elemento.sensores}\n"
            return result
        else:
            return f"nombre:{self.nombre} - sensores:{self.sensores}"

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
                "nombre": self.nombre,
                "sensores": self.sensores.serializar()
            }

    def deserealizar(self, data):
        new_rooms = Room()
        for room in data:
            new_sensores = Sensor()
            for sensor_data in room['sensores']:
                new_sensor = Sensor(sensor_data['nombre'], sensor_data['unidad_de_medida'])
                new_dates = Data()
                for dataS in sensor_data['datos']:
                    new_date = Data(dataS['dato'], dataS['datatime'])
                    new_dates.agregar_elemento(new_date)
                new_sensor.datos = new_dates
                new_sensores.agregar_elemento(new_sensor)
            new_room = Room(room['nombre'], room['id_room'])
            new_room.sensores = new_sensores
            new_rooms.agregar_elemento(new_room)
        return new_rooms
    
    def guardar(self):
        return super().guardar("rooms.json")

    def cargar(self):
        return super().cargar("rooms.json")

    def leer(self):
        self.conexionS.iniciar_servidor()
        while True:
            data = self.conexionS.recibir_datos()
            self.cargarDatos(data)

    def crearRoom(self):
        sensoresJ = self.cargarSensoresJson()
        roomsJ = self.cargarRoomApi()
        for room in roomsJ:
            sensores = Sensor()
            for sensor in sensoresJ:
                new_sensor = Sensor(sensor['name'], sensor['unidad_de_medida'])
                sensores.agregar_elemento(new_sensor)
            new_room = Room(room['nombre'], room['id'])
            new_room.sensores = sensores
            sensores = Sensor()
            self.agregar_elemento(new_room)

    def cargarDatos(self, dataS):
        for room in self.elementos:
            for sensor in room.sensores.elementos:
                for sensor_data in dataS:
                    if sensor.nombre == sensor_data['name']:
                        new_date = Data(sensor_data['valor'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        sensor.datos.agregar_elemento(new_date)
                        break
        self.guardarDatos()

    def guardarDatos(self):
        if self.conexionA.is_conexion:
            for room in self.elementos:
                for sensor in room.sensores.elementos:
                    for data in sensor.datos.elementos:
                        self.conexionA.guardar_datos_habitacion(sensor.nombre, data.dato, room.id_room, data.datatime)
                sensor.datos.elementos = []
                print(self.GuardoDatos)
            if self.GuardoDatos:
                datosg = Room()
                datosg.deserealizar(datosg.cargar())
                json_data = []
                for room in self.elementos:
                    for sensor in room.sensores.elementos:
                        for data in sensor.datos.elementos:
                            json = {
                                "name": sensor.nombre,
                                "data": data.dato,
                                "room_id": room.id_room,
                                "date_time": data.datatime
                            }
                            json_data.append(json)
                print(json_data)
                datosg.conexionM.guardar_datos_many(json_data)
                datosg.elementos = []
        else:
            self.conexionA.is_conexion = self.conexionA.is_conexion_valida()
            self.guardar()

if __name__ == "__main__":
    room = Room()
    room.leer()
