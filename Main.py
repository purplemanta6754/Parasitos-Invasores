import pygame as pg
import random
import math
import cv2

# Importar clases
import src.MenuScreen as menu

# Inicialización de Pygame
pg.init()
pg.mixer.init()

# ----------------------- CONSTANTES -----------------------

# Rutas de los recursos
RUTA_LOGO = "assets/images/logo.png"
RUTA_FONDO = "assets/images/bg.png"
RUTA_JUGADOR_NAVE = "assets/images/player/player_ship.png"
RUTA_JUGADOR_LASER = "assets/images/player/player_laserbeam.png"
RUTA_ENEMIGO_NAVE = "assets/images/enemies/parasite_ship.png"
RUTA_ENEMIGO_LASER = "assets/images/enemies/parasite_laserbeam.png"
RUTA_JEFE_IMAGEN = "assets/images/enemies/boss.png"

# Rutas de los sonidos
RUTA_COMANDANTE_ORDEN = "assets/sounds/commander's_order.ogg"
RUTA_LASER_SONIDO = "assets/sounds/laser.ogg"
RUTA_EXPLOSION_SONIDO = "assets/sounds/explosion.ogg"
RUTA_GOLPE_SONIDO = "assets/sounds/hit.ogg"
RUTA_GRUÑIDO1 = "assets/sounds/growl1.ogg"
RUTA_GRUÑIDO2 = "assets/sounds/growl2.ogg"

# Configuraciones de la ventana
ANCHO = 800
ALTO = 600

# Configuraciones del juego
FPS = 60
VELOCIDAD_ENEMIGOS = 1
TIEMPO_ENTRE_DISPAROS_ENEMIGOS = 1000

# ----------------------- CLASES -----------------------

