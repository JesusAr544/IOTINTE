class Arreglo:
    def __init__(self, elementos=None):
        self.isarreglo = False
        if elementos is None:
            self.elementos = []
        else:
            self.elementos = elementos

    def agregar_elemento(self, elemento):
        self.elementos.append(elemento)

    def eliminar_elemento(self, elemento):
        if elemento in self.elementos:
            self.elementos.remove(elemento)
        else:
            print("Elemento no encontrado en el arreglo.")
