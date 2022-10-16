import pygame as pg
from the_quest import Max_time, screen_height, screen_width
from the_quest.entities import Asteroids, Spaceship
import random
import math

pg.init()
class Game:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("THE QUEST") 
        self.background = pg.image.load("the_quest/images/71ZRmajgshL._AC_SL1500_%20Edited Edited.jpeg").convert()
        self.background_endlevel = pg.image.load("the_quest/images/James-Webb-Peers-Into-TRAPPIST-1-a-Star-System-Full-of.jpeg").convert()
        self.background_width = self.background.get_width()
        self.clock = pg.time.Clock()
        self.timer = Max_time
        self.lives = 3
        self.x = 0
        self.y = 0
        self.livesMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 20)
        self.timerMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 20)
        self.pointsMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 25)
        self.spaceship = Spaceship()
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
            self.points = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = True
            
            
            """
            #no se comporta como quiero, revisar
            #aumento la velocidad si mantengo pulsado
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.spaceship.vy += 4
                    if event.key == pg.K_DOWN:
                        self.spaceship.vy += 4
        
            # El usuario suelta la tecla
                if event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        self.spaceship.vy = 1
                    if event.key == pg.K_DOWN:
                        self.spaceship.vy = 1
            """
            
        
            self.main_screen.blit(self.background, (self.x, self.y))
        
            for asteroid in self.asteroids:
                asteroid.update(800, 600)
                asteroid.draw(self.main_screen)
                if asteroid.left <= 0 - asteroid.w:
                    self.asteroidsCount+= 1 / 5
        
                if asteroid.left <= self.spaceship.right and asteroid.down >= self.spaceship.up and asteroid.up <= self.spaceship.down and asteroid.left >= self.spaceship.left:
                    self.lives -= 1
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    if self.lives == 2 or self.lives == 1:
                        asteroid = Asteroids(1)
                        asteroid.speed(-5)
                        self.asteroids.append(asteroid)
                    if self.lives == 0:
                        #p2 = self.livesMarker.render(str("GAME OVER"), True, (255, 255, 255))
                        #self.main_screen.blit(p2, (400,300))
                        self.game_over = True
                    

                if self.timer <= 0:
                    self.timer = 0
                    asteroid.vx *= -1
                    asteroid.speed(8)
                    self.x -= 1
                    if self.x <= -500:
                        self.main_screen.blit(self.background, (-500, 0))
                        self.spaceship.center_x += 1
                        if self.spaceship.center_x >= 500:
                            self.asteroidsCount = + 10
                            self.spaceship.center_x = 500
                            game = EndLevel()
                            game.mainloop()
                            #fin de nivel
                
            
            self.spaceship.move(pg.K_UP, pg.K_DOWN)
            self.spaceship.draw(self.main_screen)
           
            
            l1 = self.livesMarker.render("Lives: " + str(self.lives), True, (255, 255, 0))
            t1 = self.timerMarker.render(str(self.timer / 1000), True, (255, 255, 0))
            p1 = self.pointsMarker.render("Points: " + str(round(self.asteroidsCount)), True, (255, 255, 255))
            self.main_screen.blit(l1, (300, 20))
            self.main_screen.blit(t1, (650,10))
            self.main_screen.blit(p1, (10, 20))
            pg.display.update()
            pg.display.flip()

    def level2(Game):
        pass
        


        pg.quit()


class Menu:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("MENU")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("the_quest/images/colorful-galaxy-digital-art.jpeg")
        self.startFont =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)
    
    def mainloop(self):
        game_over = False

        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game = Game()
                        game.mainloop()


            self.main_screen.blit(self.background, (0, 0))
            menu = self.startFont.render("Press ENTER to START", True, (255, 255, 255))
            self.main_screen.blit(menu, (180, 500))
            pg.display.flip()

class Records:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("RECORDS")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("the_quest/images/colorful-galaxy-digital-art.jpeg")
        self.startFont =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)
    
    def mainloop(self):
        game_over = False

        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game_over = True


            self.main_screen.blit(self.background, (0, 0))
            records = self.startFont.render("Your puntuation is", True, (255, 255, 255))
            self.main_screen.blit(records, (200, 500))
            pg.display.flip()
    
class EndLevel:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("END")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("the_quest/images/71ZRmajgshL._AC_SL1500_%20Edited Edited.jpeg").convert()
        self.startFont =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)
        self.spaceship2 = Spaceship(500, 100) 
    def mainloop(self):
        game_over = False
       
        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game = Game()
                        game.mainloop()
                        
                

            
            self.main_screen.blit(self.background, (-500, 0))
            records = self.startFont.render("Press Enter to continue", True, (255, 255, 255))
            self.main_screen.blit(records, (10, 10))
            self.spaceship2.draw(self.main_screen)
            pg.display.flip()