class Jugador(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(RUTA_JUGADOR_NAVE).convert_alpha()
        pg.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.centery = ALTO - 50
        self.velocidad_x = 0
        self.vida = 100

    def update(self, x_cara):
        self.velocidad_x = (x_cara - self.rect.centerx) // 10
        self.rect.x += self.velocidad_x
        self.rect.clamp_ip(0, 0, ANCHO, ALTO)

    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_balas_jugador.add(bala)
        pg.mixer.Sound(RUTA_LASER_SONIDO).play()

class Enemigos(pg.sprite.Sprite):
    ultimo_disparo_enemigo = pg.time.get_ticks()

    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(RUTA_ENEMIGO_NAVE).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = VELOCIDAD_ENEMIGOS
        self.moving_right = True
        self.tiempo_entre_disparos = random.randint(0, TIEMPO_ENTRE_DISPAROS_ENEMIGOS)

    def update(self):
        if self.moving_right:
            self.rect.x += self.velocidad_x
        else:
            self.rect.x -= self.velocidad_x

        if self.rect.right >= ANCHO:
            self.moving_right = False
            self.rect.y += 60
        elif self.rect.left <= 0:
            self.moving_right = True
            self.rect.y += 60

    def disparar_enemigos(self):
        ahora = pg.time.get_ticks()
        if ahora - Enemigos.ultimo_disparo_enemigo > 500:
            bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
            grupo_balas_enemigos.add(bala)
            pg.mixer.Sound(RUTA_LASER_SONIDO).play()
            Enemigos.ultimo_disparo_enemigo = ahora
            pg.mixer.Sound(RUTA_COMANDANTE_ORDEN).play()

class Jefe(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(RUTA_JEFE_IMAGEN).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, 100)
        self.velocidad = 10
        self.vida = 1000
        self.vida_total = 1000
        self.angulo = 0

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.velocidad *= -1

        self.angulo += 0.1

    def disparar_enemigos(self):
        if random.random() < 0.01:
            for _ in range(10):
                angulo_rad = math.radians(self.angulo)
                bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
                bala.velocidad_x = 6 * math.cos(angulo_rad)
                bala.velocidad_y = 6 * math.sin(angulo_rad)
                grupo_balas_enemigos.add(bala)
                self.angulo += 36

class Balas(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(RUTA_JUGADOR_LASER).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class Balas_enemigos(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(RUTA_ENEMIGO_LASER).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidad_x = 0
        self.velocidad_y = 3

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.bottom > ALTO or self.rect.top < 0 or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pg.image.load(f"assets/images/sprites/explosion/1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.time = pg.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0 

    def update(self):
        tiempo = pg.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo 
            self.frames += 1
            if self.frames == 12:
                self.kill()
            else:
                position = self.rect.center
                self.image = pg.image.load(f"assets/images/sprites/explosion/{self.frames + 1}.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.center = position

# ----------------------- FUNCIONES -----------------------

def crear_enemigos(num_filas, num_columnas, x_inicio, y_inicio, espacio_entre_enemigos):
    for fila in range(num_filas):
        for columna in range(num_columnas):
            x = x_inicio + columna * espacio_entre_enemigos
            y = y_inicio + fila * espacio_entre_enemigos
            enemigo = Enemigos(x, y)
            grupo_enemigos.add(enemigo)

def agregar_jefe():
    jefe = Jefe()
    pg.mixer.Sound(RUTA_GRUÑIDO1).play()
    grupo_enemigos.add(jefe)
    return jefe

def texto_puntuacion(frame, text, size, x, y):
    font = pg.font.SysFont("assets/fonts/Space-Grotesk/SpaceGrotesk-Medium.ttf", size, bold=True)
    text_frame = font.render(text, True, (255, 255, 255))
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x, y)
    frame.blit(text_frame, text_rect)

def barra_vida(frame, x, y, nivel, total):
    longitud = 200
    alto = 20
    fill = int((nivel / total) * longitud)
    border = pg.Rect(x, y, longitud, alto)
    fill = pg.Rect(x, y, fill, alto)
    pg.draw.rect(frame, (255, 0, 55), fill)
    pg.draw.rect(frame, (0, 0, 0), border, 4)

# ----------------------- INICIALIZACIÓN DEL JUEGO -----------------------

# Cargar recursos
logo = pg.image.load(RUTA_LOGO)
fondo = pg.image.load(RUTA_FONDO)

# Crear la ventana
ventana = pg.display.set_mode((ANCHO, ALTO))
pg.display.set_caption("Parásitos Invasores")

# Grupos de sprites
grupo_jugador = pg.sprite.Group()
grupo_enemigos = pg.sprite.Group()
grupo_balas_jugador = pg.sprite.Group()
grupo_balas_enemigos = pg.sprite.Group()
grupo_explosiones = pg.sprite.Group()

# Inicializar el jugador
player = Jugador()
grupo_jugador.add(player)

# Inicializar la cámara
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ejecutar el menú
menu.ejecutar_menu()

# Crear los enemigos iniciales
crear_enemigos(4, 10, 10, 10, 60)

# Variables del juego
run = True
score = 0
vida = 100
fase_jefe = False
dano_jefe = 0
clock = pg.time.Clock()

# ----------------------- BUCLE PRINCIPAL -----------------------

while run:
    # Manejar eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.disparar()

    # Obtener la posición de la cara de la cámara
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_resized = cv2.resize(frame, (ANCHO // 2, ALTO // 2))
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    # Actualizar la posición del jugador
    x_cara = ANCHO // 2
    for (x, y, w, h) in faces:
        x_cara = (x + w // 2) * 2
        cv2.rectangle(frame, (x * 2, y * 2), ((x + w) * 2, (y + h) * 2), (255, 0, 0), 2)
        break
    player.update(x_cara)

    # Actualizar sprites
    grupo_jugador.update(x_cara)
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    grupo_explosiones.update()

    # Disparar enemigos
    if grupo_enemigos:
        enemigo_a_disparar = random.choice(grupo_enemigos.sprites())
        if isinstance(enemigo_a_disparar, Enemigos):
            enemigo_a_disparar.disparar_enemigos()

    # Dibujar sprites
    ventana.blit(fondo, (0, 0))
    grupo_jugador.draw(ventana)
    grupo_enemigos.draw(ventana)
    grupo_balas_jugador.draw(ventana)
    grupo_balas_enemigos.draw(ventana)
    grupo_explosiones.draw(ventana)

    # Comprobar colisiones
    colision1 = pg.sprite.groupcollide(grupo_balas_jugador, grupo_enemigos, True, False)
    for bala, enemigos in colision1.items():
        for enemigo in enemigos:
            if isinstance(enemigo, Jefe):
                pg.mixer.Sound(RUTA_GRUÑIDO2).play()
                enemigo.vida -= 10
                dano_jefe += 10
                if enemigo.vida <= 0:
                    enemigo.kill()
                    fase_jefe = False
            else:
                enemigo.kill()
                score += 10
            explo = Explosion(enemigo.rect.center)
            grupo_explosiones.add(explo)
            pg.mixer.Sound(RUTA_EXPLOSION_SONIDO).set_volume(0.3)
            pg.mixer.Sound(RUTA_EXPLOSION_SONIDO).play()

    colision2 = pg.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for hit in colision2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
        explo1 = Explosion(hit.rect.center)
        grupo_explosiones.add(explo1)
        pg.mixer.Sound(RUTA_GOLPE_SONIDO).play()

    hits = pg.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        if isinstance(hit, Jefe):
            player.vida -= 100
        else:
            player.vida -= 10
            player.score -= 5
        if player.vida <= 0:
            run = False

    # Agregar jefe
    if len(grupo_enemigos) == 0 and not fase_jefe:
        jefe = agregar_jefe()
        fase_jefe = True

    # Mostrar información del juego
    texto_puntuacion(ventana, "PUNTAJE: " + str(score) + "     ", 30, ANCHO - 85, 10)
    barra_vida(ventana, ANCHO - 200, 30, player.vida, 100)

    if fase_jefe:
        texto_puntuacion(ventana, "JEFE", 30, 85, 10)
        barra_vida(ventana, 15, 30, jefe.vida, jefe.vida_total)

    # Actualizar la pantalla
    pg.display.flip()
    clock.tick(FPS)

# Limpiar recursos
cap.release()
cv2.destroyAllWindows()
pg.quit()