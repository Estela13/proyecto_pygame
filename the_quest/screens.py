
import sqlite3
import pygame as pg
from the_quest import Max_time_game, Max_time_screen, x_max, y_max
from the_quest.entities import Asteroids, Spaceship, Explosion, Button
import random
import sys
import pygame_gui


pg.init()
class Game():
    def __init__(self):
        self.main_screen = pg.display.set_mode((x_max, y_max))
        pg.display.set_caption("THE QUEST") 
        self.background = pg.image.load("the_quest/images/backgroundplanet.jpeg").convert()
        self.bg2 = pg.image.load("the_quest/images/bg_level2.jpeg").convert()
        self.bg3 = pg.image.load("the_quest/images/bg_level3.jpeg").convert()
        self.background_width = self.background.get_width()
        self.clock = pg.time.Clock()
        self.timer = Max_time_game
        self.lives = 3
        self.x = 0
        self.y = 0
        self.livesMarker = pg.transform.scale(pg.image.load("the_quest/images/healthfull.png"), (35,35))
        self.warning = pg.transform.scale(pg.image.load("the_quest/images/health.png"), (35,35))
        self.timerMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 20)
        self.pointsMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 25)
        self.spaceship = Spaceship()
        self.game_over = False
        self.end_music = pg.mixer.Sound("the_quest/sound/01 game-game_0.ogg")
        self.music = pg.mixer.Sound("the_quest/sound/SFX_Explosion_02.wav")
        self.explosion_group = pg.sprite.Group() 
        self.playersGroup = pg.sprite.Group()
        self.playersGroup.add(self.spaceship)
        self.player2Group = pg.sprite.Group()

    def mainloop(self, level, score):
        self.FPS = 50
        self.asteroids = []
        self.level = level
        self.asteroidsCount = score
        self.end_music.set_volume(0.1)
        colliding = True
        
        if self.level == 1:
            self.asteroidsCount = 0
            for i in range(7):
                asteroid = Asteroids(random.randint(1,2))
                asteroid.speed(random.randint(2,4))
                self.asteroids.append(asteroid)
                self.playersGroup.add(asteroid)
                i += 1
                if self.timer == 0:
                    self.asteroids.pop(self.asteroids.index(asteroid))
                    break
        elif self.level == 2:
            self.background = self.bg2
            for i in range(7):
                asteroid = Asteroids(random.randint(1,3))
                asteroid.speed(random.randint(3,6))
                self.playersGroup.add(asteroid)
                self.asteroids.append(asteroid)
                i += 1
        elif self.level == 3:
            self.background = self.bg3
            for i in range(5):
                asteroid = Asteroids(random.randint(2,4))
                asteroid.speed(random.randint(5,7))
                self.playersGroup.add(asteroid)
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
                if colliding:
                    asteroid.update()
                    asteroid.draw(self.main_screen)
                    if asteroid.left <= 0 - asteroid.w:
                        self.asteroidsCount += 1
                else:
                    asteroid.draw(self.main_screen)

                if asteroid.right >= self.spaceship.left and asteroid.left<= self.spaceship.right and \
                asteroid.down >= self.spaceship.up and asteroid.up <= self.spaceship.down:
                    if colliding:
                        self.music.play()
                        self.music.set_volume(0.2)
                        self.lives -= 1
                        self.asteroids.pop(self.asteroids.index(asteroid))
                        self.explosion = Explosion(self.spaceship.center_x, self.spaceship.center_y)
                        self.explosion_group.add(self.explosion)
                        self.spaceship.remove()
                        self.spaceship = Spaceship()

                        if self.lives == 2 or self.lives == 1:
                            if self.level == 1:
                                asteroid = Asteroids(random.randint(1,2))
                            elif self.level == 2:
                                asteroid = Asteroids(random.randint(1,2))
                            elif self.level == 3:
                                asteroid = Asteroids(random.randint(2,3))
                            asteroid.speed(random.randint(5,8))
                            self.asteroids.append(asteroid)
                    
                if self.timer <= 0:
                    colliding = False
                    self.spaceship.center_y = 300
                    asteroid.center_x += -15
                    self.timer = 0
                    self.x -= 0.10
                    if level == 2:
                        if self.x <= -20:
                            end = End(self.asteroidsCount)
                            end.mainloop(2)
                    elif self.x <= -50:
                        end = End(self.asteroidsCount)
                        if level == 1:
                            end.mainloop(1)
                        if level == 3:
                            end.mainloop(3)
                       
                if self.lives == 0:
                    gameover = Game_over()
                    gameover.mainloop()

            self.spaceship.draw(self.main_screen)
            self.spaceship.move(pg.K_UP, pg.K_DOWN)
            if event.type == pg.KEYDOWN:
                self.spaceship.vy += 1
            if event.type == pg.KEYUP:
                self.spaceship.vy = 1
        
            self.explosion_group.draw(self.main_screen)
            self.explosion_group.update()
            if self.lives == 3:
                self.main_screen.blit(self.livesMarker, (675,35))
                self.main_screen.blit(self.livesMarker, (705,35))
                self.main_screen.blit(self.livesMarker, (735, 35))
            if self.lives == 2:
                self.health = self.main_screen.blit(self.warning, (675,35))
                self.main_screen.blit(self.livesMarker, (705,35))
                self.main_screen.blit(self.livesMarker, (735, 35))
            if self.lives == 1:
                self.main_screen.blit(self.warning, (675,35))
                self.main_screen.blit(self.warning, (705,34))
                self.main_screen.blit(self.livesMarker, (735, 35))
            t1 = self.timerMarker.render(str(round(self.timer / 1000, 2)), True, (255, 255, 0))
            p1 = self.pointsMarker.render("Score: " + str(round(self.asteroidsCount)), True, (255, 255, 255))
            self.main_screen.blit(t1, (720,8))
            self.main_screen.blit(p1, (10, 20))
            pg.display.update()
            pg.display.flip()

        pg.quit()

