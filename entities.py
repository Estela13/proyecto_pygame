from curses import KEY_DOWN, KEY_UP
import random
import pygame as pg


class Asteroids:
    
    def __init__(self, size, x_max = 800, y_max = 600):
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
        self.h = self.image.get_height()
        self.center_x = random.randint(x_max, x_max + 600)
        self.center_y = random.randrange(y_max - self.w)
        
    
    def speed(self, vx):
        self.vx = vx
   
    
    def move(self, x_max, y_max):
        self.center_x += self.vx
        if self.center_x < 0 - self.w:
            for a in range(5):
                self.center_x = random.randint(x_max, x_max + 30)
                self.center_y = random.randrange(y_max - self.w)
                


    def draw(self, screen):
        screen.blit(self.image, (self.center_x, self.center_y))
        
        
    def itTouches(self, spaceship):
        if self.left <= spaceship.right and self.down >= spaceship.up and self.up <= spaceship.down and self.left >= spaceship.left:
            pass

    @property
    def left(self):
        return self.center_x - self.w // 2
    
    @property
    def up(self):
        return self.center_y - self.h // 2
    
    @property
    def down(self):
        return self.center_y + self.h // 2
            

class Spaceship:
    def __init__(self, vy, y_max = 600):
        image = pg.image.load("images/spaceRocket.png")
        self.img = image
        self.center_x = 60
        self.center_y = y_max // 2
        self.w = self.img.get_width()
        self.h= self.img.get_height()
        #self.imagen_redimensionada = pg.transform.scale(self.img, (100, 100))
        self.vy = vy
        self.lives = 3

   
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


    @property
    def right(self):
        return self.center_x + self.w // 2
    
    @property
    def left(self):
        return self.center_x - self.w // 2
    
    @property
    def up(self):
        return self.center_y - self.h // 2

    @property
    def down(self):
        return self.center_y + self.h // 2
    