import pygame as pg
import random

# Lista de palabras para el juego
lista_palabras = [
    "hola", "adios", "casa", "perro", "gato", "raton", "elefante",
    "leon", "tigre", "oso", "pajaro", "pez", "ballena", "delfin",
    "tiburon", "serpiente", "cocodrilo", "rinoceronte", "hipopotamo",
    "jirafa", "cebra", "mono", "gorila", "orangutan", "chimpance",
    "koala", "canguro", "panda", "oso polar", "oso panda", "oso grizzly", "oso pardo"
]

class Ahorcado:
    def __init__(self):
        self.reiniciar()
        self.puntos = []

    def elegir_palabra(self):
        self.palabra = random.choice(lista_palabras)
        self.palabra_oculta = ["_"] * len(self.palabra)

    def comprobar_letra(self, letra):
        if letra in self.palabra and letra not in self.letras_acertadas:
            for i in range(len(self.palabra)):
                if self.palabra[i] == letra:
                    self.palabra_oculta[i] = letra
            self.letras_acertadas.append(letra)
        elif letra not in self.letras_falladas:
            self.letras_falladas.append(letra)
            self.intentos += 1

    def comprobar_palabra(self, palabra):
        if palabra == self.palabra:
            self.palabra_oculta = list(self.palabra)
        else:
            self.intentos += 1

    def comprobar_ganador(self):
        return "_" not in self.palabra_oculta

    def comprobar_perdedor(self):
        return self.intentos >= 7

    def mostrar_palabra(self):
        return " ".join(self.palabra_oculta)

    def generar_muñeco_por_errores(self, screen):
        partes = [
            lambda: pg.draw.circle(screen, (255, 255, 255), (400, 200), 50),  # Cabeza
            lambda: pg.draw.line(screen, (255, 255, 255), (400, 250), (400, 400), 5),  # Cuerpo
            lambda: pg.draw.line(screen, (255, 255, 255), (400, 300), (350, 350), 5),  # Brazo izquierdo
            lambda: pg.draw.line(screen, (255, 255, 255), (400, 300), (450, 350), 5),  # Brazo derecho
            lambda: pg.draw.line(screen, (255, 255, 255), (400, 400), (350, 450), 5),  # Pierna izquierda
            lambda: pg.draw.line(screen, (255, 255, 255), (400, 400), (450, 450), 5),  # Pierna derecha
            lambda: pg.draw.circle(screen, (0, 0, 0), (380, 190), 5),  # Ojo izquierdo
            lambda: pg.draw.circle(screen, (0, 0, 0), (420, 190), 5)   # Ojo derecho
        ]
        
        # Dibuja solo las partes que corresponden al número de intentos
        for i in range(self.intentos):
            partes[i]()

    def mostrar_puntos(self):
        return "Puntos: " + str(sum(self.puntos))
    
    def mostrar_letra_ingresada(self):
        letras_acertadas = "Letras acertadas: " + ", ".join(self.letras_acertadas)
        letras_falladas = "Letras falladas: " + ", ".join(self.letras_falladas)
        return letras_acertadas, letras_falladas

    def reiniciar(self):
        self.elegir_palabra()  # Llamada correcta a la función
        self.intentos = 0
        self.letras_acertadas = []
        self.letras_falladas = []
    
    def ganar_puntos(self):
        self.puntos.append(len(self.letras_acertadas) *3 - len(self.letras_falladas))

# Inicialización de Pygame
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Juego del Ahorcado")
font = pg.font.Font(None, 36)

# Instancia del juego
ahorcado = Ahorcado()

running = True
while running:
    screen.fill((0, 0, 0))  # Limpiar la pantalla al inicio de cada ciclo
    screen.blit(font.render(ahorcado.mostrar_puntos(), True, (255, 255, 255)), (20, 100))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.unicode.isalpha() and len(event.unicode) == 1:
                ahorcado.comprobar_letra(event.unicode)
            if event.key == pg.K_RETURN:
                palabra_ingresada = input("Introduce una palabra: ")
                if palabra_ingresada.strip():  # Verifica que no esté vacío
                    ahorcado.comprobar_palabra(palabra_ingresada)

    palabra = ahorcado.mostrar_palabra()
    texto_palabra = font.render(palabra, True, (255, 255, 255))
    screen.blit(texto_palabra, (400 - texto_palabra.get_width() // 2, 500))

    ahorcado.generar_muñeco_por_errores(screen)
    letras_acertadas, letras_falladas = ahorcado.mostrar_letra_ingresada()
    texto_acertadas = font.render(letras_acertadas, True, (255, 255, 255))
    texto_falladas = font.render(letras_falladas, True, (255, 255, 255))
    screen.blit(texto_acertadas, (20, 20))
    screen.blit(texto_falladas, (20, 60))

    if ahorcado.comprobar_ganador():
        mensaje_ganador = font.render("¡Has ganado!", True, (0, 255, 0))
        screen.blit(mensaje_ganador, (400 - mensaje_ganador.get_width() // 2, 550))
        pg.display.flip()
        pg.time.wait(2000)
        ahorcado.ganar_puntos()
        ahorcado.reiniciar()

    if ahorcado.comprobar_perdedor():
        mensaje_perdedor = font.render("Has perdido. La palabra era: " + ahorcado.palabra, True, (255, 0, 0))
        screen.blit(mensaje_perdedor, (400 - mensaje_perdedor.get_width() // 2, 550))
        pg.display.flip()
        pg.time.wait(2000)
        ahorcado.ganar_puntos()
        ahorcado.reiniciar()

    pg.display.flip()

pg.quit()