import json
from conexion import ConexionSocket, ConexionApi  ,ConexionMongoDB # Importar clases de otros archivos

class Arreglo:
    def __init__(self, elementos=None):
        self.isarreglo = False
        self.conexionS = ConexionSocket()  # Inicializar una instancia de la clase ConexionSocket
        self.conexionA = ConexionApi()      # Inicializar una instancia de la clase ConexionApi
        self.conexionM = ConexionMongoDB()  # Inicializar una instancia de la clase ConexionMongoDB
        self.conexionM.conectar()           # Conectar a la base de datos
        self.GuardoDatos = False
        
        # Inicializar la lista de elementos
        if elementos is None:
            self.elementos = []
        else:
            self.elementos = elementos

    # Método para agregar un elemento a la lista
    def agregar_elemento(self, elemento):
        self.elementos.append(elemento)

    # Método para eliminar un elemento de la lista
    def eliminar_elemento(self, elemento):
        if elemento in self.elementos:
            self.elementos.remove(elemento)
        else:
            print("Elemento no encontrado en el arreglo.")

    # Método para guardar los elementos en un archivo JSON
    def guardar(self, filename):
        with open(filename, "w") as file:
                json.dump(self.serializar(), file)  # Llama al método serializar y guarda los datos en el archivo
                self.GuardoDatos = True

    # Método para cargar elementos desde un archivo JSON
    def cargar(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)  # Carga los datos desde el archivo JSON
                self.cargoDatos = True
                return data
        except FileNotFoundError:
            print(f"El archivo '{filename}' no se encontró.")
        except Exception as e:
            print(f"Error al cargar el archivo '{filename}': {e}")

    # Método para cargar datos desde un archivo JSON llamado "sensores.json"
    def cargarSensoresJson(self):
        try:
            with open("sensores.json", "r") as file:
                data = json.load(file)  # Carga los datos desde el archivo JSON
                return data
        except FileNotFoundError:
            print("El archivo sensores.json no se encontró.")
        except Exception as e:
            print(f"Error al cargar el archivo sensores.json: {e}")

    # Método para cargar datos desde un archivo JSON llamado "roomsApi.json"
    def cargarRoomApi(self):
        try:
            with open("roomsApi.json", "r") as file:
                data = json.load(file)  # Carga los datos desde el archivo JSON
                return data
        except FileNotFoundError:
            print("El archivo roomsApi.json no se encontró.")
        except Exception as e:
            print(f"Error al cargar el archivo roomsApi.json: {e}")