class Menu():
    def __init__(self):
        self.main_screen = pg.display.set_mode((x_max, y_max))
        pg.display.set_caption("MENU")
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(pg.image.load("the_quest/images/menu_bg.webp"),(800,600)).convert()
        self.titleFont= pg.font.Font("the_quest/fonts/SpecialElite-Regular.ttf", 100)
        self.menuFont = pg.font.Font("the_quest/fonts/SpecialElite-Regular.ttf", 55)
        self.startFont =  pg.font.Font("the_quest/fonts/BlackAndWhitePicture-Regular.ttf", 40)
        self.music = pg.mixer.Sound("the_quest/sound/00 intro_0.ogg")
        
    def mainloop(self):
        game_over = False
       
        while not game_over:
            self.music.play(-1)
            self.music.set_volume(0.1)
            self.main_screen.blit(self.background, (0,0))
            menu_mouse = pg.mouse.get_pos()
            title_text = self.titleFont.render("THE QUEST", True, "#b68f40")
            self.main_screen.blit(title_text, (150, 50))
            menu_text = self.menuFont.render("MAIN MENU", True, "#DEB887")
            menu_rect = menu_text.get_rect(center=(395, 190))
            play_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(250,80)), pos=(400, 269), 
                            text_input="PLAY", font=self.startFont, base_color="#b68f40", hovering_color="White")
            instrutions_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(350,80)), pos=(400, 377), 
                            text_input="HOW TO PLAY", font=self.startFont, base_color="#b68f40", hovering_color="White")
            quit_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(250,80)), pos=(400, 485), 
                            text_input="QUIT", font=self.startFont, base_color="#b68f40", hovering_color="White")

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
                        game.mainloop(1, 0)
                    if instrutions_button.checkForInput(menu_mouse):
                        intro = Instructions()
                        intro.mainloop()
                    if quit_button.checkForInput(menu_mouse):
                        pg.quit()
                        sys.exit()

            pg.display.update()
      

class Records():
    def __init__(self):
        self.main_screen = pg.display.set_mode((x_max, y_max))
        pg.display.set_caption("RECORDS")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("the_quest/images/starbg.png")
        self.title =  pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 30)

    def show_records(self):
        conn = sqlite3.connect("Records.db")
        column_space = 100
        i = 30
        cursor = conn.cursor()
        for row in cursor.execute("Select name, score from records order by score desc limit 3"):
            column1 = self.title.render('{:>3}'.format(row[0]), True, (255,255,255))
            column2 = self.title.render('{:30}'.format(row[1]), True, (255,255,255))
            self.main_screen.blit(column1, (120, 150 + i))
            self.main_screen.blit(column2, [5 + column_space, 150 + i])
            i += 30

        
    def mainloop(self):
        game_over = False
        i = 30
        column_space = 200
        
        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game_over = True
                        
            self.main_screen.blit(self.background, (0,0))
            head1 = self.title.render(f'PLAYER', True, (255, 0, 255))
            head2 = self.title.render(f'SCORE', True, (255, 0, 255))
            self.main_screen.blit(head1, [y_max / 5, (500 / 4) + 5])
            self.main_screen.blit(head2, [y_max / 5 + column_space + 200, (500 / 4) +5])
    
            self.show_records()

            pg.display.flip()
    
