# Módulos necesarios
import random
import sys
import pygame
# Datos de pantalla
alto_pantalla = 800
ancho_pantalla = 600
# Cargamos gráficos
img_xwing_lista = [
    pygame.image.load('data/xwing0000.png'),
    pygame.image.load('data/xwing0001.png'),
    pygame.image.load('data/xwing0002.png'),
    pygame.image.load('data/xwing0003.png'),
    pygame.image.load('data/xwing0004.png'),
    pygame.image.load('data/xwing0005.png'),
    pygame.image.load('data/xwing0006.png'),
    pygame.image.load('data/xwing0007.png'),
    pygame.image.load('data/xwing0008.png'),
    pygame.image.load('data/xwing0009.png'),
    pygame.image.load('data/xwing0010.png'),
    pygame.image.load('data/xwing0011.png'),
    pygame.image.load('data/xwing0012.png'),
    pygame.image.load('data/xwing0013.png'),
    pygame.image.load('data/xwing0014.png'),
    pygame.image.load('data/xwing0015.png'),
    pygame.image.load('data/xwing0016.png'),
    pygame.image.load('data/xwing0017.png'),
    pygame.image.load('data/xwing0018.png'),
    pygame.image.load('data/xwing0019.png'),
    pygame.image.load('data/xwing0020.png'),
    pygame.image.load('data/xwing0021.png'),
    pygame.image.load('data/xwing0022.png'),
    pygame.image.load('data/xwing0023.png'),
    pygame.image.load('data/xwing0024.png'),
    pygame.image.load('data/xwing0025.png'),
    pygame.image.load('data/xwing0026.png'),
    pygame.image.load('data/xwing0027.png'),
    pygame.image.load('data/xwing0028.png'),
    pygame.image.load('data/xwing0029.png'),
    pygame.image.load('data/xwing0030.png'),

    ]
img_xwing = img_xwing_lista[2]
img_tief = pygame.image.load('data/tie.png')
img_shuttle = pygame.image.load('data/shuttle.png')
img_stroopers = pygame.image.load('data/stroopers.png')
img_falconm = pygame.image.load('data/MFalcon.png')
img_corveta = pygame.image.load('data/corveta.png')
laser_verde = pygame.image.load('data/laser_ve.png')
laser_rojo = pygame.image.load('data/laser_ro.png')
fondo = pygame.image.load("data/stars_bg.png")
explosion_bites = [pygame.image.load("data/exp_01.png"),
                   pygame.image.load("data/exp_02.png"),
                   pygame.image.load("data/exp_03.png"),
                   pygame.image.load("data/exp_04.png"),
                   pygame.image.load("data/exp_05.png"),
                   pygame.image.load("data/exp_06.png"),
                   pygame.image.load("data/exp_07.png"),
                   pygame.image.load("data/exp_08.png"),
                   pygame.image.load("data/exp_09.png"),
                   pygame.image.load("data/exp_10.png"),
                   pygame.image.load("data/exp_11.png"),
                   pygame.image.load("data/exp_12.png"),
                   pygame.image.load("data/exp_13.png"),
                   ]
lista_naves_aleatorias = [img_falconm,img_corveta]
lista_objetos_enemigos = []
lista_laseres_verdes = []
lista_laseres_rojos = []
lista_naves_adorno = []
lista_explosiones = []
lista_jugadores = []
desplazamiento_de_fondo = 0
tiempo_anim_giro = 10
vel_laser_r = 10
vel_laser_v = -10
vel_tief = 3
indice_naves_aleatorias = 2
player_2 = False
saturacion_disparo = 25
saturacion_tiempo_ties = [0, 100]
saturacion_disparo_player = [saturacion_disparo, saturacion_disparo]
naves_destruidas = 0
size_letra = 25
puntos_a_sumar = 5

def pintar_puntos_pantalla(jugador):

    #Comprobamos la ID del jugador
    x = 20
    y = 0
    if jugador[3] == 1:
        y=5
    elif jugador[3] == 2:
        x=ancho_pantalla+50
        y= 5
    texto_Pantalla = myfont.render(f'Puntos Piloto {jugador[3]}', False, (255, 0, 0))
    screen.blit(texto_Pantalla, (x, y))
    texto_Pantalla = myfont.render(str(jugador[6]), False, (255, 0, 0))
    screen.blit(texto_Pantalla, (x, y+20))

