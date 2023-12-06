import socket
import sys
import json
import time
import re
import pygame
import os
import math
##########################################################
#牌的邏輯

pos = []
for i in range(1,14):
    pos.append(i)
def show_pos(hand_cards):
    for i in hand_cards:
        print("%2s" %i,end=" ")
    print("")
def show_t_pos(table):
    for i in range(len(table)):
        print("%2s" %table[i],end=" ")
    print("")
first = 1   #每回合的第一次出牌
hand_cards = []
second = 0
#################################################

#通訊部分

bigmsg1 = {
    'table' : '',
    'hand' : '',
    'beat' : ''
}
buf_size=1024
p = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建socket并设置server端连接的IP地址和端口
ip1 = '127.0.0.1'
p.connect((ip1,1234))
msg = p.recv(buf_size) #接收server端反馈的信息编号
p.setblocking(False)
if(msg!='end'):
    print("已连接到ip为{}的server端，本机编号为{}".format(ip1,msg.decode('utf-8')))  # 连接成功时将server端ip地址反馈到client端
    #定义client端编号为num  
    num = msg.decode('utf-8')
elif(msg=='end'):
    print("server端连接数量已达上限！当前连接断开！")

#######################################################

##########################################################
#進入遊戲
suits = ['D', 'H', 'S', 'C']
def convert_graph(card):
    value = suits[(card - 1) // 13] + str((card - 1) % 13 + 1)
    return value
#成功连接时开启主循环

    

if(msg!='end'):
    while True:
        try:
            msg = p.recv(buf_size)
            init_content = json.loads(msg.decode('utf-8'))
            hand_cards = init_content[:4] #:12
            hand_graph = [suits[(value - 1) // 13] + str((value - 1) % 13 + 1) 
                        for value in hand_cards] 
            table_cards = init_content[4:16] #12:16
            table_graph = [suits[(value - 1) // 13] + str((value - 1) % 13 + 1) 
                        for value in table_cards]
            show_pos(pos)
            show_pos(hand_cards)

            show_t_pos(table_cards)
            time.sleep(0.1)
            break    
        except BlockingIOError:
            pass
    #GUI初始化

pygame.init()

# 設置遊戲視窗尺寸
screen_width = 1600
screen_height = 900
card_width = 180
card_height = 270
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("撿紅點")

path = "C:\\網路城市\\git_fina\\"
# 加載背景圖片
background = pygame.image.load(path + 'BG.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

back_of_card = pygame.image.load(path + 'Back.png')
back_of_card = pygame.transform.scale(back_of_card, (card_width, card_height))  # 假設卡牌的大小為180x270
back_of_card_pos = (screen_width - back_of_card.get_width() - 50, screen_height / 2 - back_of_card.get_height() / 2)

def load_and_scale_card_image(card_name, new_width=card_width, new_height=card_height):
    image = pygame.image.load(os.path.join(path + 'card_img', card_name + '.png'))
    return pygame.transform.scale(image, (new_width, new_height))

running = True
screen.blit(background, (0, 0))
screen.blit(back_of_card, back_of_card_pos)

clock = pygame.time.Clock()
card_width = 180
card_spacing = 100
hand_area_start = 50
hand_area_y = screen_height - 280  # 假設距底部50像素

hand_select = -1
hand_lock = False
hand_dlock = False

table_select = -1
table_lock = False

"""有關table
table_lock
table_card_rects
table_cards
table_graph
table_int
table_select"""

# 按鈕

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
color_text = (200, 200, 200)
font = pygame.font.SysFont("Arial", 35)
button_color = BLUE
button_send_lock = False
button_lock = True
button_text = "Not your turn"
hand_card_rects = []


animation_shown_cards = []

while running:
#############################################pygame
    screen.blit(background, (0, 0))
    screen.blit(back_of_card, back_of_card_pos)
    pygame.draw.rect(screen, button_color, (screen_width / 2, screen_height / 2, 
                                            100, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            
            if (text_rect.collidepoint(event.pos) and not button_lock
                and hand_lock  and table_lock and not button_send_lock):        
                if num == bigmsg_received['cur']:
                    bigmsg1['beat'] = 'L'              
                    if first:
                        bigmsg1['hand'] = str(hand_select)
                        first = 0 
                    bigmsg1['table'] = str(table_select)
                    msg_to_send = json.dumps(bigmsg1).encode('utf-8')
                    p.send(msg_to_send)
                    button_color = RED
                    button_text = "Cards played"
                    button_send_lock = True
                    hand_dlock = True
                time.sleep(0.1)
            else:
                for i, card_rect in enumerate(hand_card_rects):
                    if card_rect.collidepoint(event.pos) and hand_lock == False:                    
                        hand_select = i + 1 if i > 0 else 0
                        hand_lock = True
                        print("")
                        break
                    elif card_rect.collidepoint(event.pos) and hand_lock == True:
                        if not hand_dlock:
                            hand_lock = False
                            hand_select = -1
                            hand_card_rects = []
                        break                   
                # 選擇的牌桌上
                for i, card_rect in enumerate(table_card_rects):
                    if card_rect.collidepoint(event.pos) and table_lock == False:           
                        table_select = i + 1 if i > 0 else 0
                        table_lock = True
                        break
                    elif card_rect.collidepoint(event.pos) and table_lock == True:
                        table_lock = False
                        table_select = -1
                        break     


#############################################pygame
    try:
        msg = p.recv(buf_size)           # 接收server端发送的当前client编号  
        bigmsg_received = json.loads(msg.decode('utf-8'))
        if bigmsg_received['cur'] == "-1":
            break
        table_int = int(bigmsg_received['table'])
        if table_int < 0:
            try:
                table_cards.remove(-table_int)
                table_graph.remove(convert_graph(-table_int))
            except ValueError:
                print("t value error")
        elif table_int> 0:
            table_cards.append(table_int)
            table_graph.append(convert_graph(table_int))
        show_t_pos(table_cards)
        table_select = -1
        table_lock = False

        if num != bigmsg_received['cur'] and second != 0: 
            button_color = BLUE
            button_text = "Not your turn"
            hand_dlock = False
            
            numbers = list(map(int,re.findall(r'[+-]?\d+',bigmsg_received['hand'] )))
            for number in numbers:
                if number < 0:
                    try:
                        hand_cards.remove(-number)
                        hand_graph.remove(convert_graph(-number))
                    except ValueError:
                        print('error num=',number)
                        print("h value error")
                elif number > 0 :
                    print("桌上空的",number)
                    hand_cards.append(number)
                    hand_graph.append(convert_graph(number))
                hand_select = -1
                hand_lock = False
                show_pos(pos)
                show_pos(hand_cards)
                if not hand_select:
                    hand_select = 0
                else:
                    hand_select = len(hand_cards) - 1
                second = 0
        elif num == bigmsg_received['cur']:
            bigmsg1['beat'] = 'D'
            button_send_lock = False
            button_lock = False
            button_color = GREEN
            button_text = "Your turn"
            if second == 0:   
                second += 1
                first = 1
            else:
                numbers = list(map(int,re.findall(r'[+-]?\d+',bigmsg_received['hand'] )))
                for number in numbers:
                    if number < 0:
                        try:
                            hand_cards.remove(-number)
                            hand_graph.remove(convert_graph(-number))
                        except ValueError:
                            print('error num=',number)
                            print("h value error")
                    elif number > 0 : 
                        hand_cards.append(number)
                        hand_graph.append(convert_graph(number))
                    hand_select = -1
                if not hand_select:
                    hand_select = 0
                else:
                    hand_select = len(hand_cards) - 1
                
                show_pos(hand_cards)
    except BlockingIOError:
        pass


    mouse_h_x, mouse_h_y = pygame.mouse.get_pos()  


    active_card_index = None  
    for i, card_name in enumerate(hand_graph):           
        card = load_and_scale_card_image(card_name)
        card_rect = card.get_rect(topleft=(50 +  i * card_spacing, card.get_height() + 320))
        # 先檢查是否為最右邊一張  再檢查滑鼠是否在牌的主要部分上方
        if i == len(hand_graph) - 1:
            if card_rect.collidepoint(mouse_h_x,mouse_h_y):
                active_card_index = i
        else:
            if card_rect.collidepoint(mouse_h_x, mouse_h_y) and (mouse_h_x < card_rect.right - card_spacing // 1.25):
                active_card_index = i      
        # 根據活躍牌索引處理牌的顯示
        if i == active_card_index and not hand_lock:
            card_rect.y -= 20  # 將活躍的牌向上移動        
        elif i == hand_select and hand_lock == True:
            print("鎖哪張",hand_select)
            card_rect.y -= 20
        hand_card_rects.append(card_rect)
        screen.blit(card, card_rect)

    table_card_rects = []
    active_card_index = None
    for i, card_name in enumerate(table_graph):           
        card = load_and_scale_card_image(card_name)
        card_rect = card.get_rect(topleft=(50 +  i * card_spacing, 100))
        # 先檢查是否為最右邊一張  再檢查滑鼠是否在牌的主要部分上方
        if i == len(table_graph) - 1:
            if card_rect.collidepoint(mouse_h_x,mouse_h_y):
                active_card_index = i
        else:
            if card_rect.collidepoint(mouse_h_x, mouse_h_y) and (mouse_h_x < card_rect.right - card_spacing // 1.25):
                active_card_index = i      
        # 根據活躍牌索引處理牌的顯示
        if i == active_card_index and table_lock == False:
            card_rect.y -= 20  # 將活躍的牌向上移動        
        elif i == table_select and table_lock == True:
            card_rect.y -= 20
        table_card_rects.append(card_rect)
        screen.blit(card, card_rect)


    text_clicked = font.render(button_text, True, color_text)
    text_rect = text_clicked.get_rect(center=(screen_width/2, 
                                                screen_height/2))
    text_rect.center = (screen_width/2 + 50, screen_height/2 + 25)
    screen.blit(text_clicked, text_rect)
    pygame.display.flip()
p.close()
print("连接已断开！")
# 退出 Pygame
pygame.quit()
sys.exit()




