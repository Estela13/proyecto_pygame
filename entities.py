import pygame as pg

class Asteroids:
    def __init__(self, center_x, center_y, radio=10, color=(255, 255, 0)):
        self.center_x = center_x
        self.center_y = center_y
        self.radio = radio
        self.color = color

        self.vx = 0
        self.vy = 0
        
    
    def velocidad(self, vx, vy):

        self.vx = vx
        self.vy = vy
    
    def mover(self):

        self.center_x += self.vx

    def dibujar(self, pantalla):
        pg.draw.circle(pantalla, self.color, (self.center_x, self.center_y), self.radio)

class Nave:
    def __init__(self, center_x=20, center_y=240, w=25, h=60, color=(255, 0, 255)):
        self.center_x = center_x
        self.center_y = center_y
        self.w = w
        self.h= h
        self.color = color

    def velocidad(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def mover(self, tecla_arriba, tecla_abajo, y_max=600):
        estado_teclas = pg.key.get_pressed()
        if estado_teclas[tecla_arriba]:
            self.center_y -= self.vy
        if self.center_y < self.h // 2:
            self.center_y = self.h // 2


        if estado_teclas[tecla_abajo]:
            self.center_y += self.vy
        if self.center_y > y_max - self.h // 2:
            self.center_y = y_max - self.h // 2

    def dibujar(self, pantalla):
        pg.draw.rect(pantalla, self.color, (self.center_x - self.w//2, self.center_y - self.h//2, self.w, self.h))