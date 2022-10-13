from asyncio import AbstractEventLoop
import math
import pygame as pg
import random
from entities import Asteroids, Spaceship

pg.init()

main_screen = pg.display.set_mode((800, 600))
pg.display.set_caption("THE QUEST")
background = pg.image.load("images/starbg.png").convert()
background_width = background.get_width()
spaceship = Spaceship(2)
lives = 3
livesMarker = pg.font.Font("fonts/PEOPLE BOOK.otf", 40)
clock = pg.time.Clock()
FPS = 50
asteroids = []

for i in range(5):
    asteroid = Asteroids(1)
    asteroid.speed(-5)
    asteroids.append(asteroid)
    i += 1

game_over = False

while not game_over:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
    
    """
    no se comporta como quiero, revisar
    #aumento la velocidad si mantengo pulsado
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                spaceship.vy += 4
            if event.key == pg.K_DOWN:
                spaceship.vy += 4
 
    # El usuario suelta la tecla
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                spaceship.vy = 1
            if event.key == pg.K_DOWN:
                spaceship.vy = 1
    """
   
    main_screen.blit(background, (0, 0))
   
    for asteroid in asteroids:
        asteroid.move(800, 600)
        asteroid.draw(main_screen)
        if asteroid.left <= spaceship.right and asteroid.down >= spaceship.up and asteroid.up <= spaceship.down and asteroid.left >= spaceship.left:
            lives -= 1
            asteroids.pop(asteroids.index(asteroid))
            if lives == 2 or lives == 1:
                asteroid = Asteroids(1)
                asteroid.speed(-5)
                asteroids.append(asteroid)
            if lives == 0:
                game_over = True
                
    
    spaceship.move(pg.K_UP, pg.K_DOWN)
    spaceship.draw(main_screen)
    
    p1 = livesMarker.render("Lives: " + str(lives), True, (255, 255, 0))
    main_screen.blit(p1, (10,10))
    pg.display.update()
    pg.display.flip()

pg.quit()

