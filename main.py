# Módulos necesarios
import random
import sys
import pygame
from graphics import *

# Datos de pantalla
alto_pantalla = 800
ancho_pantalla = 600

# Preparamos las listas y variables de gŕaficos
img_xwing_lista = []
explosion_bites = []

# Las variables las declaro a None ya que serán cargadas en un def más adelante, y por
# tanto deben existir antes de entrar en el def.
img_tief = None
img_shuttle = None
img_stroopers = None
img_falconm = None
img_corveta = None
laser_verde = None
laser_rojo = None
fondo = None

# Definimos la variables de configuración del juego.
desplazamiento_de_fondo = 0
tiempo_anim_giro = 10
vel_laser_r = 10
vel_laser_v = -10
vel_tief = 3
indice_naves_aleatorias = 2
player_2 = False
saturacion_disparo = 25
saturacion_tiempo_ties = [0, 100]
naves_destruidas = 0
size_letra = 25
puntos_a_sumar = 5


# ------------------------------ Pintar Puntos -------------------------------------------------------- #
def pintar_puntos_pantalla(jugador):

    # Comprobamos la ID del jugador
    x = 20
    y = 0
    if jugador[3] == 1:
        y = 5
    elif jugador[3] == 2:
        x = ancho_pantalla+50
        y = 5
    texto_pantalla = myfont.render(f'Puntos Piloto {jugador[3]}', False, (255, 0, 0))
    screen.blit(texto_pantalla, (x, y))
    texto_pantalla = myfont.render(str(jugador[6]), False, (255, 0, 0))
    screen.blit(texto_pantalla, (x, y+20))


# ------------------------------ Naves Aleatorias ----------------------------------------------------- #
def random_naves_aleatoras(naves_destruidas):
    if naves_destruidas == 10:
        pasada_de_nave_adorno(lista_naves_aleatorias[0])
    elif naves_destruidas == 20:
        pasada_de_nave_adorno(lista_naves_aleatorias[1])


# ------------------------------ Pasada nave adorno---------------------------------------------------- #
def pasada_de_nave_adorno(imagen):
    lista_naves_adorno.append([imagen, random.randint(0,ancho_pantalla),600])


# ------------------------------ Actualizar y pintar naves de adorno ---------------------------------- #
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


# ------------------------------ Dibujar lista de jugadores ------------------------------------------- #
def dibujar_lista_jugadores():
    for jugador in lista_jugadores:
        screen.blit(jugador[0], (jugador[1], jugador[2]))


# ------------------------------ Actualizar animación giros jugador ------------------------------------#
def actualiza_animacion_direccion_jugador(jugador, valor):
    # Miramos el tiempod de animacion
    if valor == "derecha":
        if jugador[4] < 30: jugador[4] += 1
    elif valor == "izquierda":
        if jugador[4] > 0 : jugador[4] -= 1
    elif valor == "centro" :
        if jugador[4] < 15: jugador[4] += 1
        elif jugador[4] > 15:  jugador[4] -= 1
    jugador[0] = img_xwing_lista[jugador[4]]


# ------------------------------ Dibujar objetos dinámicos -------------------------------------------- #
def dibujar_lista_objetos_dinamicos(lista_objetos_dinamicos):
    for objeto in lista_objetos_dinamicos:
        screen.blit(objeto[0], (objeto[1], objeto[2]))


# ------------------------------ Crear nueva explosión  ----------------------------------------------- #
def nueva_explosion(pos_x, pos_y):
    # explosion [fase (entero de 1 a 13) y pos]
    lista_explosiones.append([0, pos_x - 100, pos_y - 100])


# ------------------------------ Animar y pintar explosión -------------------------------------------- #
def actualizar_y_pintar_explosiones():
    for explosion in lista_explosiones:
        # Pinto la explosion
        screen.blit(explosion_bites[explosion[0]], (explosion[1], explosion[2]))
        # Actualizo la explosion
        if explosion[0] < len(explosion_bites) - 1:
            explosion[0] += 1
        else:
            lista_explosiones.remove(explosion)


# ------------------------------ Chequear impactos de disparos rojos ---------------------------------- #
def chequea_colision_impactos(lista_objetos, lista_lasers_rojos):
    # Chequeamos para cada laser
    for laser in lista_lasers_rojos:
        for objeto in lista_objetos:
            # Chequeo altura
            if abs((objeto[2] - laser[2])) < 10:
                # Chequeo horizontal
                ancho_nave = objeto[0].get_width()
                if (laser[1] - objeto[1] > 0) and (laser[1] - objeto[1] < ancho_nave):
                    nueva_explosion(objeto[1], objeto[2])
                    effect = pygame.mixer.Sound('data/ExplosionFighter1.wav')
                    effect.play()
                    lista_objetos.remove(objeto)
                    # Veo qué jugador disparó el laser
                    id_player = laser[3]
                    # Sumo los puntos
                    for player in lista_jugadores:
                        if player[3] == id_player: player[6] += puntos_a_sumar
                    lista_laseres_rojos.remove(laser)
                    return True


