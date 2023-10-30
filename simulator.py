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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                self.cube.strobe_color = not self.cube.strobe_color

        key = py.key.get_pressed()
        if key[pygame.K_d]:
            self.cube.rotate_y(-self.rotate_speed * self.dt)
        if key[pygame.K_s]:
            self.cube.rotate_x(self.rotate_speed * self.dt)
        if key[pygame.K_a]:
            self.cube.rotate_y(self.rotate_speed * self.dt)
        if key[pygame.K_w]:
            self.cube.rotate_x(-self.rotate_speed * self.dt)
        if key[pygame.K_e]:
            self.cube.rotate_z(self.rotate_speed * self.dt)
        if key[pygame.K_q]:
            self.cube.rotate_z(-self.rotate_speed * self.dt)
        if key[pygame.K_k]:
            self.cube.resize(self.resize_speed * self.dt)
        if key[pygame.K_l]:
            self.cube.resize(-self.resize_speed * self.dt)
        if key[pygame.K_RIGHT]:
            self.cube.move_x(self.rotate_speed * self.dt)
        if key[pygame.K_LEFT]:
            self.cube.move_x(-self.rotate_speed * self.dt)
        if key[pygame.K_UP]:
            self.cube.move_y(-self.rotate_speed * self.dt)
        if key[pygame.K_DOWN]:
            self.cube.move_y(self.rotate_speed * self.dt)

    def update(self):
        self.cube.update(self.dt)

    def render(self):
        self.screen.fill((0, 0, 0))

        self.cube.debug()

        self.cube.render()

        font = py.font.Font(None, 36)
        font1= py.font.Font(None, 24)
        fps_text = font.render(f"FPS: {round(self.clock.get_fps())}", True, (255, 0, 0))
        control_text = font1.render("CONTROLS:", True, (255, 0, 0))
        yaw_text = font1.render("YAW: A D", True, (255, 0, 0))
        pitch_text = font1.render("PITCH: W S", True, (255, 0, 0))
        roll_text = font1.render("ROLL: A D", True, (255, 0, 0))
        resize_text = font1.render("RESIZE: K L", True, (255, 0, 0))
        auto_text = font1.render("AUTO: P", True, (255, 0, 0))
        strobe_text = font1.render("STROBE: O", True, (255, 0, 0))
        move_text = font1.render("MOVE: ARROWS", True, (255, 0, 0))
        self.screen.blit(fps_text, (self.screen.get_width() - 160, 20))
        self.screen.blit(control_text, (self.screen.get_width() - 160, 110))
        self.screen.blit(yaw_text, (self.screen.get_width() - 160, 130))
        self.screen.blit(pitch_text, (self.screen.get_width() - 160, 150))
        self.screen.blit(roll_text, (self.screen.get_width() - 160, 170))
        self.screen.blit(resize_text, (self.screen.get_width() - 160, 190))
        self.screen.blit(auto_text, (self.screen.get_width() - 160, 210))
        self.screen.blit(strobe_text, (self.screen.get_width() - 160, 230))
        self.screen.blit(move_text, (self.screen.get_width() - 160, 250))

    def clean(self):
        py.display.flip()
        self.dt = self.clock.tick(144) / 1000
