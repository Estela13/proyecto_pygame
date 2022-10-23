import sqlite3
import pygame as pg
from the_quest import Max_time, screen_height, screen_width
from the_quest.entities import Asteroids, Spaceship, Explosion
import random
import sys
from the_quest.button import Button


pg.init()
class Game:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("THE QUEST") 
        self.background = pg.image.load("the_quest/images/backgroundplanet.jpeg").convert()
        self.bg2 = pg.image.load("the_quest/images/opppp3 Edited.jpeg").convert()
        self.background_width = self.background.get_width()
        self.clock = pg.time.Clock()
        self.timer = Max_time
        self.lives = 3
        self.x = 0
        self.y = 0
        self.livesMarker = pg.image.load("the_quest/images/heart.png")
        self.warning = pg.transform.scale(pg.image.load("the_quest/images/virus warning.png"), (35,35))
        self.timerMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 20)
        self.pointsMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 25)
        self.spaceship = Spaceship()
        self.game_over = False
        self.end_music = pg.mixer.Sound("the_quest/sound/01 game-game_0.ogg")
        self.music = pg.mixer.Sound("the_quest/sound/SFX_Explosion_02.wav")
        self.explosion_group = pg.sprite.Group() 

    def mainloop(self, level):
        self.FPS = 50
        self.asteroidsCount = 0
        self.asteroids = []
        self.level = level
        self.end_music.set_volume(0.1)
 
        if self.level == 1:
            for i in range(5):
                asteroid = Asteroids(random.randint(1,2))
                asteroid.speed(random.randint(3,6))
                self.asteroids.append(asteroid)
                i += 1
        elif self.level == 2:
            self.background = self.bg2
            for i in range(4):
                asteroid = Asteroids(random.randint(1,3))
                asteroid.speed(random.randint(5,8))
                self.asteroids.append(asteroid)
                i += 1
    
       
        while not self.game_over:

            game_time = self.clock.tick(self.FPS)
            self.timer -= game_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        
            self.main_screen.blit(self.background, (self.x, self.y))
    
            for asteroid in self.asteroids:
                asteroid.update()
                asteroid.draw(self.main_screen)
                if asteroid.left <= 0 - asteroid.w:
                    self.asteroidsCount+= 1 / 5
        
                if asteroid.left <= self.spaceship.right and asteroid.down >= self.spaceship.up and asteroid.up <= self.spaceship.down and asteroid.left >= self.spaceship.left:
                    self.music.play()
                    self.lives -= 1
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    self.explosion = Explosion(self.spaceship.center_x, self.spaceship.center_y)
                    self.explosion_group.add(self.explosion)
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
                    asteroid.speed(-9)
                    self.x -= 1
                    if self.x <= -500:
                        self.spaceship.vy = 0
                        self.spaceship.img = self.spaceship.flipped
                        self.main_screen.blit(self.background, (-500, 0))
                        self.spaceship.center_x += 1
                        if self.spaceship.center_x >= 500:
                            self.spaceship.center_x = 500   
                        p2 = self.pointsMarker.render("PRESS ENTER TO NEXT LEVEL ", True, (255, 255, 0))
                        self.main_screen.blit(p2, (200, 300))
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_RETURN:
                                self.end_music.stop()
                                gameagain = Game()
                                gameagain.mainloop(2)
                            if event.key == pg.K_ESCAPE:
                                self.end_music.stop()
                                game = Game()
                                game.mainloop(1)
                            #fin de nivel
                    
                
           
            self.spaceship.draw(self.main_screen)
            self.spaceship.move(pg.K_UP, pg.K_DOWN)
            self.explosion_group.draw(self.main_screen)
            self.explosion_group.update()

            self.main_screen.blit(self.livesMarker, (670,25))
            self.main_screen.blit(self.livesMarker, (700,25))
            self.main_screen.blit(self.livesMarker, (730, 25))
            if self.lives == 2:
                self.main_screen.blit(self.warning, (678,33))
            if self.lives == 1:
                self.main_screen.blit(self.warning, (678,33))
                self.main_screen.blit(self.warning, (708,33))
            t1 = self.timerMarker.render(str(round(self.timer / 1000, 2)), True, (255, 255, 0))
            p1 = self.pointsMarker.render("Score: " + str(round(self.asteroidsCount)), True, (255, 255, 255))
            self.main_screen.blit(t1, (720,8))
            self.main_screen.blit(p1, (10, 20))
            pg.display.update()
            pg.display.flip()

        pg.quit()


