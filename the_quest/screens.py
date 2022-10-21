import pygame as pg
from the_quest import Max_time, screen_height, screen_width
from the_quest.entities import Asteroids, Spaceship, Explosion
import random
import math


pg.init()
class Game:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("THE QUEST") 
        self.background = pg.image.load("the_quest/images/71ZRmajgshL._AC_SL1500_%20Edited Edited.jpeg").convert()
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
        self.music = pg.mixer.Sound("the_quest/sound/sound explosion.zip")
        self.explosion_group = pg.sprite.Group() 

    def mainloop(self, level):
        self.FPS = 50
        self.asteroidsCount = 0
        self.asteroids = []
        self.level = level
 
        if self.level == 1:
            for i in range(5):
                asteroid = Asteroids(1)
                asteroid.speed(-5)
                self.asteroids.append(asteroid)
                i += 1
        elif self.level == 2:
            for i in range(4):
                asteroid = Asteroids(2)
                asteroid.speed(-5)
                self.asteroids.append(asteroid)
                i += 1
       
        while not self.game_over:

            game_time = self.clock.tick(self.FPS)
            self.timer -= game_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = True
        
            self.main_screen.blit(self.background, (self.x, self.y))
    
            for asteroid in self.asteroids:
                asteroid.update()
                asteroid.draw(self.main_screen)
                if asteroid.left <= 0 - asteroid.w:
                    self.asteroidsCount+= 1 / 5
        
                if asteroid.left <= self.spaceship.right and asteroid.down >= self.spaceship.up and asteroid.up <= self.spaceship.down and asteroid.left >= self.spaceship.left:
                    self.music.play(-1)
                    self.lives -= 1
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    self.explosion = Explosion(self.spaceship.center_x, self.spaceship.center_y)
                    self.explosion_group.add(self.explosion)
                    self.music.stop()
                    self.spaceship.remove()
                    self.spaceship = Spaceship()
      
                    if self.lives == 2 or self.lives == 1:
                        if self.level == 1:
                            asteroid = Asteroids(1)
                        elif self.level == 2:
                            asteroid = Asteroids(2)
                        asteroid.speed(-5)
                        self.asteroids.append(asteroid)
                    if self.lives == 0:
                        self.game_over = True
                        
                if self.timer <= 0:
                    self.timer = 0
                    asteroid.vx *= -1
                    asteroid.speed(8)
                    self.x -= 1
                    if self.x <= -500:
                        self.main_screen.blit(self.background, (-500, 0))
                        self.spaceship.center_x += 1
                        self.spaceship.img = self.spaceship.flipped
                        if self.spaceship.center_x >= 500:
                            self.spaceship.center_x = 500      
                            
                        #puntuación si aterriza en el planeta        
                        #if self.spaceship.center_y <= 400 and self.spaceship.center_y >= 100:
                            #self.asteroidsCount += 15        
                        p2 = self.pointsMarker.render("PRESS ENTER TO NEXT LEVEL or ESC TO PLAY AGAIN: ", True, (255, 255, 255))
                        self.main_screen.blit(p2, (10, 300))
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_RETURN:
                                gameagain = Game()
                                gameagain.mainloop(2)
                            if event.key == pg.K_ESCAPE:
                                game = Game()
                                game.mainloop(1)
                            #fin de nivel
                
            self.spaceship.draw(self.main_screen)
            self.spaceship.move(pg.K_UP, pg.K_DOWN)
            self.explosion_group.draw(self.main_screen)
            self.explosion_group.update()
    
            
            l1 = self.livesMarker.render("Lives: " + str(self.lives), True, (255, 255, 0))
            t1 = self.timerMarker.render(str(round(self.timer / 1000, 2)), True, (255, 255, 0))
            p1 = self.pointsMarker.render("Points: " + str(round(self.asteroidsCount)), True, (255, 255, 255))
            self.main_screen.blit(l1, (300, 20))
            self.main_screen.blit(t1, (650,10))
            self.main_screen.blit(p1, (10, 20))
            pg.display.update()
            pg.display.flip()

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
                        game.mainloop(1)


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
    
class Game_over(Game):

    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("GAME OVER")

    def mainloop(self):
        while not self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game = Game()
                    if self.level == 1:
                        game.mainloop(1)
                    if self.level == 2:
                        game.mainloop(2)

        self.main_screen.blit(self.background, (-500, 0))
        p2 = self.pointsMarker.render("PRESS ENTER PLAY AGAIN: ", True, (255, 255, 255))
        self.main_screen.blit(p2, (10, 300))
        pg.display.flip()