import pygame as pg
import random
from entities import Asteroids, Nave


pg.init()

main_screen = pg.display.set_mode((800, 600))
pg.display.set_caption("THE QUEST")

asteroids = Asteroids(800, 300)
asteroids.velocidad(-1, 0)
nave = Nave()
nave.velocidad(1, 1)

"""
x = 20
y = 240
vx = 1
vy = 1
w = 25
h = 60
"""
game_over = False

while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        


    main_screen.fill((100, 0, 255))
    asteroids.mover()
    nave.mover(pg.K_UP, pg.K_DOWN)
    """
    y += vy

    if y <= 0 or y >= 600 - h:
        vy *= - 1
    """
    nave.dibujar(main_screen)
    asteroids.dibujar(main_screen)
    pg.display.flip()

pg.quit()