# ------------------------------ Chequear impacto de disparo en player -------------------------------- #
def chequea_impacto_en_jugador(lst_jugadores, lst_lasers_verdes):
    # Chequeamos para cada laser
    for laser in lst_lasers_verdes:
        for jugador in lst_jugadores:
            # Chequeo altura
            if abs((jugador[2] - laser[2])) < 10:
                ancho_nave = jugador[0].get_width()
                if (laser[1] - jugador[1] > 0) and (laser[1] - jugador[1] < ancho_nave):
                    nueva_explosion(jugador[1], jugador[2])
                    effect = pygame.mixer.Sound('data/ExplosionFighter1.wav')
                    effect.play()
                    lista_jugadores.remove(jugador)


# ------------------------------ Actualiza lista aparación enemigos ----------------------------------- #
def actualiza_aparicion_ties():
    if saturacion_tiempo_ties[0] < saturacion_tiempo_ties[1]:
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


# ------------------------------ Insertar nueva nave IA ----------------------------------------------- #
def inserta_nave_ia(img_nave, pos_x, pos_y, lista_objetos):
    lista_objetos.append([img_nave, pos_x, pos_y])


# ------------------------------ Insertar nuevo jugador ----------------------------------------------- #
def insertar_nuevo_jugador(img_nave, pos_x, posy, new_id, estado_animacion, tiempo_animacion, puntos):
    lista_jugadores.append([img_nave, pos_x, posy, new_id, estado_animacion, tiempo_animacion, puntos])


# ------------------------------ player dispara un láser ---------------------------------------------- #
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


# ------------------------------ enemigos disparan un láser ------------------------------------------- #
def disparar_laser_enemigos(posx, posy, lista_objetos):
    # Dispara
    lista_objetos.append([laser_verde, posx + 15, posy + 15])
    lista_objetos.append([laser_verde, posx + 21, posy + 15])
    # Emito sonido
    effect = pygame.mixer.Sound('data/EmpireLaserTurbo.wav')
    effect.play()


# ------------------------------ Control de tiempos de disparo / enfriamiento de armas ---------------- #
def actualiza_saturacion_disparos():
    if saturacion_disparo_player[0] < saturacion_disparo:
        saturacion_disparo_player[0] += 1
    if saturacion_disparo_player[1] < saturacion_disparo:
        saturacion_disparo_player[1] += 1


# ------------------------------ Actualizar posición objetos en movimiento ---------------------------- #
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
                if random.randint(0, 100) == 100:
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


# ------------------------------ insertamos un nuevo jugador humano ----------------------------------- #
def crear_nuevo_jugador(lst_jugadores, pos_x, pos_y, new_id):
    # Chequeamos que no esté ya jugando
    existe = False
    for new_jugador in lst_jugadores:
        if new_jugador[3] == new_id:
            existe = True
    if not existe:
        # Creamos jugador_1 con img_xwing, pos_x, pos_y, id player 1 y estado animación 15 y puntos
        insertar_nuevo_jugador(img_xwing, pos_x, pos_y, new_id, 15, tiempo_anim_giro, 0)


# ------------------------------ Cargador de gráficos del juego --- ----------------------------------- #
def cargar_graficos_juego():
    # Lo vamos a hacer en un único bloque TRY. Si falla la carga, no arrancamos el juego.
    # La idea es no arrancar el juego con gráficos no cargados.
    global img_tief, img_shuttle, img_stroopers, img_falconm, img_corveta, laser_verde, laser_rojo, fondo
    graficos_cargados = True
    try:
        # Cargamos animaciones de los PJs
        for x_grp in range(0, len(grf_lst_xwing)):
            img_xwing_lista.append(pygame.image.load(grf_lst_xwing[x_grp]))
        # Cargamos la aminación de la explosión
        for e_grp in range(0, len(grf_lst_explosion)):
            explosion_bites.append(pygame.image.load(grf_lst_explosion[e_grp]))
        # Cargamos las imágenes estáticas
        img_tief = pygame.image.load(grf_tief)
        img_shuttle = pygame.image.load(grf_shuttle)
        img_stroopers = pygame.image.load(grf_stroopers)
        img_falconm = pygame.image.load(grf_falconm)
        img_corveta = pygame.image.load(grf_corveta)
        laser_verde = pygame.image.load(grf_laser_verde)
        laser_rojo = pygame.image.load(grf_laser_rojo)
        fondo = pygame.image.load(grf_fondo)
    except FileNotFoundError:
        # Si hay algún error, no cargamos el juego!
        print("Ha ocurrido una excepción grafica")
        graficos_cargados = False
    finally:
        # Devolvemos el resultado de la carga de gráficos
        return graficos_cargados


