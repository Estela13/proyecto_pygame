import pygame as pg
import random
from entities import Asteroids, Spaceship


pg.init()

main_screen = pg.display.set_mode((800, 600))
pg.display.set_caption("THE QUEST")
background = pg.image.load("/Users/estelafugaz/Desktop/Proyecto final/images/starbg.png")

spaceship = Spaceship()
spaceship.speed(1, 1)
clock = pg.time.Clock()
FPS = 60

asteroids = []
for i in range(random.randint(5, 30)):
    asteroid = Asteroids(800, center_y=random.randint(200, 600), radio = random.randint(5, 10), color = (random.randint(0,255), random.randint(0,255),random.randint (0, 255)))
    asteroid.speed(random.randint(-2, 3), (-2, 4))
    asteroids.append(asteroid)
    i += 1
game_over = False


while not game_over:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        

    main_screen.blit(background, (0, 0))
    for asteroid in asteroids:
        asteroid.draw(main_screen)
        asteroid.move()
    
    spaceship.move(pg.K_UP, pg.K_DOWN)
   
    spaceship.draw(main_screen)
    

    pg.display.flip()

pg.quit()

