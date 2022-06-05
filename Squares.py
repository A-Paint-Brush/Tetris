import Colors
import Shapes
import random


class Squares:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.pixels = [list(Colors.display_colors["grey"] for column in range(self.width)) for row in range(self.height)]
        self.hit_box = [list(0 for column in range(self.width)) for row in range(self.height)]
        self.shape = None
        self.letter_bag = ["O", "I", "J", "L", "S", "T", "Z"]
        self.score = 0
        self.level = 0
        self.level_up = 10 * (self.level + 1)
        self.row_counter = 0

    def get_score(self):
        return self.score

    def get_level(self):
        return self.level

    def get_pixels(self):
        return self.pixels

    def get_size(self):
        return self.width, self.height

    def has_shape(self):
        if self.shape is None:
            return False
        else:
            return True

    def spawn_new(self):
        letter = self.letter_bag.pop(random.randint(0, len(self.letter_bag) - 1))
        if len(self.letter_bag) == 0:
            self.letter_bag = ["O", "I", "J", "L", "S", "T", "Z"]
        self.shape = Shapes.Shape(letter, self.hit_box, (self.width, self.height))
        if self.shape.spawn_collision()[0] == 0:
            self.shape.render_current_frame(self.pixels)
            return False
        else:
            self.shape = None
            return True

    def move_right(self):
        if self.shape is None:
            return None
        self.shape.clear_prev_frame(self.pixels)
        self.shape.move_right()
        self.shape.render_current_frame(self.pixels)

    def move_left(self):
        if self.shape is None:
            return None
        self.shape.clear_prev_frame(self.pixels)
        self.shape.move_left()
        self.shape.render_current_frame(self.pixels)

    def rotate_right(self):
        if self.shape is None:
            return None
        self.shape.clear_prev_frame(self.pixels)
        self.shape.rotate_right()
        self.shape.render_current_frame(self.pixels)

    def move_down(self):
        if self.shape is None:
            return None
        self.shape.clear_prev_frame(self.pixels)
        if not self.shape.move_down():
            self.shape.settle(self.pixels)
            rows = self.shape.clear_rows(self.pixels)
            self.shape = None
            self.score += (0, 40, 100, 300, 1200)[rows] * (self.level + 1)
            self.row_counter += rows
            if self.row_counter >= self.level_up:
                self.row_counter -= self.level_up
                self.level += 1
                self.level_up = 10 * (self.level + 1)
        else:
            self.shape.render_current_frame(self.pixels)


if __name__ == "__main__":
    Squares()