class Instructions():
    def __init__(self):
        self.main_screen = pg.display.set_mode((x_max, y_max))
        pg.display.set_caption("INSTRUCTIONS")
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(pg.image.load("the_quest/images/menu_bg.webp"),(800,600)).convert()
        self.startFont =  pg.font.Font("the_quest/fonts/SpecialElite-Regular.ttf", 25)
        self.titleFont =  pg.font.Font("the_quest/fonts/SpecialElite-Regular.ttf", 35)
        self.rect = pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(700,300))
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
            play_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(100,60)), pos=(200, 100), 
                        text_input="PLAY", font=self.startFont, base_color="#d7fcd4", hovering_color="White")
            back_button = Button(pg.transform.scale(pg.image.load("the_quest/images/Rect.png"),(100,60)), pos=(80, 100), 
                            text_input="BACK", font=self.startFont, base_color="#d7fcd4", hovering_color="White")
            for button in [play_button, back_button]:
                button.changeColor(menu_mouse)
                button.update(self.main_screen)
            text = self.titleFont.render("INSTRUCTIONS", True, "#b68f40")
            text_rect = text.get_rect(center=(400, 175))
            text_instru = self.textFont.render("The Quest game. You are in outta space searching for new planets to conquer.", True, (255,255,255))
            text_instru2 = self.textFont.render("You've got 3 lives in each level, if you collide with an asteroid you'll lose one of those lives.", True, (255,255,255))
            text_instru3 = self.textFont.render("You have to survive 30 seconds on each level without losing your 3 lives.", True, (255,255,255))
            text_instru4 = self.textFont.render("To move your spaceship you'll use the key arrow UP and DOWN.", True, (255,255,255))
            text_instru5 = self.textFont.render("The more asteroids you pass without colliding the bigger score you'll get.", True, (255,255,255))
            text_instru6 = self.textFont.render("At the end of the level you will land in a new planet and you'll get 15 extra points for it.", True, (255,255,255))
            text_instru7 = self.textFont.render("If you lose your 3 lives it will be GAME OVER. ", True, (255,255,255))
            text_instru8 = self.textFont.render("If it's GAME OVER, you'll have to start from the first level.", True, (255,255,255))


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
                        game.mainloop(1, 0)
            self.main_screen.blit(text, text_rect)
            self.main_screen.blit(self.rect, (50,200))
            self.main_screen.blit(text_instru, (70, 230))
            self.main_screen.blit(text_instru2, (70, 260))
            self.main_screen.blit(text_instru3, (70, 290))
            self.main_screen.blit(text_instru4, (70, 320))
            self.main_screen.blit(text_instru5, (70, 350))
            self.main_screen.blit(text_instru6, (70, 380))
            self.main_screen.blit(text_instru7, (70, 410))
            self.main_screen.blit(text_instru8, (70, 440))            
            pg.display.flip()
    
