import pygame
import Squares
import Colors
# TODO: Add pause menu
# TODO: Add lose screen
# TODO: Add score counter
# TODO: Add next piece preview?


class Display:
    def __init__(self):
        self.resolution = (430, 600)
        self.min_size = self.resolution
        game_run = True
        self.frame_count = 30
        self.mode = "game"
        self.squares = Squares.Squares()
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.root = pygame.display.set_mode(self.resolution, pygame.RESIZABLE)
        clock = pygame.time.Clock()
        while game_run:
            clock.tick(60)
            if self.mode == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_run = False
                    elif event.type == pygame.VIDEORESIZE:
                        w = event.w
                        h = event.h
                        resize = False
                        if w < self.min_size[0]:
                            resize = True
                            w = self.min_size[0]
                        if h < self.min_size[1]:
                            resize = True
                            h = self.min_size[1]
                        self.resolution = (w, h)
                        if resize:
                            pygame.display.set_mode((w, h), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.squares.move_left()
                        elif event.key == pygame.K_RIGHT:
                            self.squares.move_right()
                        elif event.key == pygame.K_UP or event.key == pygame.K_x:
                            self.squares.rotate_right()
                self.root.fill(Colors.display_colors["white"])
                if not self.squares.has_shape():
                    if self.squares.spawn_new():
                        self.mode = "gg"
                        print("Game Over!!!")
                self.frame_count -= 1
                if self.frame_count <= 0:
                    self.frame_count = 30
                    self.squares.move_down()
                self.draw_pixels()
                pygame.display.update()
            elif self.mode == "gg":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_run = False
                    elif event.type == pygame.VIDEORESIZE:
                        w = event.w
                        h = event.h
                        resize = False
                        if w < self.min_size[0]:
                            resize = True
                            w = self.min_size[0]
                        if h < self.min_size[1]:
                            resize = True
                            h = self.min_size[1]
                        self.resolution = (w, h)
                        if resize:
                            pygame.display.set_mode((w, h), pygame.RESIZABLE)
                self.root.fill(Colors.display_colors["white"])
                pygame.display.update()
        pygame.quit()

    def draw_pixels(self):
        squares = self.squares.get_pixels()
        width, height = self.squares.get_size()
        if self.resolution[0] / width * height > self.resolution[1]:
            length = self.resolution[1] / height
        else:
            length = self.resolution[0] / width
        for row in range(0, height):
            for column in range(0, width):
                x = length * column
                y = length * row
                pygame.draw.rect(self.root, squares[row][column], [x + 2, y + 2, length - 4, length - 4], 0)


if __name__ == "__main__":
    Display()
