import requests
import json
import socket
import pymongo

class ConexionMongoDB:
    def __init__(self):
        self.client = None
        self.db_name = "Integrador"
        self.collection_name = "sensor_data"
        self.isconexion = False
        self.db = None
        self.collection = None

    def conectar(self):
        try:
            self.client = pymongo.MongoClient("mongodb+srv://jesusaranda5446373773:2uDKpO465FuUDvwM@cluster0.sosxkit.mongodb.net/?retryWrites=true&w=majority")
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print("Conexión con la base de datos establecida")
            self.isconexion = True
        except Exception as e:
            self.isconexion = False
            raise ConnectionError("Error al conectar con la base de datos:", e)

    def guardar_datos_many(self, data):
        print(data)
        try:
            self.collection.insert_many(data)
            print("Datos guardados en la base de datos")
            return True
        except Exception as e:
            print("Error al guardar los datos en la base de datos:", e)
            return False
    
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
        self.base_url = "http://127.0.0.1:8000/api/auth"
        self.session = requests.Session()
        self.headers = {}
        self.is_conexion = False

    def is_connection_valid(self):
        try:
            response = self.session.get("http://127.0.0.1:8000")
            self.login()
            self.is_conexion = True if response.status_code == 200 else False
        except requests.exceptions.RequestException:
            self.is_conexion = False
        except ConnectionError as e:
            self.is_conexion = False
            print("Error saving room data:", e)

    def login(self):
            
        path = "/login"
        url = self.base_url + path
        data = {
            "email": "jesusaranda8714544@hotmail.com",
            "password": "Alicia544."
        }   
        try:
            response = self.session.post(url, data=data)
            if response.status_code == 200:
                json_response = response.json()
                token = json_response['access_token']
                role_id = str(json_response['role_id'])
                self.headers = {
                    "Authorization": "Bearer " + token,
                    "role_id": role_id
                }
                self.is_conexion = True
                return True
            else:
                print("Login failed with status code:", response.status_code)
        except ConnectionError as e:
            self.is_conexion = False
            
            print("Error saving room data:", e)
            return False
        except Exception as e:
            self.is_conexion = False
            print("Error during login:", e)
            return False

        return False

    def get_rooms(self):
        try:
            if not self.is_conexion:
                return None
                
            path = "/habitaciones"
            url = self.base_url + path
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                with open("roomsApi.json", "w") as file:
                    json.dump(response.json(), file)
                return response.json()
            else:
                print("Failed to get rooms with status code:", response.status_code)
        except ConnectionError as e:
            self.is_conexion = False
            print("Error saving room data:", e)
            return False
        except Exception as e:
            self.is_conexion = False
            print("Error getting rooms:", e)
            return False
        
        return None

    def save_room_data(self, name, data, room_id, date_time):
        try:
            if not self.is_conexion:
                return None
                
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
            else:
                print("Failed to save room data with status code:", response.status_code)
                return False
        
        except ConnectionError as e:
            self.is_conexion = False
            print("Error de conexión al guardar datos de habitación:", e)
            return False
        except Exception as e:
            self.is_conexion = False
            print("Error saving room data:", e)
            return False
        return None