class Menu():
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("MENU")
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(pg.image.load("the_quest/images/op2.jpeg"),(800,600))
        self.titleFont= pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 90)
        self.menuFont = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 50)
        self.startFont =  pg.font.Font("the_quest/fonts/PermanentMarker-Regular.ttf", 40)
        self.music = pg.mixer.Sound("the_quest/sound/00 intro_0.ogg")
        
    def mainloop(self):
        game_over = False
       
        while not game_over:
            self.music.play(-1)
            self.music.set_volume(0.1)
            self.main_screen.blit(self.background, (0,0))
            menu_mouse = pg.mouse.get_pos()
            title_text = self.titleFont.render("THE QUEST", True, "#b68f40")
            self.main_screen.blit(title_text, (125, 10))
            menu_text = self.menuFont.render("MAIN MENU", True, "#DEB887")
            menu_rect = menu_text.get_rect(center=(390, 150))
            play_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(250,100)), pos=(400, 250), 
                            text_input="PLAY", font=self.startFont, base_color="#d7fcd4", hovering_color="White")
            instrutions_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(350,100)), pos=(400, 370), 
                            text_input="HOW TO PLAY", font=self.startFont, base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(250,100)), pos=(400, 490), 
                            text_input="QUIT", font=self.startFont, base_color="#d7fcd4", hovering_color="White")

            self.main_screen.blit(menu_text, menu_rect)
            for button in [play_button, instrutions_button, quit_button]:
                button.changeColor(menu_mouse)
                button.update(self.main_screen)

        
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.music.stop()
                    if play_button.checkForInput(menu_mouse):
                        game = Game()
                        game.mainloop(1)
                    if instrutions_button.checkForInput(menu_mouse):
                        intro = Instructions()
                        intro.mainloop()
                    if quit_button.checkForInput(menu_mouse):
                        pg.quit()
                        sys.exit()

            pg.display.update()
      


class Records:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("RECORDS")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("the_quest/images/colorful-galaxy-digital-art.jpeg")
        self.title =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)

    def mainloop(self):
        game_over = False

        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game_over = True


            self.main_screen.blit(self.background, (0, 0))
            records = self.startFont.render("Your puntuation is", True, (255, 255, 255))
            self.main_screen.blit(records, (200, 500))
            pg.display.flip()
    