# ------------------------------ MAIN ----------------------------------------------------------------- #
# Primero intentamos cargar los gráficos.
graficos_correctos = cargar_graficos_juego()
# Si no se han cargado, no creamos la GUI, salimos directamente.
if graficos_correctos:
    # Creamos las listas para almacenar objetos del juego.
    # Lista para control de jugadores humanos
    img_xwing = img_xwing_lista[2]
    # Lista para control de enfriamiento de armas de los jugadores humanos
    saturacion_disparo_player = [saturacion_disparo, saturacion_disparo]
    # Lista de naves aleatorias a elegir por la dinámica del juego.
    lista_naves_aleatorias = [img_falconm, img_corveta]
    # Listas de objetos para actualizar, animar y chequear colisiones
    lista_objetos_enemigos = []
    lista_laseres_verdes = []
    lista_laseres_rojos = []
    lista_naves_adorno = []
    lista_explosiones = []
    lista_jugadores = []
    # Inicializamos en el entorno de Pygame
    pygame.init()
    # También el uso de letras
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', size_letra)
    # Texto de la ventana
    pygame.display.set_caption('Python Wars!')
    # Un poco de música emotiva
    try:
        pygame.mixer.music.load('data/backgroundmusic.ogg')
    except FileNotFoundError:
        print("Archivo de música no encontrado.")
    else:
        # Le damos al play a la música!
        pygame.mixer.music.play(0)

    # Iniciamos la pantalla
    screen = pygame.display.set_mode((alto_pantalla, ancho_pantalla))
    # Creamos jugador_1 con img_xwing, posx, posy, id player 1 y estado animación 15.
    # tiempos entre frames de animaciones y puntos de inicio.
    crear_nuevo_jugador(lista_jugadores, 375, 500, 1)
    done = False
    # Asignamos el reloj de pyGame para el control de frames.
    clock = pygame.time.Clock()
    # Declaramos la variable para salir del juego.
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
            # Creamos jugador_2 con img_xwing, pos_x, pos_y, id player 2 y estado animación 15 y puntos
            crear_nuevo_jugador(lista_jugadores, 500, 500, 2)
            # Lo habilitamos para jugar
            player_2 = True
        if pressed[pygame.K_r]:
            # Creamos jugador_1 con img_xwing, pos_x, pos_y, id player 1 y estado animación 15 y puntos
            crear_nuevo_jugador(lista_jugadores, 370, 500, 1)
        # Movimientos de los jugadores
        for jugador in lista_jugadores:
            # Saco ese jugador (Esto se puede mejorar, pero pierdo claridad
            x = jugador[1]
            y = jugador[2]
            # Dependiendo del jugador que sea, se usan unas teclas u otras
            if jugador[3] == 1:
                # Es player 1
                if pressed[pygame.K_UP] and y > 0:
                    y -= 4
                if pressed[pygame.K_DOWN] and y < ancho_pantalla - 80:
                    y += 4
                if pressed[pygame.K_LEFT] and x > 0:
                    x -= 4
                    actualiza_animacion_direccion_jugador(jugador, "izquierda")
                if pressed[pygame.K_RIGHT] and x < alto_pantalla - 58:
                    x += 4
                    actualiza_animacion_direccion_jugador(jugador, "derecha")
                if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                    actualiza_animacion_direccion_jugador(jugador, "centro")
                if pressed[pygame.K_RSHIFT]:
                    dispara_laser(x, y, lista_laseres_rojos, 1)
                if pressed[pygame.K_v]:
                    pasada_de_nave_adorno(img_corveta)
            elif jugador[3] == 2:
                # Es player 2
                if pressed[pygame.K_w] and y > 0:
                    y -= 4
                if pressed[pygame.K_s] and y < ancho_pantalla - 80:
                    y += 4
                if pressed[pygame.K_a] and x > 0:
                    x -= 4
                    actualiza_animacion_direccion_jugador(jugador, "izquierda")
                if pressed[pygame.K_d] and x < alto_pantalla - 58:
                    x += 4
                    actualiza_animacion_direccion_jugador(jugador, "derecha")
                if not pressed[pygame.K_d] and not pressed[pygame.K_a]:
                    actualiza_animacion_direccion_jugador(jugador, "centro")
                if pressed[pygame.K_LSHIFT]:
                    dispara_laser(x, y, lista_laseres_rojos, 2)
            # asignamos los nuevos valores
            # guardamos los nuevos valores de posición
            jugador[1] = x
            jugador[2] = y
        # Dibujamos/Actualizamos la lista de objetos dinámicos
        # ¡¡Van en orden de capa de pintado!! Para controlar quién aparece arriba o abajo cuando se superponen
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
        # Pintamos los textos en pantalla (va en la ultima capa)
        for jugador in lista_jugadores:
            pintar_puntos_pantalla(jugador)
        # Chequeamos triggers
        if chequea_colision_impactos(lista_objetos_enemigos, lista_laseres_rojos):
            naves_destruidas += 1
            random_naves_aleatoras(naves_destruidas)
        actualiza_aparicion_ties()
        # Muestro pantalla y actualizo reloj
        pygame.display.flip()
        clock.tick(60)
        # Veo si se ha activado el evento de salir del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.display.quit()
                sys.exit()
else:
    # Salimos por que no se han cargado bien los gráficos
    print("Error al cargar los gráficos el juego. Saliendo...")