def random_naves_aleatoras(naves_destruidas):
    if naves_destruidas == 10:
       pasada_de_nave_adorno(lista_naves_aleatorias[0])
    elif naves_destruidas == 20:
       pasada_de_nave_adorno(lista_naves_aleatorias[1])
    #print(naves_destruidas)


def pasada_de_nave_adorno(imagen):
    lista_naves_adorno.append([imagen, random.randint(0,ancho_pantalla),600])

def actualiza_y_pinta_naves_adorno():
    for nave in lista_naves_adorno:
        if nave[0] == img_falconm:
            screen.blit(nave[0], (nave[1], nave[2]))
            nave[2] -= 5
            if nave[2] > 2000: lista_naves_adorno.remove(nave)
        else:
            screen.blit(nave[0], (nave[1], nave[2]))
            nave[2] -= 2
            if nave[2] > 2000: lista_naves_adorno.remove(nave)


def dibujar_lista_jugadores():
    for jugador in lista_jugadores:
        screen.blit(jugador[0], (jugador[1], jugador[2]))

def actualiza_animacion_direccion_jugador(jugador, valor):
    #Miramos el tiempod de animacion
    if valor == "derecha":
        if jugador[4] < 30: jugador[4] += 1
    elif valor == "izquierda":
        if jugador[4] > 0 : jugador[4] -= 1
    elif valor == "centro" :
        if jugador[4] < 15: jugador[4] += 1
        elif jugador[4] > 15:  jugador[4] -= 1
    jugador[0] = img_xwing_lista[jugador[4]]




def dibujar_lista_objetos_dinamicos(lista_objetos_dinamicos):
    for objeto in lista_objetos_dinamicos:
        screen.blit(objeto[0], (objeto[1], objeto[2]))


def nueva_explosion(pos_x, pos_y):
    # explosion [fase (entero de 1 a 13) y pos]
    lista_explosiones.append([0, pos_x - 100, pos_y - 100])


def actualizar_y_pintar_explosiones():
    for explosion in lista_explosiones:
        # Pinto la explosion
        screen.blit(explosion_bites[explosion[0]], (explosion[1], explosion[2]))
        # Actualizo la explosion
        if explosion[0] < len(explosion_bites) - 1:
            explosion[0] += 1
        else:
            lista_explosiones.remove(explosion)


def chequea_colision_impactos(lista_objetos, lista_laseres_rojos):
    # Chequeamos para cada laser
    for laser in lista_laseres_rojos:
        for objeto in lista_objetos:
            # Chequeo altura
            if abs((objeto[2] - laser[2])) < 10:
                # Chequeo horizontal
                ancho_nave = objeto[0].get_width()
                if laser[1] - objeto[1] > 0 and laser[1] - objeto[1] < ancho_nave:
                    nueva_explosion(objeto[1], objeto[2])
                    effect = pygame.mixer.Sound('data/ExplosionFighter1.wav')
                    effect.play()
                    lista_objetos.remove(objeto)
                    #Veo qué jugador disparó el laser
                    id_player = laser[3]
                    #sumo los puntos
                    for player in lista_jugadores:
                        if player[3] == id_player: player[6] += puntos_a_sumar
                    lista_laseres_rojos.remove(laser)
                    return True


def chequea_impacto_en_jugador(lista_jugadores, lista_laseres_verdes):
    # Chequeamos para cada laser
    for laser in lista_laseres_verdes:
        for jugador in lista_jugadores:
            # Chequeo altura
            if abs((jugador[2] - laser[2])) < 10:
                ancho_nave = jugador[0].get_width()
                if laser[1] - jugador[1] > 0 and laser[1] - jugador[1] < ancho_nave:
                    nueva_explosion(jugador[1], jugador[2])
                    effect = pygame.mixer.Sound('data/ExplosionFighter1.wav')
                    effect.play()
                    lista_jugadores.remove(jugador)


def actualiza_aparicion_ties():
    if (saturacion_tiempo_ties[0] < saturacion_tiempo_ties[1]):
        saturacion_tiempo_ties[0] += 1
    else:
        nave = random.randint(0, 101)
        if nave < 15:
            inserta_nave_ia(img_stroopers, (random.randint(0, ancho_pantalla)), 0, lista_objetos_enemigos)
        elif nave > 90:
            inserta_nave_ia(img_shuttle, (random.randint(0, ancho_pantalla)), 0, lista_objetos_enemigos)
        else:
            inserta_nave_ia(img_tief, (random.randint(0, ancho_pantalla)), 0, lista_objetos_enemigos)
        saturacion_tiempo_ties[0] = 0


