import pygame as pg

class Asteroids:
    def __init__(self, center_x, center_y, radio=10, color=(255, 255, 0)):
        self.center_x = center_x
        self.center_y = center_y
        self.radio = radio
        self.color = color

        self.vx = 0
        self.vy = 0
        
    
    def speed(self, vx, vy):

        self.vx = vx
        self.vy = vy
    
    def move(self):

        self.center_x += self.vx

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.center_x, self.center_y), self.radio)

class Spaceship:
    image = pg.image.load("images/spaceRocket.png")
    def __init__(self):
        image = pg.image.load("images/spaceRocket.png")
        self.img = image
        self.center_x = 60
        self.center_y = 240
        self.w = self.img.get_width()
        self.h= self.img.get_height()


    def speed(self, vx, vy):
        self.vx = vx
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