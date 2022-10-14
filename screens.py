import pygame as pg
from entities import Asteroids, Spaceship
import random

pg.init()
class Game:
    def __init__(self):
        self.main_screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("THE QUEST") 
        self.background = pg.image.load("images/starbg.png").convert()
        self.background_width = self.background.get_width()
        self.clock = pg.time.Clock()
        self.lives = 3
        self.livesMarker = pg.font.Font("fonts/PEOPLE BOOK.otf", 40)
        self.spaceship = Spaceship(5)
        
    def mainloop(self):
        self.FPS = 50
        self.asteroids = []
        self.asteroidsCount = 0
        for i in range(5):
            asteroid = Asteroids(1)
            asteroid.speed(-5)
            self.asteroids.append(asteroid)
            i += 1

        self.game_over = False

        while not self.game_over:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = True
            
            
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
        
            self.main_screen.blit(self.background, (0, 0))
        
            for asteroid in self.asteroids:
                points = asteroid.move(800, 600)
                asteroid.draw(self.main_screen)
                if asteroid.left <= self.spaceship.right and asteroid.down >= self.spaceship.up and asteroid.up <= self.spaceship.down and asteroid.left >= self.spaceship.left:
                    self.lives -= 1
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    if self.lives == 2 or self.lives == 1:
                        asteroid = Asteroids(1)
                        asteroid.speed(-5)
                        self.asteroids.append(asteroid)
                    if self.lives == 0:
                        self.game_over = True
                
            
            self.spaceship.move(pg.K_UP, pg.K_DOWN)
            self.spaceship.draw(self.main_screen)
            
            p1 = self.livesMarker.render("Lives: " + str(self.lives), True, (255, 255, 0))
            self.main_screen.blit(p1, (10,10))
            pg.display.update()
            pg.display.flip()

        pg.quit()