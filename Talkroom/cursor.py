import pygame
import sys

class Cursor:
    def __init__(self, font, input_box):
        self.surface = font.render("|", True, (41, 226, 243))  # 光标显示为竖线
        self.width = self.surface.get_width()  # 光标的宽度
        self.blink = True  # 初始为True表示光标可见
        self.timer = 0  # 用于控制光标闪烁速度的计时器
        self.input_box = input_box
        self.pos = 0
    def update(self):
        # 控制光标的闪烁
        self.timer += 1
        if self.timer >= 2500:  # 控制光标的闪烁速度，数字越大闪烁速度越慢
            self.blink = not self.blink
            self.timer = 0

    def draw(self, window, input_surface):
        # 绘制光标
        if self.blink:  # 如果光标可见，则绘制光标
            cursor_x = self.input_box.x + input_surface.get_width() + 3 
            window.blit(self.surface, (cursor_x, self.input_box.y + 5))
    def adjust_cursor_position(text, mouse_x):
        # 计算点击位置对应的光标位置
        cursor_x = mouse_x - input_box.x - 5
        # 找到离光标位置最近的字符索引
        char_index = len(text)
        total_width = 0
        for i, char in enumerate(text):
            char_width = font.size(char)[0]
            total_width += char_width
            if total_width >= cursor_x:
                char_index = i
                break
        # 插入竖线字符以显示光标位置
        adjusted_text = text[:char_index] + "|" + text[char_index:]
        return adjusted_text