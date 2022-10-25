import random
import pygame as pg
from the_quest import y_max, x_max

NEGRO = (0,0,0)

class Asteroids(pg.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        asteroid50 = pg.transform.scale(pg.image.load("the_quest/images/meteorito.png"),(50,50))
        asteroid100 = pg.transform.scale(pg.image.load("the_quest/images/meteorito.png"),(70,70))
        asteroid150 = pg.transform.scale(pg.image.load("the_quest/images/meteorito.png"),(100,100))
        self.size = size
        if self.size == 1:
            self.image = asteroid50
        elif self.size == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.center_x = random.randint(x_max, x_max + 600)
        self.center_y = random.randrange(y_max - self.w)

    def speed(self, vx):
        self.vx = vx
        self.vx *= -1
    
    def update(self):
        self.center_x += self.vx
        if self.center_x < 0 - self.w:
            for a in range(5):
                self.center_x = random.randint(x_max, x_max + 30)
                self.center_y = random.randrange(y_max - self.w)

    def draw(self, screen):
        screen.blit(self.image, (self.center_x, self.center_y))
        
    @property
    def left(self):
        return self.center_x - self.w // 2
    
    @property
    def up(self):
        return self.center_y - self.h // 2
    
    @property
    def down(self):
        return self.center_y + self.h // 2
            
class Spaceship(pg.sprite.Sprite):
    def __init__(self, center_x=60, vy = 2):
        super().__init__()
        self._image = pg.transform.scale(pg.image.load("the_quest/images/blueships1.png"),(80,70))
        self.landing = pg.transform.scale(pg.image.load("the_quest/images/blueships1.png"),(60,30))
        self.center_x = center_x
        self.img = self._image
        self.flipped = pg.transform.rotate(self.img, 0)
        self.center_y = y_max // 2
        self.vy = vy
        self.w = self.img.get_width()
        self.h= self.img.get_height()
        self.lives = 3
        self.angle = 0
        self.rect = self.img.get_rect()
        self.rect_center = (self.w // 2, self.h // 2)
        self.rotating = False
       


    def move(self, key_up, key_down):
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
        screen.blit(self.img, ((self.center_x - self.w // 2), self.center_y - self.h // 2))
        if self.rotating:
            self.angle += 1
            img1 = pg.transform.rotate(self.img , self.angle) 
            rect1 = img1.get_rect()
            rect1.center = self.rect.center
            if self.angle == 180:
                self.angle = 180

        

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
        return (self.center_y + self.h // 2) - 50
    

class Explosion(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pg.image.load(f"the_quest/images/exp{num}.png")
			img = pg.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


