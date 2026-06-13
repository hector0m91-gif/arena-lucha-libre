import queue
import random
import time

class Aficionado:
    contador = 1

    def __init__(self):
        self.__id = Aficionado.contador
        Aficionado.contador += 1

        nombres = ["Juan", "Pedro", "Ana", "Luis", "Carlos",
                   "María", "Sofía", "Diego", "José", "Elena"]

        self.__nombre = random.choice(nombres)

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def __str__(self):
        return f"Aficionado {self.__id}: {self.__nombre}"


class ArenaLuchaLibre:

    def __init__(self):
        self.__cola_entrada = queue.Queue()
        self.__cola_boletos = queue.Queue()

    def agregar_aficionado(self, aficionado):
        self.__cola_entrada.put(aficionado)

    def vender_boletos(self):
        while not self.__cola_entrada.empty():
            aficionado = self.__cola_entrada.get()

            print(f"Atendiendo a {aficionado}")
            time.sleep(1)

            self.__cola_boletos.put(aficionado)

            print(f"Boleto vendido a {aficionado}")

    def mostrar_boletos_vendidos(self):
        print("\n===== BOLETOS VENDIDOS =====")

        while not self.__cola_boletos.empty():
            print(self.__cola_boletos.get())


# Programa principal
arena = ArenaLuchaLibre()

for i in range(15):
    aficionado = Aficionado()
    arena.agregar_aficionado(aficionado)
    print(f"Llegó -> {aficionado}")

arena.vender_boletos()

arena.mostrar_boletos_vendidos()