import datetime
from arreglo import Arreglo
from sensor import Sensor
from dato import Data


class Room(Arreglo):
    def __init__(self, nombre=None, id_room=None):
        if nombre is None:
            super().__init__()
            self.isarreglo = True
            self.rooms_info = []
            self.GuardoDatos = False 
            self.enviarnotificacionhumo = False 
            
            
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
       
        if  self.conexionA.is_connection_valid():
            print("Obteniendo rooms info")
            self.rooms_info = self.conexionA.get_rooms()
        else:
            self.rooms_info = self.cargarRoomApi()
        self.crearRoom()

    def crearRoom(self):
            sensoresJ = self.cargarSensoresJson()
            roomsJ = self.rooms_info
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
                    if sensor_data['name'] == "Humo":
                        self.notificar(room.id_room, sensor_data['name'], sensor_data['valor'])         
                    if sensor.nombre == sensor_data['name']:
                        new_date = Data(sensor_data['valor'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        sensor.datos.agregar_elemento(new_date)
                        break
    
        self.guardarDatos()


    def notificar(self, room_id, sensorname, sensor_data):
        
        if sensorname == "Humo" and sensor_data == "Gas Detectado":
                    print("Se detecto gas en la habitacion")
                    print( self.enviarnotificacionhumo)
                    if self.enviarnotificacionhumo == False:
                        print("Se envia notificacion de gas detectado")
                        self.conexionA.save_notificacion(room_id, "alta", "Gas detectado en la habitacion")
                        self.enviarnotificacionhumo = True
        else:
            if self.enviarnotificacionhumo == False:
                print("no se detecto gas en la habitacion")
            else:
                    print("Se envia notificacion de gas detectado")
                    self.enviarnotificacionhumo = False
                        
                    
                

            
    
    def ApagarAlarmaSp32(self):
        from conexion import conexionSocketEnviar
        socket = conexionSocketEnviar()
        socket.conectar_servidor()
        socket.enviar_datos()

    def guardarDatos(self):
        
        if not self.conexionM.isconexion:
            self.conexionM.conectar()
            self.guardar()
            self.GuardoDatos = True
            return
        
        es = self.conexionA.estado_sensor()
        
        if es['status']:
                self.enviarnotificacionhumo = False
                self.ApagarAlarmaSp32()
                self.conexionA.apagar_alarma(es['habitaciones'])
            
            
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
        if self.conexionM.isconexion:
            print("Guardando datos")
            res = self.conexionM.guardar_datos_many(json_datas)
            if not res:
                self.guardar()
                self.GuardoDatos = True
            else:
                self.elementos = []
                self.obtener_rooms_info()

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

