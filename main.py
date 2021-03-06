import os
import sys
import pygame
import Squares
import Menu
import Colors


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Display:
    def __init__(self):
        self.resolution = (430, 600)
        self.min_size = self.resolution
        game_run = True
        self.frame_count = 30
        self.frame_delay = 30
        self.key_repeat = 0
        self.key_delay = 5
        self.pause_menu = Menu.Menu()
        self.mode = "title"
        self.squares = Squares.Squares()
        pygame.init()
        clock = pygame.time.Clock()
        font1 = pygame.font.SysFont("simhei", 40)
        font2 = pygame.font.SysFont("simhei", 70)
        background_music = pygame.mixer.Sound(resource_path(os.path.normpath("./Sounds/Tetris.ogg")))
        background_music.play(-1)
        pygame.display.set_caption("Tetris")
        pygame.display.set_icon(pygame.image.load(resource_path(os.path.normpath("./Images/Icon.png"))))
        self.root = pygame.display.set_mode(self.resolution, pygame.RESIZABLE)
        while game_run:
            clock.tick(60)
            if self.mode == "title":
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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if round(self.resolution[0] / 2 - 100) <= x <= round(self.resolution[0] / 2 - 100) + 200 and \
                                self.resolution[1] - 70 <= y <= self.resolution[1] - 70 + 60:
                            self.mode = "game"
                    self.root.fill(Colors.display_colors["white"])
                    title = "Tetris"
                    text2 = "Start"
                    self.root.blit(font2.render(title, True, Colors.display_colors["black"]), (round(self.resolution[0] / 2 - font2.size(title)[0] / 2), 20))
                    pygame.draw.rect(self.root, Colors.display_colors["orange"], [round(self.resolution[0] / 2 - 100), self.resolution[1] - 70, 200, 60], 0)
                    self.root.blit(font1.render(text2, True, Colors.display_colors["black"]), (round(self.resolution[0] / 2 - font1.size(text2)[0] / 2), round(self.resolution[1] - 70 + (60 / 2) - (font1.size(text2)[1] / 2))))
                    pygame.display.update()
            elif self.mode == "game":
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
                        if not self.pause_menu.is_paused():
                            if event.key == pygame.K_LEFT:
                                self.key_repeat = 1
                                self.key_delay = 5
                            elif event.key == pygame.K_RIGHT:
                                self.key_repeat = 2
                                self.key_delay = 5
                            elif event.key == pygame.K_UP or event.key == pygame.K_x:
                                self.squares.rotate_right()
                            elif event.key == pygame.K_DOWN:
                                self.frame_delay = 3
                                self.frame_count = 0
                    elif event.type == pygame.KEYUP:
                        if not self.pause_menu.is_paused():
                            if event.key == pygame.K_LEFT:
                                if self.key_repeat == 1:
                                    self.key_repeat = 0
                            elif event.key == pygame.K_RIGHT:
                                if self.key_repeat == 2:
                                    self.key_repeat = 0
                            elif event.key == pygame.K_DOWN:
                                self.frame_delay = 30
                                self.frame_count = 30
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if self.pause_menu.is_paused():
                            pos = self.pause_menu.get_btn_hit_box()
                            if pos[0] <= x <= pos[1] and pos[2] <= y <= pos[3]:
                                self.pause_menu.toggle_pause()
                            else:
                                pos = self.pause_menu.get_btn2_hit_box()
                                if pos[0] <= x <= pos[1] and pos[2] <= y <= pos[3]:
                                    self.pause_menu.toggle_pause()
                                    self.squares = Squares.Squares()
                                    self.frame_count = 30
                                    self.frame_delay = 30
                                    self.key_repeat = 0
                                    self.key_delay = 5
                        else:
                            if 8 <= x <= 28 and self.resolution[1] - 27 <= y <= self.resolution[1] - 13:
                                self.pause_menu.toggle_pause()
                self.root.fill(Colors.display_colors["white"])
                if not self.pause_menu.is_paused():
                    if not pygame.key.get_focused():
                        self.pause_menu.set_pause()
                    if not self.squares.has_shape():
                        if self.squares.spawn_new():
                            self.mode = "gg"
                    if self.key_repeat != 0:
                        self.key_delay -= 1
                        if self.key_delay <= 0:
                            self.key_delay = 5
                            (self.squares.move_left, self.squares.move_right)[self.key_repeat - 1]()
                    self.frame_count -= 1
                    if self.frame_count <= 0:
                        self.frame_count = self.frame_delay
                        self.squares.move_down()
                self.draw_pixels()
                self.root.blit(font1.render(f"Score: {self.squares.get_score()}", True, Colors.display_colors["black"]), (20, 5))
                size = font1.size(f"Score: {self.squares.get_score()}")
                text = f"Level: {self.squares.get_level()}"
                self.root.blit(font1.render(text, True, Colors.display_colors["black"]), (self.resolution[0] - font1.size(text)[0] - 20, 5))
                size = font1.size(text)
                pygame.draw.rect(self.root, Colors.display_colors["black"], [8, self.resolution[1] - 27, 20, 5], 0)
                pygame.draw.rect(self.root, Colors.display_colors["black"], [8, self.resolution[1] - 20, 20, 5], 0)
                pygame.draw.rect(self.root, Colors.display_colors["black"], [8, self.resolution[1] - 13, 20, 5], 0)
                if self.pause_menu.is_paused():
                    self.key_repeat = 0
                    self.key_delay = 5
                    self.frame_delay = 30
                    self.pause_menu.relocate(self.resolution, font1)
                    overlay_surface = pygame.Surface(self.resolution, pygame.SRCALPHA)
                    overlay_surface.fill(Colors.display_colors["transparent"])
                    self.root.blit(overlay_surface, (0, 0))
                    pygame.draw.rect(self.root, Colors.display_colors["grey"], self.pause_menu.get_rect(), 0)
                    self.root.blit(font1.render("Game Paused!", True, Colors.display_colors["black"]), self.pause_menu.get_text())
                    pygame.draw.rect(self.root, Colors.display_colors["orange"], self.pause_menu.get_button(), 0)
                    self.root.blit(font1.render("Continue", True, Colors.display_colors["black"]), self.pause_menu.get_label())
                    pygame.draw.rect(self.root, Colors.display_colors["orange"], self.pause_menu.get_button2(), 0)
                    self.root.blit(font1.render("Restart", True, Colors.display_colors["black"]), self.pause_menu.get_label2())
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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if round(self.resolution[0] / 2 - 100) <= x <= round(self.resolution[0] / 2 - 100) + 200 and \
                                self.resolution[1] - 70 <= y <= self.resolution[1] - 70 + 60:
                            self.squares = Squares.Squares()
                            self.frame_count = 30
                            self.frame_delay = 30
                            self.key_repeat = 0
                            self.key_delay = 5
                            self.mode = "title"
                if self.mode == "title":
                    continue
                self.root.fill(Colors.display_colors["white"])
                line1 = "Game Over!"
                line2 = f"Score: {self.squares.get_score()}"
                line3 = f"Level: {self.squares.get_level()}"
                line4 = "Home"
                align = max(font1.size(line2)[0], font1.size(line3)[0])
                self.root.blit(font1.render(line1, True, Colors.display_colors["black"]), (round(self.resolution[0] / 2 - font1.size(line1)[0] / 2), 40))
                self.root.blit(font1.render(line2, True, Colors.display_colors["black"]), (round(self.resolution[0] / 2 - align / 2), round(self.resolution[1] / 2 - font1.size(line2)[1])))
                self.root.blit(font1.render(line3, True, Colors.display_colors["black"]), (round(self.resolution[0] / 2 - align / 2), round(self.resolution[1] / 2)))
                pygame.draw.rect(self.root, Colors.display_colors["orange"], [round(self.resolution[0] / 2 - 100), self.resolution[1] - 70, 200, 60], 0)
                self.root.blit(font1.render(line4, True, Colors.display_colors["black"]), (round(self.resolution[0] / 2 - font1.size(line4)[0] / 2), round(self.resolution[1] - 70 + (60 / 2) - (font1.size(line4)[1] / 2))))
                pygame.display.update()
        pygame.quit()

    def draw_pixels(self):
        squares = self.squares.get_pixels()
        width, height = self.squares.get_size()
        if self.resolution[0] / width * height > self.resolution[1] - 30:
            length = (self.resolution[1] - 30) / height
        else:
            length = self.resolution[0] / width
        for row in range(0, height):
            for column in range(0, width):
                x = length * column + round(self.resolution[0] / 2 - length * width / 2)
                y = length * row + 30
                pygame.draw.rect(self.root, squares[row][column], [x + 2, y + 2, length - 4, length - 4], 0)


if __name__ == "__main__":
    Display()
