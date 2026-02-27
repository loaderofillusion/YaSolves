import random

import arcade

SPEED = 4
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Donatello Game"
CELL_SIZE = 64


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(":resources:images/enemies/fly.png")
        self.scale = 0.3

    def update(self, delta_time):
        """ Отражение персонажа """
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < CELL_SIZE or self.right > SCREEN_WIDTH - CELL_SIZE:
            self.change_x *= -1
        if self.bottom < CELL_SIZE or self.top > SCREEN_HEIGHT - CELL_SIZE:
            self.change_y *= -1


class GridGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.cell_size = CELL_SIZE
        self.all_sprites = arcade.SpriteList()
        self.wall_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()
        # Загружаем текстуры из встроенных ресурсов
        self.stone_texture = arcade.load_texture(":resources:images/tiles/stoneCenter.png")
        self.sand_texture = arcade.load_texture(":resources:images/tiles/sandCenter.png")
        self.player_texture = arcade.load_texture(":resources:images/enemies/slimeBlue.png")
        self.player1_texture = arcade.load_texture(":resources:images/enemies/slimePurple.png")

    def setup(self):
        self.grid = [[0 for _ in range(15)] for _ in range(10)]
        for row in range(10):
            for col in range(15):
                if not row * col or row == 9 or col == 14:
                    self.grid[row][col] = 1
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2

                # Рисуем основу клетки
                if self.grid[row][col] == 0:
                    sand_sprite = arcade.Sprite(self.sand_texture, scale=0.5)
                    sand_sprite.position = (x, y)
                    self.grid[row][col] = [sand_sprite]
                    self.all_sprites.append(sand_sprite)
                else:
                    stone_sprite = arcade.Sprite(self.stone_texture, scale=0.5)
                    self.grid[row][col] = [stone_sprite]
                    stone_sprite.position = (x, y)
                    self.wall_sprites.append(stone_sprite)
                    self.all_sprites.append(stone_sprite)

        free_places = [(x, y) for x in range(1, 14) for y in range(1, 9)]
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        x = 12 * self.cell_size + self.cell_size // 2
        y = 5 * self.cell_size + self.cell_size // 2
        self.player.position = (x, y)
        self.all_sprites.append(self.player)
        free_places.remove((12, 5))

        self.player1 = arcade.Sprite(self.player1_texture, scale=0.5)
        x = 2 * self.cell_size + self.cell_size // 2
        y = 5 * self.cell_size + self.cell_size // 2
        self.player1.position = (x, y)
        self.all_sprites.append(self.player1)
        free_places.remove((2, 5))

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_sprites
        )
        self.physics_engine1 = arcade.PhysicsEngineSimple(
            self.player1, self.wall_sprites
        )

        # Enemies
        for _ in range(5):
            enemy = Enemy()
            enemy.change_x = random.randint(-4, 4)
            enemy.change_y = random.randint(-4, 4)
            x, y = random.choice(free_places)
            free_places.remove((x, y))
            enemy.position = (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2)
            self.enemy_sprites.append(enemy)
            self.all_sprites.append(enemy)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.physics_engine1.update()
        self.enemy_sprites.update()
        check_enemy = arcade.check_for_collision_with_list(self.player, self.enemy_sprites) + \
                      arcade.check_for_collision_with_list(self.player1, self.enemy_sprites)
        for enemy in check_enemy:
            self.enemy_sprites.remove(enemy)
            self.all_sprites.remove(enemy)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED

        if key == arcade.key.W:
            self.player1.change_y = SPEED
        elif key == arcade.key.S:
            self.player1.change_y = -SPEED
        elif key == arcade.key.A:
            self.player1.change_x = -SPEED
        elif key == arcade.key.D:
            self.player1.change_x = SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0
        if key in [arcade.key.W, arcade.key.S]:
            self.player1.change_y = 0
        if key in [arcade.key.A, arcade.key.D]:
            self.player1.change_x = 0


def setup_game(width=960, height=640, title="Donatello Game"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()

