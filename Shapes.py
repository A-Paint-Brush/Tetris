import random
import Colors
shape_data = {
    "O": ((1, 1),
          (1, 1)),
    "I": ((0, 0, 0, 0),
          (1, 1, 1, 1),
          (0, 0, 0, 0),
          (0, 0, 0, 0)),
    "J": ((0, 0, 0),
          (1, 1, 1),
          (0, 0, 1)),
    "L": ((0, 0, 0),
          (1, 1, 1),
          (1, 0, 0)),
    "S": ((0, 0, 0),
          (0, 1, 1),
          (1, 1, 0)),
    "T": ((0, 0, 0),
          (1, 1, 1),
          (0, 1, 0)),
    "Z": ((0, 0, 0),
          (1, 1, 0),
          (0, 1, 1))
}
shape_colors = {
    "O": (255, 255, 0),
    "I": (0, 255, 255),
    "J": (0, 0, 255),
    "L": (255, 165, 0),
    "S": (0, 255, 0),
    "T": (255, 0, 255),
    "Z": (255, 0, 0)
}


class Shape:
    def __init__(self, piece, hit_box, board_size):
        self.x = 0
        self.y = 0
        self.color = shape_colors[piece]
        self.hit_box = hit_box
        self.board_size = board_size
        self.pixels = [list(i) for i in shape_data[piece]]
        self.length = len(self.pixels)
        for i in range(random.randint(0, 3)):
            self.rotate_right(True)
        self.top_index = 0
        for self.top_index in range(self.length):
            if any(self.pixels[self.top_index]):
                break
        self.left_index = 0
        for self.left_index in range(self.length):
            if any(self.pixels[i][self.left_index] for i in range(self.length)):
                break
        self.right_index = self.length - 1
        for self.right_index in range(self.length - 1, -1, -1):
            if any(self.pixels[i][self.right_index] for i in range(self.length)):
                break
        self.y -= self.top_index
        self.x = random.randint(-self.left_index, board_size[0] - self.length + (self.length - self.right_index) - 1)

    def spawn_collision(self):
        return self.detect_collision(self.pixels)

    def clear_prev_frame(self, display_board):
        for row in range(self.y, self.y + self.length):
            for column in range(self.x, self.x + self.length):
                if self.pixels[row - self.y][column - self.x] == 1:
                    if row < 0:
                        continue
                    display_board[row][column] = Colors.display_colors["grey"]

    def render_current_frame(self, display_board):
        for row in range(self.y, self.y + self.length):
            for column in range(self.x, self.x + self.length):
                if self.pixels[row - self.y][column - self.x] == 1:
                    if row < 0:
                        continue
                    display_board[row][column] = self.color

    def detect_collision(self, pixels):
        for row in range(self.y, self.y + self.length):
            for column in range(self.x, self.x + self.length):
                if pixels[row - self.y][column - self.x] == 1:
                    if column < 0:
                        return 1, 0
                    if column > self.board_size[0] - 1:
                        return 1, 1
                    if row < 0:
                        continue
                    if row > self.board_size[1] - 1:
                        return 2, None
                    if self.hit_box[row][column] == 1:
                        return 3, None
        return 0, None

    def clear_rows(self, display_board):
        row_cleared = False
        for row in range(self.board_size[1] - 1, -1, -1):
            if all(self.hit_box[row]):
                for i in range(row, 0, -1):
                    self.hit_box[i] = self.hit_box[i - 1]
                    display_board[i] = display_board[i - 1]
                self.hit_box[0] = [0 for i in range(self.board_size[0])]
                display_board[0] = [Colors.display_colors["grey"] for i in range(self.board_size[0])]
                row_cleared = True
                break
        if row_cleared:
            return 1 + self.clear_rows(display_board)
        else:
            return 0

    def rotate_right(self, no_clip=False):
        rotated = [list(0 for column in range(self.length)) for row in range(self.length)]
        for column in range(0, self.length):
            for row in range(self.length - 1, -1, -1):
                rotated[column][self.length - row - 1] = self.pixels[row][column]
        if no_clip:
            self.pixels = rotated
            return None
        collision = self.detect_collision(rotated)
        if collision[0] in (2, 3):
            return False
        elif collision[0] == 1:
            if (self.move_right, self.move_left)[collision[1]](rotated):
                self.pixels = rotated
                return True
            else:
                return False
        else:
            self.pixels = rotated
            return True

    def move_left(self, rotated=None):
        if rotated is None:
            pixels = self.pixels
        else:
            pixels = rotated
        self.x -= 1
        if self.detect_collision(pixels)[0] == 0:
            return True
        else:
            self.x += 1
            return False

    def move_right(self, rotated=None):
        if rotated is None:
            pixels = self.pixels
        else:
            pixels = rotated
        self.x += 1
        if self.detect_collision(pixels)[0] == 0:
            return True
        else:
            self.x -= 1
            return False

    def move_down(self):
        self.y += 1
        collision = self.detect_collision(self.pixels)
        if collision[0] in (2, 3):
            self.y -= 1
            return False
        elif collision[0] == 0:
            return True

    def settle(self, display_board):
        for row in range(self.y, self.y + self.length):
            for column in range(self.x, self.x + self.length):
                if self.pixels[row - self.y][column - self.x] == 1:
                    self.hit_box[row][column] = 1
                    display_board[row][column] = self.color
