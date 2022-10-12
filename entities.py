import random
import pygame as pg


class Asteroids:
    
    def __init__(self, size):
        asteroid50 = pg.image.load("images/asteroid50.png")
        asteroid100 = pg.image.load("images/asteroid100.png")
        asteroid150 = pg.image.load("images/asteroid100.png")
        self.size = size
        if self.size == 1:
            self.image = asteroid50
        elif self.size == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = self.image.get_width()
        self.h= self.image.get_height()
        self.center_x = random.randint(800, 1500)
        self.center_y = random.randrange(600 - self.w)
        
    
    def speed(self, vx):
        self.vx = vx
   

    def draw(self, screen):
        screen.blit(self.image, (self.center_x, self.center_y))
    
    def move(self):
        self.center_x += self.vx
        if self.center_x < 0 - self.w:
            for a in range(5):
                self.center_x = random.randint(800, 830)
                self.center_y = random.randrange(600 - self.w)
            

class Spaceship:
    def __init__(self):
        image = pg.image.load("images/spaceRocket.png")
        self.img = image
        self.center_x = 60
        self.center_y = 240
        self.w = self.img.get_width()
        self.h= self.img.get_height()


    def speed(self, vy):
        self.vy = vy

   
    def move(self, key_up, key_down, y_max=600):
        key_state = pg.key.get_pressed()
        if key_state[key_up]:
            self.center_y -= self.vy 
        if self.center_y < self.h // 2:
            self.center_y = self.h // 2
      
       
        if key_state[key_down]:
            self.center_y += self.vy
        if self.center_y > y_max - self.h // 2:
            self.center_y = y_max - self.h // 2
        
        

    def draw(self, screen):
        screen.blit(self.img, (self.center_x - self.w//2, self.center_y - self.h//2, self.w, self.h))