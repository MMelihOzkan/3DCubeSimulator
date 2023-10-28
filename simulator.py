import pygame
import pygame as py
from cube import Cube


class Simulator:
    def __init__(self, name, window_width, window_height, full_screen):
        py.init()
        self.name = name
        screen_info = py.display.Info()
        self.screen = py.display.set_mode((window_width, window_height))
        py.display.set_caption(name)
        if full_screen:
            width, height = screen_info.current_w, screen_info.current_h
            py.display.set_mode((width, height), py.FULLSCREEN)
        self.clock = py.time.Clock()
        self.run = True
        self.dt = 0
        self.rotate_speed = 100
        self.resize_speed = 1
        self.cube = Cube("3Dcube", 300, (0, 125, 0), (255, 0, 0), 2, (self.screen.get_width() / 2, self.screen.get_height() / 2), self.screen)
        self.cube1 = Cube("3Dcube", 150, (0, 125, 0), (255, 0, 0), 2, (self.screen.get_width() / 2, self.screen.get_height() / 2), self.screen)


    def handle_events(self):
        for event in py.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.cube.recolor()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.cube.auto_animate = not self.cube.auto_animate
                self.cube1.auto_animate = not self.cube1.auto_animate
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                self.cube.strobe_color = not self.cube.strobe_color
                self.cube1.strobe_color = not self.cube1.strobe_color

        key = py.key.get_pressed()
        if key[pygame.K_d]:
            self.cube.rotate_y(-self.rotate_speed * self.dt)
        if key[pygame.K_s]:
            self.cube.rotate_x(self.rotate_speed * self.dt)
        if key[pygame.K_a]:
            self.cube.rotate_y(self.rotate_speed * self.dt)
        if key[pygame.K_w]:
            self.cube.rotate_x(-self.rotate_speed * self.dt)
        if key[pygame.K_RIGHT]:
            self.cube.rotate_z(self.rotate_speed * self.dt)
        if key[pygame.K_LEFT]:
            self.cube.rotate_z(-self.rotate_speed * self.dt)
        if key[pygame.K_k]:
            self.cube.resize(self.resize_speed * self.dt)
        if key[pygame.K_l]:
            self.cube.resize(-self.resize_speed * self.dt)

    def update(self):
        self.cube.update(self.dt)
        self.cube1.update(self.dt)

    def render(self):
        self.screen.fill((0, 0, 0))

        self.cube.render()
        self.cube1.render()

        self.cube.debug()
        font = py.font.Font(None, 36)
        fps_text = font.render(f"FPS: {round(self.clock.get_fps())}", True, (255, 0, 0))
        self.screen.blit(fps_text, (self.screen.get_width() - 160, 20))
        pass

    def clean(self):
        py.display.flip()
        self.dt = self.clock.tick(144) / 1000
