import pygame
import sys
import socket
import time


def create_button(text, position):
    # 创建按钮矩形
    button_rect = pygame.Rect(position[0], position[1], 100, 40)
    button_color = (0, 0, 0)  # 黑色按钮

    # 创建字体对象
    font = pygame.font.Font(None, 36)

    # 创建文本
    button_text = font.render(text, True, (255, 255, 255))  # 白色文本

    return button_rect, button_color, button_text

def connect_to_server(server_ip, port):
    server_ip = socket.gethostbyname(server_ip)
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (server_ip, port))
    cSocket.connect((server_ip, port))
    cSocket.setblocking(False)
    return cSocket

tmp = connect_to_server('127.0.0.1',6666)

def talkroom(cSocket):
    send_server = 0
    pygame.init()

    width, height = 400, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("黑白背景切换")

    start_button_rect, start_button_color, start_button_text = create_button("start", (width - 130, height - 70))
    exit_button_rect, exit_button_color, exit_button_text = create_button("exit", (30, height - 70))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # 在这里执行游戏开始的操作
                    if send_server == 0:
                        msg = 'start'
                        cSocket.send(msg.encode('utf-8'))
                        send_server = 1
                    time.sleep(0.01)
                elif exit_button_rect.collidepoint(event.pos):
                    if send_server == 0:
                        cSocket.send('exit'.encode('utf-8'))
                    time.sleep(0.01)
                    running = False
                    break
        try:
            start_msg = cSocket.recv(1024).decode('utf-8')
            if start_msg == 'start': 
                print("進入遊戲")
                running = False
                break
        except BlockingIOError:
            pass
        screen.fill((255, 255, 255))  # 白色背景

        # 绘制开始按钮
        pygame.draw.rect(screen, start_button_color, start_button_rect)
        text_rect = start_button_text.get_rect(center=start_button_rect.center)
        screen.blit(start_button_text, text_rect)

        # 绘制退出按钮
        pygame.draw.rect(screen, exit_button_color, exit_button_rect)
        text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_button_text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

talkroom(tmp)