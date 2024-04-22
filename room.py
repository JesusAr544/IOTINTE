import datetime
from arreglo import Arreglo
from sensor import Sensor
from dato import Data
import threading

class Room(Arreglo):
    def __init__(self, nombre=None, id_room=None):
        if nombre is None:
            super().__init__()
            self.isarreglo = True
            self.rooms_info = []
            self.GuardoDatos = False 
            self.alarma = False
        else:
            self.id_room = id_room
            self.nombre = nombre
            self.sensores = Sensor()
            self.isarreglo = False

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

    def cargar_rooms(self):
        return super().cargar_rooms("rooms.json")

    def leer(self):
        self.conexionS.iniciar_servidor()
        while True:
            data = self.conexionS.recibir_datos()
            self.cargarDatos(data)

    def obtener_rooms_info(self):
        self.conexionA.is_connection_valid()
        if self.conexionA.is_conexion:
            print("Obteniendo rooms info")
            self.rooms_info = self.conexionA.get_rooms()
        else:
            self.rooms_info = self.cargarRoomApi()
        self.crearRoom()

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
                    if sensor_data['name'] == "Temperatura" and sensor_data['valor'] > "33":
                            if not self.alarma:
                                for rooms in self.elementos:
                                    self.conexionA.encender_alarma(rooms.id_room)
                                self.conexionA.save_notificacion(room.id_room, "media", "Temperatura fuera de rango")
                                self.alarma = True
                    if sensor_data['name'] == "Humedad" and sensor_data['valor'] > "80":
                            if not self.alarma:
                                self.conexionA.save_notificacion(room.id_room, "media", "Humedad fuera de rango")    
                                self.alarma = True
                    if sensor_data['name'] == "FotoResistencia" and sensor_data['valor'] > 1:
                            if not self.alarma:
                                self.conexionA.save_notificacion(room.id_room, "media", "Luz fuera de rango")
                                self.alarma = True
                    if sensor_data['name'] == "Voltaje" and sensor_data['valor'] == 5:
                            if not self.alarma:
                                self.conexionA.save_notificacion(room.id_room, "media", "Movimiento detectado")
                                self.alarma = True
                    if sensor_data['name'] == "Infrarrojo" and sensor_data['valor'] == 1:
                            if not self.alarma:
                                self.conexionA.save_notificacion(room.id_room, "media", "Movimiento detectado")    
                                self.alarma = True
                    if sensor_data['name'] == "Magnetico" and sensor_data['valor'] == 1:
                            if not self.alarma:
                                self.conexionA.save_notificacion(room.id_room, "media", "Se abrio la puerta")    
                                self.alarma = True
                    if sensor_data['name'] == "Humo" and sensor_data['valor'] == "Gas Detectado":
                            if not self.alarma:
                                self.conexionA.save_notificacion(room.id_room, "media", "Gas detectado")
                                self.alarma = True
    
                    if sensor.nombre == sensor_data['name']:
                        new_date = Data(sensor_data['valor'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        sensor.datos.agregar_elemento(new_date)
                        break





        self.alarma = False
        self.guardarDatos()

    

    def guardarDatos(self):
        from conexion import conexionSocketEnviar
        if not self.conexionM.isconexion:
            self.conexionM.conectar()
            self.guardar()
            self.GuardoDatos = True
            self.elementos = []
            self.obtener_rooms_info()
            return
        
        es = self.conexionA.estado_sensor()
        if es['status']:
            self.conexionA.apagar_alarma(es['habitaciones'])
            socket = conexionSocketEnviar()
            socket.conectar_servidor()
            socket.enviar_datos()

        

        json_datas = []
        for room in self.elementos:
            for sensor in room.sensores.elementos:
                for data in sensor.datos.elementos:
                    json_data = {
                        "name": sensor.nombre,
                        "data": data.dato,
                        "room_id": room.id_room,
                        "date_time": data.datatime
                    }
                    json_datas.append(json_data)
                    print(json_data)
                if self.conexionM.isconexion:
                    sensor.datos.elementos = []
        if self.conexionM.isconexion:
            print("Guardando datos")
            self.conexionM.guardar_datos_many(json_datas)
        else:
            self.conexionM.conectar()
            self.guardar()
            self.GuardoDatos = True
                
                        
        if self.GuardoDatos:
            if self.conexionM.isconexion:
                self.guardar_Datos_Mongo()
                self.GuardoDatos = False
            else:
                self.conexionM.conectar()
                

    def guardar_Datos_Mongo(self):
        data = Room()
        data = data.deserealizar(data.cargar_rooms())
        json_data = []
        for room in data.elementos:
            for sensor in room.sensores.elementos:
                for data in sensor.datos.elementos:
                    json = {
                        "name": sensor.nombre,
                        "data": data.dato,
                        "room_id": room.id_room,
                        "date_time": data.datatime
                    }
                    json_data.append(json)
        data = Room()
        data.guardar()
        self.conexionM.guardar_datos_many(json_data)

if __name__ == "__main__":
    from room import Room
    room = Room()
    room.obtener_rooms_info()
    room.conexionM.conectar()
    room.leer()