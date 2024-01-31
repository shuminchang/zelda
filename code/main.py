import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        background_image = pygame.image.load(os.path.join(dir_path, 'graphics', 'start_menu', 'background.png')).convert()

        # Resize the background image to match the game window size
        self.start_menu_background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        self.level = Level()

        # sound
        main_sound = pygame.mixer.Sound(os.path.join(dir_path, 'audio', 'main.ogg'))
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

    def run(self):
        self.start_menu()  # Call the start menu before the game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.level.game_over:
                    if event.type == pygame.KEYDOWN:
                        self.level.restart_game()
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.level.toggle_menu()
            
            self.screen.fill(WATER_COLOR)

            if self.level.transitioning:
                self.level.handle_transition(self.screen)
            else:
                self.level.run()
                
            pygame.display.update()
            self.clock.tick(FPS)

    def start_menu(self):
        menu = True
        selected = "start"
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected = "end" if selected == "start" else "start"
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            menu = False
                        elif selected == "end":
                            pygame.quit()
                            sys.exit()

            self.screen.fill((0, 0, 0))  # Fill the screen with black or your desired background color
            title_font = pygame.font.Font(None, 74)  # You might want to adjust the font size

            # Draw the background image
            self.screen.blit(self.start_menu_background, (0, 0))

            # Use draw_text_with_shadow for title
            # Dynamically calculate position to center the title
            title_text_1 = 'The Chronicles of Eldoria'
            title_text_2 = 'Shadows of the Lost Kingdom'
            self.draw_text_with_shadow_centered(title_text_1, title_font, (255, 255, 255), (0, 0, 0), HEIGHT // 4 - 50, (2, 2))
            self.draw_text_with_shadow_centered(title_text_2, title_font, (255, 255, 255), (0, 0, 0), HEIGHT // 4, (2, 2))

            if selected == "start":
                self.draw_text_with_shadow_centered('Start Game', title_font, (255, 0, 0), (0, 0, 0), HEIGHT // 2, (2, 2))
                self.draw_text_with_shadow_centered('End Game', title_font, (255, 255, 255), (0, 0, 0), HEIGHT // 2 + 100, (2, 2))
            else:
                self.draw_text_with_shadow_centered('Start Game', title_font, (255, 255, 255), (0, 0, 0), HEIGHT // 2, (2, 2))
                self.draw_text_with_shadow_centered('End Game', title_font, (255, 0, 0), (0, 0, 0), HEIGHT // 2 + 100, (2, 2))

            pygame.display.update()
            self.clock.tick(60)

    def draw_text_with_shadow_centered(self, text, font, color, shadow_color, y, shadow_offset):
        text_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, shadow_color)
        
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + shadow_offset[0], y + shadow_offset[1]))

        self.screen.blit(shadow_surface, (shadow_rect.x, shadow_rect.y))
        self.screen.blit(text_surface, (text_rect.x, text_rect.y))


if __name__ == '__main__':
    game = Game()
    game.run()