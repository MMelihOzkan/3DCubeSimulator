import pygame as py
import math as m
import random


class Cube:
    def __init__(self, name, size, color, border_color, border_width, pos, screen):
        self.name = name
        self.size = size  # in pixels
        self.color = color
        self.screen = screen
        self.border_color = border_color
        self.border_width = border_width
        self.pos = py.Vector2(pos[0], pos[1])  # pass pos as (x,y)
        self.r = m.pi * (1 / 180)  # 1 degree in radians
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        # size adjust as "sa"
        self.sa = 1
        self.auto_animate = False
        self.auto_animate_random_timer = py.time.get_ticks()
        self.timer_cooldown = True
        self.strobe_color = False
        self.strobe_color_timer = py.time.get_ticks()
        self.strobe_color_timer_cooldown = True
        self.random_x = random.randint(-1, 1)
        self.random_y = random.randint(-1, 1)
        self.random_z = random.randint(-1, 1)
        # Original vertices
        self.v = ((- size / 2, - size / 2, - size / 2),  # top left -z
                  (+ size / 2, - size / 2, - size / 2),  # top right -z
                  (- size / 2, + size / 2, - size / 2),  # bottom left -z
                  (+ size / 2, + size / 2, - size / 2),  # bottom right -z
                  (- size / 2, - size / 2, size / 2),  # top left +z
                  (+ size / 2, - size / 2, size / 2),  # top right +z
                  (- size / 2, + size / 2, size / 2),  # bottom left +z
                  (+ size / 2, + size / 2, size / 2))  # bottom right +z
        # Projected vertices
        self.pv = [[- size / 2, - size / 2, - size / 2],  # top left -z
                   [+ size / 2, - size / 2, - size / 2],  # top right -z
                   [- size / 2, + size / 2, - size / 2],  # bottom left -z
                   [+ size / 2, + size / 2, - size / 2],  # bottom right -z
                   [- size / 2, - size / 2, size / 2],  # top left +z
                   [+ size / 2, - size / 2, size / 2],  # top right +z
                   [- size / 2, + size / 2, size / 2],  # bottom left +z
                   [+ size / 2, + size / 2, size / 2]]  # bottom right +z

        self.lines = ((0, 1), (0, 2), (0, 4), (3, 1), (3, 2), (3, 7), (5, 1), (5, 4), (5, 7), (6, 2), (6, 4), (6, 7))
        self.polygons = ((0,1,3,2),(4,5,7,6),(0,4,5,1),(1,5,7,3),(2,3,7,6),(0,4,6,2))
        self.colors = []
        for i in range(12):
            self.colors.append((random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)))

    def render(self):
        """"
        for polygon in self.polygons:
            print(f"a: {polygon[0]}, b:{polygon[1]}, c:{polygon[2]}, d:{polygon[3]}")
        """

        for polygon in self.polygons:
            py.draw.polygon(self.screen,self.color,((self.pv[polygon[0]][0] + self.pos.x,self.pv[polygon[0]][1] + self.pos.y),
                                                    (self.pv[polygon[1]][0] + self.pos.x, self.pv[polygon[1]][1] + self.pos.y),
                                                    (self.pv[polygon[2]][0] + self.pos.x, self.pv[polygon[2]][1] + self.pos.y),
                                                    (self.pv[polygon[3]][0] + self.pos.x, self.pv[polygon[3]][1] + self.pos.y)))

        count = 0
        for line in self.lines:
            color = self.colors[count]
            py.draw.aaline(self.screen, self.border_color,
                           (self.pv[line[0]][0] + self.pos.x, self.pv[line[0]][1] + self.pos.y),
                           (self.pv[line[1]][0] + self.pos.x, self.pv[line[1]][1] + self.pos.y))
            count += 1

        # py.draw.aaline(self.screen, self.border_color,(self.pos.x, self.pos.y),(self.pv[0][0] + self.pos.x, self.pv[0][1] + self.pos.y))

    def update(self, dt):
        self.auto(dt)
        c, b, a = self.x_rotation * self.r, self.y_rotation * self.r, self.z_rotation * self.r
        for i in range(8):
            self.pv[i][0] = self.x_pos + (self.sa * (self.v[i][0] * (m.cos(a) * m.cos(b)) + self.v[i][1] * (m.cos(a) * m.sin(b) * m.sin(c) - m.sin(a) * m.cos(c)) + self.v[i][2] * (m.cos(a) * m.sin(b) * m.cos(c) + m.sin(a) * m.sin(c))))
            self.pv[i][1] = self.y_pos + (self.sa * (self.v[i][0] * (m.sin(a) * m.cos(b)) + self.v[i][1] * (m.sin(a) * m.sin(b) * m.sin(c) + m.cos(a) * m.cos(c)) + self.v[i][2] * (m.sin(a) * m.sin(b) * m.cos(c) - m.cos(a) * m.sin(c))))
            self.pv[i][2] = self.z_pos + (self.sa * (self.v[i][0] * (-m.sin(b)) + self.v[i][1] * (m.cos(b) * m.sin(c)) + self.v[i][2] * (m.cos(b) * m.cos(c))))

    def debug(self):
        font = py.font.Font(None, 28)
        x_text = font.render(f"x rotation: {int(self.x_rotation)}", True, (0, 0, 255))
        y_text = font.render(f"y rotation: {int(self.y_rotation)}", True, (0, 0, 255))
        z_text = font.render(f"z rotation: {int(self.z_rotation)}", True, (0, 0, 255))
        self.screen.blit(x_text, (self.screen.get_width() - 160, 45))
        self.screen.blit(y_text, (self.screen.get_width() - 160, 65))
        self.screen.blit(z_text, (self.screen.get_width() - 160, 85))



    def rotate_x(self, direction):
        self.x_rotation += direction
        if self.x_rotation > 359:
            self.x_rotation -= 360
        elif self.x_rotation < 0:
            self.x_rotation += 360

    def rotate_y(self, direction):
        self.y_rotation += direction
        if self.y_rotation > 359:
            self.y_rotation -= 360
        elif self.y_rotation < 0:
            self.y_rotation += 360

    def rotate_z(self, direction):
        self.z_rotation += direction
        if self.z_rotation > 359:
            self.z_rotation -= 360
        elif self.z_rotation < 0:
            self.z_rotation += 360

    def resize(self, amount):
        self.sa += amount

    def move_x(self, amount):
        self.x_pos += amount

    def move_y(self, amount):
        self.y_pos += amount

    def move_z(self, amount):
        self.z_pos += amount

    def recolor(self):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.border_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def auto(self, dt):
        if self.strobe_color_timer_cooldown and self.strobe_color:
            self.strobe_color_timer_cooldown = not self.strobe_color_timer_cooldown
            self.recolor()
        if self.timer_cooldown and self.auto_animate:
            self.sa = random.randint(-2, 2)
            if self.sa == 0:
                self.sa += 1
            self.timer_cooldown = False
            self.recolor()
            self.random_x = random.randint(-5, 5)
            self.random_y = random.randint(-5, 5)
            self.random_z = random.randint(-5, 5)

        if py.time.get_ticks() - self.auto_animate_random_timer > 1000:
            self.timer_cooldown = True
            self.auto_animate_random_timer = py.time.get_ticks()

        if py.time.get_ticks() - self.strobe_color_timer > 200:
            self.strobe_color_timer_cooldown = True
            self.strobe_color_timer = py.time.get_ticks()

        if self.auto_animate:

            self.rotate_x(dt * self.random_x *20)
            self.rotate_y(dt * self.random_y *20)
            self.rotate_z(dt * self.random_z *20)
