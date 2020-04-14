import pygame

class Button:
    point = None
    size = None
    font = None
    text = None
    text_color = None
    background_color = None
    text_padding = None
    callback = None
    rect = None

    def __init__(self, point, size, text, 
            font_path, font_size, font_color, background_color, callback,
            text_padding=(0,0)):
        self.point = point
        self.size = size
        self.font = pygame.font.Font(font_path, font_size) 
        self.font_color = font_color
        self.background_color = background_color
        self.text = text
        self.text_padding = [*text_padding]
        self.callback = callback
        self.rect = pygame.Rect(*self.point, *self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        textRect = text.get_rect().move(*self.point).move(*self.text_padding)
        screen.blit(text, textRect)

    def on_mouse_button_down(self, event):
        position = event.pos
        if self.rect.collidepoint(*position):
            self.callback()