# new menu created at 16th july 2025 at 10:05pm 

import pygame
import sys
from classes.settings import *
from classes.utils import draw_grass

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.scroll = 0

        self.sky_img = pygame.transform.scale(
            pygame.image.load("Images/sky.png").convert(), (W, H - GH)
        )
        self.grass_img = pygame.transform.scale(
            pygame.image.load("Images/grass.png").convert_alpha(), (GW, GH)
        )

        self.start_button_img = pygame.image.load("gui/buttons/Play.png").convert_alpha()
        button_width = 150
        aspect_ratio = self.start_button_img.get_height() / self.start_button_img.get_width()
        button_height = int(button_width * aspect_ratio)
        self.start_button_img = pygame.transform.scale(
            self.start_button_img, (button_width, button_height)
        )
        self.start_button_rect = self.start_button_img.get_rect(center=(W // 2, H // 2 + 50))

        try:
            self.font = pygame.font.Font("./gui/fonts/pixel.ttf", 36)
        except:
            self.font = pygame.font.SysFont("Courier", 36)

    def draw_background(self):
        self.screen.blit(self.sky_img, (0, 0))
        draw_grass(self.screen, self.grass_img, self.scroll)

    def draw_title(self):
        render = self.font.render("Flappy Doge", True, (255, 255, 255))
        x = W // 2 - render.get_width() // 2
        y = H // 3
        self.screen.blit(render, (x, y))

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.scroll += SPEED

            self.draw_background()
            self.draw_title()
            self.screen.blit(self.start_button_img, self.start_button_rect)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(pygame.mouse.get_pos()):
                        return  # Start the game

            pygame.display.update()
