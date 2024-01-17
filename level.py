import pygame.time

from enemy import Enemy
from magic import MagicPlayer
from particles import AnimationPlayer
from player import Player
from settings import *
from support import *
from tile import Tile
from ui import UI
from upgrade import Upgrade
from weapon import Weapon


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'entities': import_csv_layout('map/map_Entities.csv'),
            'player': import_csv_layout('map/map_Player.csv')
            # 'objects': None,
        }
        graphics = {
            'bricks': import_folder('sprites/bricks')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            bricks_image = graphics['bricks']
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                                 'invisible', bricks_image[0])
                        if style == 'player':
                            if col == '0':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacles_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )
                        if style == 'entities':
                            if col == '1':
                                monster_name = 'rabbit'
                            elif col == '0':
                                monster_name = 'fox'
                            elif col == '2':
                                monster_name = 'wolf'
                            else:
                                monster_name = 'monster'
                            Enemy(monster_name, (x, y),
                                  [self.visible_sprites, self.attackable_sprites, self.monsters],
                                  self.obstacles_sprites, self.damage_player, self.trigger_death_particles,
                                  self.add_exp)

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

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
                            target_sprite.kill()
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # TODO: Draw damage animations for the main character and uncomment
            # self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def win_game(self):
        if len(self.monsters) == 0:
            self.game_paused = True

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.win_game()
        player_is_alive = self.player.check_life()

        if self.game_paused or not player_is_alive:
            # display upgrade menu
            if len(self.monsters) == 0:
                self.ui.show_game_win()
            elif player_is_alive:
                self.upgrade.display()
            else:
                self.ui.show_game_over()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load('map/game_map.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