def inserta_nave_ia(img_nave, posx, posy, lista_objetos):
    lista_objetos.append([img_nave, posx, posy])


def insertar_nuevo_jugador(img_nave, posx, posy, id, estado_animacion, tiempo_animacion, puntos):
    lista_jugadores.append([img_nave, posx, posy, id, estado_animacion, tiempo_animacion, puntos])


def dispara_laser(posx, posy, lista_objetos, player):
    if saturacion_disparo_player[player-1] == saturacion_disparo:
        # Dispara (guardamos el jugador que disparó para contar los puntos.
        lista_objetos.append([laser_rojo, posx, posy, player])
        lista_objetos.append([laser_rojo, posx + 52, posy, player])
        # Marco saturación de disparo
        saturacion_disparo_player[player-1] = 0
        # Emito sonido
        effect = pygame.mixer.Sound('data/xfire.ogg')
        effect.play()


def disparar_laser_enemigos(posx, posy, lista_objetos):
    # Dispara
    lista_objetos.append([laser_verde, posx + 15, posy + 15])
    lista_objetos.append([laser_verde, posx + 21, posy + 15])
    # Emito sonido
    effect = pygame.mixer.Sound('data/EmpireLaserTurbo.wav')
    effect.play()


def actualiza_saturacion_disparos():
    if saturacion_disparo_player[0] < saturacion_disparo:
        saturacion_disparo_player[0] += 1
    if saturacion_disparo_player[1] < saturacion_disparo:
        saturacion_disparo_player[1] += 1


def actualiza_posiciones_dinamicos(lista_objetos_dinamicos):
    for objeto in lista_objetos_dinamicos:
        if objeto[0] == laser_rojo:
            # Está fuera de pantalla?
            if objeto[2] > 0:
                objeto[2] -= vel_laser_r
            else:
                lista_objetos_dinamicos.remove(objeto)
        if objeto[0] == laser_verde:
            # Está fuera de pantalla?
            if objeto[2] < alto_pantalla:
                objeto[2] -= vel_laser_v
            else:
                lista_objetos_dinamicos.remove(objeto)
        elif objeto[0] == img_tief:
            if objeto[2] < alto_pantalla:
                objeto[2] += vel_tief
                # Disparamos?
                if (random.randint(0, 100) == 100):
                    disparar_laser_enemigos(objeto[1], objeto[2], lista_laseres_verdes)
            else:
                lista_objetos_dinamicos.remove(objeto)
        elif objeto[0] == img_shuttle:
            if objeto[2] < alto_pantalla:
                objeto[2] += vel_tief - 1
            else:
                lista_objetos_dinamicos.remove(objeto)
        elif objeto[0] == img_stroopers:
            if objeto[2] < alto_pantalla:
                objeto[2] += vel_tief - 2
            else:
                lista_objetos_dinamicos.remove(objeto)
def crear_nuevo_jugador(lista_jugadores, pos_x, pos_y, id):
    # Chequeamos que no esté ya jugando
    existe = False
    for jugador in lista_jugadores:
        if jugador[3] == id:
            existe = True
    if not existe:
        # Creamos jugador_1 con img_xwing, posx,posy, id player 1 y estado animación 15 y puntos
        insertar_nuevo_jugador(img_xwing, pos_x, pos_y, id, 15, tiempo_anim_giro, 0)

# Inicializamos
pygame.init()
#También el uso de letras
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', size_letra)
#Texto de la ventana
pygame.display.set_caption('Python Wars!')
# Un poco de música emotiva
pygame.mixer.music.load('data/backgroundmusic.ogg')
pygame.mixer.music.play(0)
# Iniciamos la pantalla
screen = pygame.display.set_mode((alto_pantalla, ancho_pantalla))

# Creamos jugador_1 con img_xwing, posx,posy, id player 1 y estado animacion 15, tiempo entre animaciones y puntos
crear_nuevo_jugador(lista_jugadores, 375, 500, 1)
done = False

clock = pygame.time.Clock()

# surface = pygame.Surface((64, 55), pygame.SRCALPHA)