class End():
    def __init__(self, score):
        self.screen = pg.display.set_mode((800 , 600)) 
        pg.display.set_caption("LEVEL END") 
        self.score = score + 15
        self.img =  pg.transform.scale(pg.image.load("the_quest/images/blueships1.png"),(80,70))
        self.background = pg.image.load("the_quest/images/backgroundplanet.jpeg").convert()
        self.bg2 = pg.image.load("the_quest/images/bg_level2.jpeg").convert()
        self.bg3 = pg.image.load("the_quest/images/bg_level3.jpeg").convert()
        self.x = 0
        self.rect0 = self.img.get_rect()
        self.center_x = 60
        self.center_y = 300
        self.rect0.center = (self.center_x, self.center_y)
        self.text1 = pg.font.Font("the_quest/fonts/SpecialElite-Regular.ttf", 40)
        self.pointsMarker = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 25)
        self.timer = Max_time_screen
        self.is_best_3 = False
    

    def insert(self, name, score):
        conn = sqlite3.connect("Records.db")
        cursor = conn.cursor()
        query = f"INSERT INTO records VALUES ('{name}', {score})"
        cursor.execute(query)
        conn.commit()
        conn.close()
        
    def read_ordered(self):
        conn = sqlite3.connect("Records.db")
        cursor = conn.cursor()
        query_best_3 = "SELECT name, score FROM records ORDER BY score DESC LIMIT 3"
        data = cursor.execute(query_best_3)
        conn.commit()
        return data
    
    def best_score(self):
        data = self.read_ordered()

        for name, score in data:
            if self.score >= score:
                self.is_best_3 = True

    def get_user_name(self):
        self.screen = pg.display.set_mode((x_max, y_max))
        pg.display.set_caption("Insert name")
        background = pg.image.load("the_quest/images/bg_level3.jpeg")
        font = pg.font.Font("the_quest/fonts/Silkscreen-Regular.ttf", 15)
        manager = pygame_gui.UIManager((x_max, y_max))
        text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pg.Rect((150, 200), (300, 50)), manager=manager,
                                                    object_id='#main_text_entry')
        clock = pg.time.Clock()

        while True:
            refresh_rate = clock.tick(50)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                    return event.text
                
                manager.process_events(event)
            
            manager.update(refresh_rate)
            self.screen.blit(background, (-500, 0))
            f = font.render("Introduce your name if you want to save your score: ", True, (255, 255, 255))
            self.screen.blit(f, (150, 170))
            manager.draw_ui(self.screen)

            pg.display.update()

    def mainloop(self, level):
        clock = pg.time.Clock() 
        runing = True
        angle = 0
        run = True
        self.level = level
            
        while run:
            screen_time = clock.tick(50)
            self.timer -= screen_time
            if level == 1:
                self.screen.blit(self.background, (self.x, 0))
                if self.center_x >= 500:
                    self.center_x = 500
                    p2 = self.text1.render("PRESS ENTER TO NEXT LEVEL", True, (255, 255, 0))
                    self.screen.blit(p2, (120, 525))
                    
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            gameagain = Game()
                            gameagain.mainloop(2, self.score)
            elif level == 2:
                self.screen.blit(self.bg2, (self.x, 0))
                if self.center_x >= 550:
                    self.center_x = 550
                    p2 = self.text1.render("PRESS ENTER TO NEXT LEVEL", True, (255, 255, 0))
                    self.screen.blit(p2, (110, 525))
                    
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            gameagain = Game()
                            gameagain.mainloop(3, self.score)
            elif level == 3:
                self.screen.blit(self.bg3, (self.x, 0))
                if self.center_x >= 395:
                    self.center_x = 395
                    p4 = self.text1.render("YOU'VE WON!", True, (255, 255, 255))
                    self.screen.blit(p4, (270, 200))
                    self.best_score()
                    if self.is_best_3 == True:
                        p3 = self.text1.render("PRESS ENTER TO RECORDS SCREEN", True, (255, 255, 0))
                        self.screen.blit(p3, (75, 500))
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_RETURN:
                                name = self.get_user_name()
                                if name != "":
                                    self.insert(name, self.score)
                                    record = Records()
                                    record.mainloop()
                    else:
                        p5 = self.text1.render("PRESS ENTER TO PLAY AGAIN", True, (255, 255, 0))
                        self.screen.blit(p5, (100, 500))
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_RETURN:
                                game = Game()
                                game.mainloop(1, 0)                 
                
            self.x -= 1
            if self.x <= -500:
                self.x = -500  
            self.center_x += 1
            
            for event in pg.event.get():  
                if event.type == pg.QUIT:  
                    pg.quit()
               
            if runing:        
                angle += 1
                if angle % 180 == 0:
                    runing = False
                        
            if self.timer <= 0:
                menu = Menu()
                menu.mainloop()
            
            p1 = self.pointsMarker.render("Score: " + str(round(self.score)), True, (255, 255, 255))
            self.screen.blit(p1, (10, 20))
            img1 = pg.transform.rotate(self.img , angle) 
            rect1 = img1.get_rect()
            rect1.center = (self.center_x, self.center_y)
            self.screen.blit(img1 ,rect1)
            
            pg.display.flip()


class Game_over():    
    def __init__(self):
        self.main_screen = pg.display.set_mode((x_max, y_max))
        pg.display.set_caption("GAME OVER")
        self.game__over = pg.font.Font("the_quest/fonts/SpecialElite-Regular.ttf", 40)  
        self.game_over_bg = pg.transform.scale(pg.image.load("the_quest/images/game_overr.jpeg"),(800,600))
        self.music_gv = pg.mixer.Sound("the_quest/sound/gameover3-ogg.ogg")
        self.clock = pg.time.Clock()


    def mainloop(self):
        waiting = True
        while waiting:
            self.music_gv.play(-1)
            self.music_gv.set_volume(0.1)
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.music_gv.stop()
                        game = Game()
                        game.mainloop(1, 0)
                        
            self.main_screen.blit(self.game_over_bg, (0,0))
            self.text_continue = self.game__over.render("Press ENTER to play again", True, (255, 255, 0))
            self.main_screen.blit(self.text_continue, (130, 285))

            pg.display.flip()
