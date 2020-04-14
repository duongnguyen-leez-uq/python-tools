import pygame

class TextBox:
    point = None
    font = None
    text = None
    font_color = None
    background_color = None

    def __init__(self, point, font_path, font_size, font_color, background_color=None):
        self.point = point
        self.font = pygame.font.Font(font_path, font_size) 
        self.font_color = font_color
        self.background_color = background_color

    def set_text(self, text):
        self.text = text

    def draw(self, screen):
        text = self.font.render(self.text, True, self.font_color, self.background_color)
        textRect = text.get_rect().move(*self.point)
        screen.blit(text, textRect)

    pass