import pygame

class InputBox:
    point = None
    length = None
    color = None
    color_inactive = None
    color_active = None
    text = None
    active = None
    font = None
    font_color = None
    text_padding = None
    max_char = None

    def __init__(self, point, length, font_path, font_size, default_text='',
                max_char=10,
                text_padding=(0,0),
                color_inactive=pygame.Color('lightskyblue3'),
                color_active=pygame.Color('dodgerblue2'),
                font_color=pygame.Color('dodgerblue2')):
        x, y = point
        w, h = length, font_size
        self.point = point
        self.length = length
        self.rect = pygame.Rect(x, y, w, h)

        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = self.color_inactive 

        self.max_char = max_char
        self.text_padding = [*text_padding]
        self.font_color = font_color
        self.text = default_text
        self.font = pygame.font.Font(font_path, font_size)
        self.txt_surface = self.font.render(default_text, True, self.font_color)
        self.active = False

    def on_mouse_button_down(self, event):
        # If the user clicked on the input_box rect.
        if self.rect.collidepoint(event.pos):
            # Toggle the active variable.
            self.active = not self.active
        else:
            self.active = False
        # Change the current color of the input box.
        self.color = self.color_active if self.active else self.color_inactive

    def on_key_down(self, event):
        if self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) <= self.max_char:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = self.font.render(self.text, True, self.font_color)

            width = max(200, self.txt_surface.get_width()+10)
            self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+self.text_padding[0], 
                                       self.rect.y+self.text_padding[1]))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