class Instructions:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("INSTRUCTIONS")
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(pg.image.load("the_quest/images/op2.jpeg"),(800,600))
        self.startFont =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)
        self.rect = pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(700,400))
        self.textFont = pg.font.Font("the_quest/fonts/PTSans-Regular.ttf", 17)
        self.music = pg.mixer.Sound("the_quest/sound/00 intro_0.ogg")
    def mainloop(self):
        game_over = False
        pg.font.init()
       
        while not game_over:
            self.music.play(-1)
            self.music.set_volume(0.1)
            self.main_screen.blit(self.background, (0,0))
            
            menu_mouse = pg.mouse.get_pos()
            
            play_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(100,80)), pos=(200, 100), 
                        text_input="PLAY", font=self.startFont, base_color="#d7fcd4", hovering_color="White")
            back_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(100,80)), pos=(80, 100), 
                            text_input="BACK", font=self.startFont, base_color="#d7fcd4", hovering_color="White")
            for button in [play_button, back_button]:
                button.changeColor(menu_mouse)
                button.update(self.main_screen)
            text = self.startFont.render("Instructions", True, "#b68f40")
            text_rect = text.get_rect(center=(400, 100))
            text_instru = self.textFont.render("The Quest game. You are in outta space searching for new planets to conqueer.", True, (0,0,0))
            text_instru2 = self.textFont.render("You've got 3 lives in each level, if you collide with an asteroid you'll lose one of those lives.", True, (0,0,0))
            text_instru_ = self.textFont.render("You have to survive 30 seconds on each level without losing your 3 lives.", True, (0,0,0))
            text_instru_2 = self.textFont.render("To move your spaceship you'll use the key arrow UP and DOWN.", True, (0,0,0))
            text_instru_4 = self.textFont.render("The more asteroids you pass without colliding the bigger score you'll get.", True, (0,0,0))
            text_instru4 = self.textFont.render("At the end of the level you will land in a new planet you've discovered.", True, (0,0,0))
            text_instru5 = self.textFont.render("If you lose your 3 lives it will be GAME OVER. The level will restart automatically.", True, (0,0,0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.music.stop()
                    if back_button.checkForInput(menu_mouse):
                        menu = Menu()
                        menu.mainloop()
                    if play_button.checkForInput(menu_mouse):
                        game = Game()
                        game.mainloop(1)
            self.main_screen.blit(text, text_rect)
            self.main_screen.blit(self.rect, (50,150))
            self.main_screen.blit(text_instru, (70, 200))
            self.main_screen.blit(text_instru2, (70, 235))
            self.main_screen.blit(text_instru_, (70, 265))
            self.main_screen.blit(text_instru_2, (70, 295))
            self.main_screen.blit(text_instru_4, (70, 325))
            self.main_screen.blit(text_instru4, (70, 355))
            self.main_screen.blit(text_instru5, (70, 385))

           
            pg.display.flip()
    
class EndLevel:
    def __init__(self):
        self.main_screen = pg.display.set_mode((screen_height, screen_width))
        pg.display.set_caption("END")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("the_quest/images/backgroundplanet.jpeg").convert()
        self.startFont =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)
        self.spaceship = Spaceship() 
        self.angle = 0
        self.img0 = pg.transform.scale(pg.image.load("the_quest/images/blueships1.png"),(100,80))
        self.img1 = pg.transform.rotate(self.img0 , self.angle) 
        self.rect0 = self.img0.get_rect()
        center_x = 60
        center_y = 600 // 2
        self.rect0.center = center_x , center_y
        self.runing = False
        self.x = 0
        self.y = 0
        self.end_music = pg.mixer.Sound("the_quest/sound/01 game-game_0.ogg")
        self.pointsMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 25)
    def mainloop(self):
        game_over = False
       
        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.end_music.play(-1)
            self.end_music.set_volume(0.1)
            self.x -= 1
            if self.x <= -500:
                self.main_screen.blit(self.background, (-500, 0)) 
                self.runing = True   
                self.spaceship.center_x += 1
                if self.spaceship.center_x >= 500:
                    self.spaceship.center_x = 500  
                 
                p2 = self.pointsMarker.render("PRESS ENTER TO NEXT LEVEL ", True, (255, 255, 0))
                self.main_screen.blit(p2, (200, 300))
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.end_music.stop()
                        gameagain = Game()
                        gameagain.mainloop(2)
                    if event.key == pg.K_ESCAPE:
                        self.end_music.stop()
                        game = Game()
                        game.mainloop(1)
            if self.runing:        
                    self.angle += 1
                    if self.angle % 180 == 0:
                        self.runing = False
            img1 = pg.transform.rotate(self.img0 , self.angle) 
            rect1 = img1.get_rect()
            rect1.center = self.rect0.center
            
            
            self.main_screen.blit(self.background, (self.x, self.y))
            self.main_screen.blit(img1,rect1)
            
            
                    

            pg.display.flip()
