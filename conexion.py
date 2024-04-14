import requests
import json
import socket
import pymongo

class ConexionMongoDB:
    def __init__(self):
        self.client = None
        self.db_name = "Integrador"
        self.collection_name = "sensor_data"
        self.db = None
        self.collection = None

    def conectar(self):
        try:
            self.client = pymongo.MongoClient("mongodb+srv://jesusaranda5446373773:2uDKpO465FuUDvwM@cluster0.sosxkit.mongodb.net/?retryWrites=true&w=majority")
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
        except Exception as e:
            raise ConnectionError("Error al conectar con la base de datos:", e)

    def guardar_datos_many(self, data):
        try:
            self.collection.insert_many(data)
            print("Datos guardados en la base de datos")
        except Exception as e:
            print("Error al guardar los datos en la base de datos:", e)
    
    def cerrar_conexion(self):
        if self.client:
            self.client.close()
            print("Conexión con la base de datos cerrada")
class ConexionSocket:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 1234
        self.server_socket = None

    def iniciar_servidor(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Servidor escuchando en {self.host}:{self.port}")

    def recibir_datos(self):
        client_socket, client_address = self.server_socket.accept()
        with client_socket:
            data = client_socket.recv(1024)
            data = json.loads(data.decode())
            return data

    def cerrar_servidor(self):
        if self.server_socket:
            self.server_socket.close()
            print("Servidor cerrado")

class ConexionApi:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/api/auth"
        self.session = requests.Session()
        self.headers = {}
        self.is_conexion = self.is_conexion_valida()

    def is_conexion_valida(self):
        try:
            response = self.session.get("http://127.0.0.1:8000")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def login(self):
        if self.is_conexion:
            path = "/login"
            url = self.url + path
            data = {
                "email": "jesusaranda8714544@hotmail.com",
                "password": "Alicia544."
            }   
            try:
                response = requests.post(url, data=data, headers=self.headers)
                if response.status_code == 200:
                    json_response = response.json()
                    token = json_response['access_token']
                    role_id = str(json_response['role_id'])
                    self.headers = {
                        "Authorization": "Bearer " + token,
                        "role_id": role_id
                    }
                    return True
            except Exception as e:
                self.is_conexion = False
                print("Error en el inicio de sesión:", e)
        return False

    def obtener_habitaciones(self):
        try:
            if self.is_conexion:
                path = "/habitaciones"
                url = self.url + path
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 200:
                    with open("roomsApi.json", "w") as file:
                        json.dump(response.json(), file)
                    return response.json()
        except Exception as e:
            self.is_conexion = False
            print("Error al obtener las habitaciones:", e)
        return None

    def guardar_datos_habitacion(self, name, data, room_id, date_time):
        try:
            if self.is_conexion:
                url = "http://127.0.0.1:8000/api/sensores"
                json_data = {
                    "name": name,
                    "data": data,
                    "room_id": room_id,
                    "date_time": date_time
                }
                response = self.session.post(url, json=json_data, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            self.is_conexion = False
            print("Error al guardar datos de la habitación:", e)
        return None





if __name__ == "__main__":
    data = [
        {
            "name": "sensor1",
            "data": 25,
            "room_id": 1,
            "date_time": "2021-09-10 12:00:00"
        },
        {
            "name": "sensor2",
            "data": 30,
            "room_id": 1,
            "date_time": "2021-09-10 12:00:00"
        }
    ]
    conexion = ConexionMongoDB()
    conexion.conectar()
    conexion.guardar_datos_many(data)