salir = False
while not salir:
    # Desplazamiento de los dos rectángulos de fondo de estrellas
    if desplazamiento_de_fondo > ancho_pantalla:
        desplazamiento_de_fondo = 0
    screen.blit(fondo, (0, desplazamiento_de_fondo))
    screen.blit(fondo, (0, desplazamiento_de_fondo - ancho_pantalla))
    desplazamiento_de_fondo += 1.5
    # Control de teclado
    pressed = pygame.key.get_pressed()
    # Salimos?
    if pressed[pygame.K_ESCAPE]:
        salir = True
    # ¿Metemos al player 2?
    if pressed[pygame.K_t]:
        # Creamos jugador_2 con img_xwing, posx,posy, id player 2 y estado animación 15 y puntos
        crear_nuevo_jugador(lista_jugadores, 500, 500, 2)
        # Lo habilitamos para jugar
        player_2 = True
    if pressed[pygame.K_r]:
        # Creamos jugador_1 con img_xwing, posx,posy, id player 1 y estado animación 15 y puntos
        crear_nuevo_jugador(lista_jugadores, 370, 500, 1)
    # Movimientos de los jugadores
    for jugador in lista_jugadores:
        # Saco ese jugador (Esto se puede mejorar, pero pierdo claridad
        x = jugador[1]
        y = jugador[2]
        # Dependiendo del jugador que sea, se usan unas teclas u otras
        if (jugador[3] == 1):
            # Es player 1
            if pressed[pygame.K_UP] and y > 0: y -= 4
            if pressed[pygame.K_DOWN] and y < ancho_pantalla - 80: y += 4
            if pressed[pygame.K_LEFT] and x > 0:
                x -= 4
                actualiza_animacion_direccion_jugador(jugador, "izquierda")
            if pressed[pygame.K_RIGHT] and x < alto_pantalla - 58:
                x += 4
                actualiza_animacion_direccion_jugador(jugador, "derecha")
            if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                actualiza_animacion_direccion_jugador(jugador, "centro")
            if pressed[pygame.K_RSHIFT]: dispara_laser(x, y, lista_laseres_rojos, 1)
            if pressed[pygame.K_v]: pasada_de_nave_adorno(img_corveta)
        elif (jugador[3] == 2):
            # Es player 2
            if pressed[pygame.K_w] and y > 0: y -= 4
            if pressed[pygame.K_s] and y < ancho_pantalla - 80: y += 4
            if pressed[pygame.K_a] and x > 0:
                x -= 4
                actualiza_animacion_direccion_jugador(jugador, "izquierda")
            if pressed[pygame.K_d] and x < alto_pantalla - 58:
                x += 4
                actualiza_animacion_direccion_jugador(jugador, "derecha")
            if not pressed[pygame.K_d] and not pressed[pygame.K_a]:
                actualiza_animacion_direccion_jugador(jugador, "centro")
            if pressed[pygame.K_LSHIFT]: dispara_laser(x, y, lista_laseres_rojos, 2)
        # asignamos los nuevos valores
        # guardamos los nuevos valores de posición
        jugador[1] = x
        jugador[2] = y
        # Pintamos al player
        #screen.blit(jugador[0], (jugador[1], jugador[2]))
    # Imprimos la lista de objetos dinámicos ¡¡Van en orden de capa de pintado!
    actualiza_y_pinta_naves_adorno()
    dibujar_lista_objetos_dinamicos(lista_laseres_rojos)
    dibujar_lista_objetos_dinamicos(lista_laseres_verdes)
    dibujar_lista_objetos_dinamicos(lista_objetos_enemigos)
    dibujar_lista_jugadores()
    chequea_impacto_en_jugador(lista_jugadores, lista_laseres_verdes)
    # Actualizamos el mundo del juego
    actualizar_y_pintar_explosiones()
    actualiza_posiciones_dinamicos(lista_objetos_enemigos)
    actualiza_posiciones_dinamicos(lista_laseres_rojos)
    actualiza_posiciones_dinamicos(lista_laseres_verdes)
    actualiza_saturacion_disparos()
    #Pintamos los textos en pantalla (va en la ultima capa)
    for jugador in lista_jugadores:
        pintar_puntos_pantalla(jugador)
    # Chequeamos triggers
    if chequea_colision_impactos(lista_objetos_enemigos, lista_laseres_rojos):
        naves_destruidas += 1
        random_naves_aleatoras(naves_destruidas)
    actualiza_aparicion_ties()
    #random_naves_aleatoras(naves_destruidas)
    # muestro pantalla y actualizo reloj
    pygame.display.flip()
    clock.tick(60)
    # Veo si se ha activado el evento de salir del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            sys.exit()
            pygame.display.quit()