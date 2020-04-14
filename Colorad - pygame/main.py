import pygame
from grid import Grid, color_values
from text_box import TextBox
from input_box import InputBox
from button import Button

class ColoradTheGame:
    screen_size = None
    screen = None
    background_color = None
    clock = None
    seed = None

    font_path = None
    
    # UI
    grid = None
    text_box_score = None
    text_box_score_value = None
    text_box_cur_seed = None
    text_box_cur_seed_value = None
    text_box_seed = None
    input_box_seed = None
    button_generate = None

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # window
        self.screen_size = (842, 562)
        self.background_color = (222, 213, 200)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Colorad')
        self.font_path = 'fonts/Quicksand-Bold.ttf'

        # grid
        self.seed = 180603
        self.grid = Grid(size=(32, 32), point_pxl=(20, 20), 
                        border_color=(205, 192, 180), border_thickness_pxl=5, 
                        cell_size_pxl=(16, 16), spacing_pxl=(0, 0),
                        cell_colors=color_values, random_seed=self.seed)

        # text box score
        self.text_box_score = TextBox(point=(550, 20), font_path=self.font_path,
                                font_size=32, font_color=(100, 92, 85))
        self.text_box_score.set_text("Score:")

        # text box score value
        self.text_box_score_value = TextBox(point=(550, 50), font_path=self.font_path,
                                font_size=32, font_color=(100, 92, 85))
        self.text_box_score_value.set_text(str(self.grid.total_score))

        # text box current seed
        self.text_box_cur_seed = TextBox(point=(550, 150), font_path=self.font_path,
                                font_size=32, font_color=(100, 92, 85))
        self.text_box_cur_seed.set_text("Current seed:")

        # text box current seed value
        self.text_box_cur_seed_value = TextBox(point=(550, 180), font_path=self.font_path,
                                font_size=32, font_color=(100, 92, 85))
        self.text_box_cur_seed_value.set_text(str(self.seed))

        # text box seed
        self.text_box_seed = TextBox(point=(550, 280), font_path=self.font_path,
                                font_size=32, font_color=(100, 92, 85))
        self.text_box_seed.set_text("Enter seed:")

        # input box seed
        self.input_box_seed = InputBox(point=(550, 320), length=140, max_char=10, font_size=32,
                                        text_padding=(4, -4), font_path=self.font_path)

        # button generate
        self.button_generate = Button(point=(550, 360), size=(147, 40), text='Generate',
                                        text_padding=(10, 0), font_path=self.font_path, font_size=28, 
                                        font_color=(100, 92, 85), background_color=(205, 192, 180),
                                        callback=self.set_seed)

        # draw the first time!!
        self.draw()

    #_____core_____
    def run(self):
        running = True
        # main loop
        while (running):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_button_down(event)
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event)

            if self.is_end_game():
                self.end_game()

            self.clock.tick(30)
                    
        # loop over, quite pygame
        pygame.quit()

    def update(self):
        self.text_box_score_value.set_text(str(self.grid.total_score))
        self.text_box_cur_seed_value.set_text(str(self.seed))

    def draw(self):
        # clear screen
        self.screen.fill(self.background_color)

        self.grid.draw(self.screen)
        self.text_box_score.draw(self.screen)
        self.text_box_score_value.draw(self.screen)
        self.text_box_cur_seed.draw(self.screen)
        self.text_box_cur_seed_value.draw(self.screen)
        self.text_box_seed.draw(self.screen)
        self.input_box_seed.draw(self.screen)
        self.button_generate.draw(self.screen)
        # update screen
        pygame.display.flip()

    #_____events_____
    def on_key_down(self, event):
        self.input_box_seed.on_key_down(event)
        self.update()
        self.draw()

    def on_mouse_button_down(self, event):
        self.grid.on_mouse_button_down(event)
        self.input_box_seed.on_mouse_button_down(event)
        self.button_generate.on_mouse_button_down(event)
        self.update()
        self.draw()

    def is_end_game(self):
        return self.grid.is_empty()

    def end_game(self):
        print("end game!!!")

    #_____logic_____
    def set_seed(self):
        try:
            seed = int(self.input_box_seed.text)
            self.seed = seed
        except:
            pass

        self.grid.reset_seed(self.seed)

        self.update()
        self.draw()



if __name__ == "__main__":
    my_game = ColoradTheGame()

    my_game.run()