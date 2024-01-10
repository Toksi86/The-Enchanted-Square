from random import choice

from player import Player
from settings import *
from support import *
from tile import Tile
from weapon import Weapon
from ui import UI


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Details.csv'),
            'entities': import_csv_layout('map/map_Entities.csv'),
            # 'objects': None,
        }
        graphics = {
            'grass': import_folder('sprites/grass'),
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
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'invisible', bricks_image[0])
                        # if style == 'object':
                        #    surf = graphics['objects'][int(col)]
                        #    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', surf)
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
                        if style == 'entities':
                            # TODO: change object id on map in Tiled!!!
                            if col == '0':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacles_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )
                            else:
                                # TODO: create Enemy()
                                pass

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


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
