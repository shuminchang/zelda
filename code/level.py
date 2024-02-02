import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from arrow import Arrow

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.arrow_sprites = pygame.sprite.Group()

        # sprite group setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.game_over = False

        # need to find better coordinates
        self.next_level_trigger_position = (2500, 1344)
        self.player_has_moved = False

        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 5  # Speed of fade in/out

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(os.path.join(dir_path, 'map', 'map_FloorBlocks.csv')),
            'grass': import_csv_layout(os.path.join(dir_path, 'map', 'map_Grass.csv')),
            'object': import_csv_layout(os.path.join(dir_path, 'map', 'map_Objects.csv')),
            'entities': import_csv_layout(os.path.join(dir_path, 'map', 'map_Entities.csv'))
        }
        graphics = {
            'grass': import_folder(os.path.join(dir_path, 'graphics', 'grass')),
            'objects': import_folder(os.path.join(dir_path, 'graphics', 'objects'))
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), 
                                 [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                                 'grass', 
                                 random_grass_image)
                            
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name, 
                                    (x, y), 
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        if self.player.weapon == 'bow':
            Arrow(self.player, [self.visible_sprites, self.arrow_sprites], self.obstacle_sprites, self.attackable_sprites)
            

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, strength, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

        if self.arrow_sprites:
            for arrow_sprite in self.arrow_sprites:
                collision_sprites = pygame.sprite.spritecollide(arrow_sprite, self.attackable_sprites, False)
                collision_obstacle_sprites = pygame.sprite.spritecollide(arrow_sprite, self.obstacle_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                            arrow_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, arrow_sprite.sprite_type)
                            arrow_sprite.kill()

                if collision_obstacle_sprites:
                    for target_sprite in collision_obstacle_sprites:
                        if target_sprite.sprite_type != 'invisible':
                            arrow_sprite.kill()

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    # def check_for_next_level(self):
    #     if self.player.rect.topleft == self.next_level_trigger_position:
    #         self.start_next_level()

    def check_for_next_level(self):
        trigger_x, trigger_y = self.next_level_trigger_position
        player_x, player_y = self.player.rect.topleft

        # Define a tolerance range
        tolerance = TILESIZE

        within_tolerance = (trigger_x - tolerance <= player_x <= trigger_x + tolerance and
                            trigger_y - tolerance <= player_y <= trigger_y + tolerance)

        if within_tolerance and self.player_has_moved:
            self.start_transition()  # Start the transition instead of directly starting the next level

        # Set player_has_moved to True only if the player moves outside the tolerance range
        if not within_tolerance:
            self.player_has_moved = True

    def start_next_level(self):
        # Logic to start the next level
        # This could involve loading a new map, resetting states, etc.
        # For simplicity, here we just call __init__ to reset the level
        self.__init__()

    def handle_transition(self, screen):
        if self.transitioning:
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.start_next_level()  # Reset level and start next level
                self.transitioning = False
                self.transition_alpha = 0
            else:
                # Draw a semi-transparent surface over the screen
                overlay = pygame.Surface(screen.get_size())
                overlay.fill((0, 0, 0))
                overlay.set_alpha(self.transition_alpha)
                screen.blit(overlay, (0, 0))

                # Display game over message
                font = pygame.font.Font(None, 74)
                text = font.render('NEXT LEVEL', True, (255, 0, 0))  # Red color for Game Over
                text_rect = text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
                self.display_surface.blit(text, text_rect)

    def start_transition(self):
        self.transitioning = True
        self.transition_alpha = 0

    def run(self):
        # Check for game over
        if self.player.health <= 0:
            self.game_over = True

        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        elif not self.game_over:
            # Update and logic processing
            self.check_for_next_level()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
        else:
            self.display_game_over()

    def display_game_over(self):
        # Create a semi-transparent surface to darken the background
        overlay = pygame.Surface(self.display_surface.get_size())
        overlay.set_alpha(128)  # Adjust alpha for desired darkness (0-255)
        overlay.fill((0, 0, 0))  # Fill with black color
        self.display_surface.blit(overlay, (0, 0))  # Draw the overlay

        # Display game over message
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))  # Red color for Game Over
        text_rect = text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.display_surface.blit(text, text_rect)

        # Display restart message
        restart_font = pygame.font.Font(None, 50)
        restart_text = restart_font.render('Press any key to restart', True, (255, 255, 255))  # White color for restart text
        restart_rect = restart_text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 50))
        self.display_surface.blit(restart_text, restart_rect)

    def restart_game(self):
        # Reset the game state
        self.__init__()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(os.path.join(dir_path, 'graphics', 'tilemap', 'ground.png')).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)