import pygame as pg
from the_quest import Max_time
from the_quest.entities import Asteroids, Spaceship
import random
import math

pg.init()
class Game:
    def __init__(self):
        self.main_screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("THE QUEST") 
        self.background = pg.image.load("the_quest/images/James-Webb-Peers-Into-TRAPPIST-1-a-Star-System-Full-of.jpeg").convert()
        self.background_endlevel = pg.image.load("the_quest/images/James-Webb-Peers-Into-TRAPPIST-1-a-Star-System-Full-of.jpeg").convert()
        self.background_width = self.background.get_width()
        self.clock = pg.time.Clock()
        self.timer = Max_time
        self.lives = 3
        self.x = 0
        self.y = 0
        self.livesMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 40)
        self.timerMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 20)
        self.spaceship = Spaceship(60, 5)
        self.game_over = False
        
    def mainloop(self):
        self.FPS = 50
        self.asteroidsCount = 0
        self.asteroids = []
        for i in range(5):
            asteroid = Asteroids(1)
            asteroid.speed(-5)
            self.asteroids.append(asteroid)
            i += 1
       
        while not self.game_over:
            game_time = self.clock.tick(self.FPS)
            self.timer -= game_time
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
        
            self.main_screen.blit(self.background, (self.x, self.y))
        
            for asteroid in self.asteroids:
                asteroid.update(800, 600)
                asteroid.draw(self.main_screen)
                #if asteroid.center_x < 0 - asteroid.w:
                    #self.asteroids.pop(self.asteroids.index(asteroid))
                if asteroid.left <= self.spaceship.right and asteroid.down >= self.spaceship.up and asteroid.up <= self.spaceship.down and asteroid.left >= self.spaceship.left:
                    self.lives -= 1
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    if self.lives == 2 or self.lives == 1:
                        asteroid = Asteroids(1)
                        asteroid.speed(-5)
                        self.asteroids.append(asteroid)
                    if self.lives == 0:
                       self.game_over = True

                if self.timer <= 0:
                    self.x -= 1
                    if self.x <= -500:
                        self.main_screen.blit(self.background, (-500, 0))
                        self.spaceship.center_x += 1
                        if self.spaceship.center_x >= 500:
                            self.spaceship.center_x = 500
                            #fin de nivel
                
            
            self.spaceship.move(pg.K_UP, pg.K_DOWN)
            self.spaceship.draw(self.main_screen)
            #sprites.update(800, 600)
            #sprites.draw(self.main_screen)
            
            p1 = self.livesMarker.render("Lives: " + str(self.lives), True, (255, 255, 0))
            t1 = self.timerMarker.render(str(self.timer / 1000), True, (255, 255, 0))
            self.main_screen.blit(p1, (10,10))
            self.main_screen.blit(t1, (650,10))
            pg.display.update()
            pg.display.flip()

        pg.quit()