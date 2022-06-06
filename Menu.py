class Menu:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.text_x = 0
        self.text_y = 0
        self.btn_x = 0
        self.btn_y = 0
        self.btn_width = 180
        self.btn_height = 40
        self.label_x = 0
        self.label_y = 0
        self.width = 300
        self.height = 200
        self.pause = False

    def is_paused(self):
        return self.pause

    def toggle_pause(self):
        self.pause = not self.pause

    def relocate(self, resolution, font1):
        self.x = round(resolution[0] / 2 - self.width / 2)
        self.y = round(resolution[1] / 2 - self.height / 2)
        text = "Game Paused!"
        self.text_x = round(resolution[0] / 2 - font1.size(text)[0] / 2)
        self.text_y = round(resolution[1] / 2 - font1.size(text)[1]) - 10
        self.btn_x = round(resolution[0] / 2 - self.btn_width / 2)
        self.btn_y = round(resolution[1] / 2) + 10
        text = "Continue"
        self.label_x = round(resolution[0] / 2 - font1.size(text)[0] / 2)
        self.btn_height = font1.size(text)[1]
        self.label_y = round(resolution[1] / 2) + 10

    def get_btn_hit_box(self):
        return self.btn_x, self.btn_x + self.btn_width, self.btn_y, self.btn_y + self.btn_height

    def get_rect(self):
        return [self.x, self.y, self.width, self.height]

    def get_text(self):
        return self.text_x, self.text_y

    def get_button(self):
        return [self.btn_x, self.btn_y, self.btn_width, self.btn_height]

    def get_label(self):
        return self.label_x, self.label_y
