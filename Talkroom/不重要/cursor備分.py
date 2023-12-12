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
"""
#pygame.init()
pygame.init()
input_box = pygame.Rect(10, 320, 380, 50)
font = pygame.font.Font(None, 36)

# 初始化Pygame
pygame.init()

# 设置窗口大小和标题
window_size = (400, 400)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("")

# 创建用于显示聊天消息的文本框和用于输入消息的文本框
font = pygame.font.Font(None, 36)
chat_box = pygame.Rect(10, 15, 380, 300)
input_box = pygame.Rect(10, 320, 380, 50)

# 创建文本输入框和聊天框的初始文本
input_text = ""
chat_text = ""
chat_history = []

# 创建光标对象
cursor = Cursor(font, input_box)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # 用户按下回车键，发送消息
                chat_history.append("You: " + input_text )
                input_text = ""
                
            elif event.key == pygame.K_BACKSPACE:
                # 用户按下Backspace键，删除最后一个字符
                input_text = input_text[:-1]
            elif event.key == pygame.K_LEFT:
                cursor.pos -= 1
            elif event.key == pygame.K_RIGHT:
                cursor.pos += 1
                pass
            else:
                # 用户输入消息
                if len(input_text) < 20:
                    input_text += event.unicode

    # 清空屏幕
    window.fill((255, 255, 255))

    # 绘制聊天消息框和输入框
    pygame.draw.rect(window, (0, 0, 0), chat_box, 2)
    pygame.draw.rect(window, (0, 0, 0), input_box, 2)
    if len(chat_history) > 10:
        chat_history.pop(0)
    
    # 显示聊天消息和输入文本
    for i , chat_sigle in enumerate(chat_history):
        chat_surface = font.render(chat_sigle, True, (0, 0, 0))
        window.blit(chat_surface, (chat_box.x + 5, chat_box.y + 30 * i))

    position_to_remove = (len(input_text) + cursor.pos) 
    cursor_track_input_surface = font.render("You: " + input_text[:position_to_remove], True, (0, 0, 0))
    input_surface = font.render("You: " + input_text, True, (0, 0, 0))
    window.blit(input_surface, (input_box.x + 5, input_box.y + 5))
    
    # 更新和绘制光标
    cursor.update()
    cursor.draw(window, cursor_track_input_surface)

    pygame.display.flip()"""