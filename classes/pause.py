import pygame

class Pause:
    def __init__(self):
        self.active = False
        self.font = pygame.font.SysFont("Courier", 32)
        self.play_img = pygame.image.load("gui/play.png").convert_alpha()
        self.play_rect = self.play_img.get_rect(center=(200, 300))

    def toggle(self):
        self.active = not self.active

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))

        text = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 150))
        screen.blit(self.play_img, self.play_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_rect.collidepoint(event.pos):
                self.toggle()