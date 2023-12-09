import socket
import sys
import json
import time
import re
import pygame
import os

#import login_module
#import talkroom
##########################################################
#牌的邏輯
"""
pos = []
for i in range(1,14):
    pos.append(i)"""

def show_pos(hand_cards):
    for i in hand_cards:
        print("%2s" %i,end=" ")
    print("")
def show_t_pos(table):
    for i in range(len(table)):
        print("%2s" %table[i],end=" ")
    print("")
def convert_graph(card):
    value = suits[(card - 1) // 13] + str((card - 1) % 13 + 1)
    return value

def connect_to_server(server_ip, port):
    server_ip = socket.gethostbyname(server_ip)
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (server_ip, port))
    cSocket.connect((server_ip, port))
    return cSocket



first = 1   #每回合的第一次出牌
hand_cards = []
second = 0
suits = ['D', 'H', 'S', 'C']

#################################################
"""
if not login_module.start_login_interface():
    sys.exit()
if not talkroom.main():
    sys.exit()"""

#通訊部分
bigmsg1 = {
    'table' : '',
    'hand' : '',
    'beat' : ''
}
buf_size=1024
IP = '127.0.0.1'
PORT = 6666
client = connect_to_server(IP,PORT)
down_count = False

msg = client.recv(buf_size) #接收server端反馈的信息编号
client.setblocking(False)
if(msg!='end'):
    print("已连接到ip为{}的server端，本机编号为{}".format(IP,msg.decode('utf-8')))  # 连接成功时将server端ip地址反馈到client端
    #定义client端编号为num  
    num = msg.decode('utf-8')
elif(msg=='end'):
    print("server端连接数量已达上限！当前连接断开！")

##########################################################
#進入遊戲
if msg!='end':
    while True:
        try:
            msg = client.recv(buf_size)
            init_content = json.loads(msg.decode('utf-8'))
     
            hand_cards = init_content[:12] 
            hand_graph = [suits[(value - 1) // 13] + str((value - 1) % 13 + 1) 
                        for value in hand_cards] 
            table_cards = init_content[12:16] 
            table_graph = [suits[(value - 1) // 13] + str((value - 1) % 13 + 1) 
                        for value in table_cards]
            #show_pos(pos)
            #show_pos(hand_cards)
            #show_t_pos(table_cards)
            time.sleep(0.01)
            break    
        except BlockingIOError:
            pass

##########################################################GUI
#GUI初始化

pygame.init()
# 設置遊戲視窗尺寸
screen_width = 1600
screen_height = 900
card_width = 180
card_height = 270
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("撿紅點")

path = "C:\\網路城市\\git_fina\\1.0.2\\card_img\\"
def load_and_scale_card_image(card_name, new_width=card_width, new_height=card_height):
    image = pygame.image.load(os.path.join(path , card_name + '.png'))
    return pygame.transform.scale(image, (new_width, new_height))

# 加載背景圖片
background = pygame.image.load(path + 'BG.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
back_of_card = pygame.image.load(path + 'Back.png')
back_of_card = pygame.transform.scale(back_of_card, (card_width, card_height))  # 假設卡牌的大小為180x270
back_of_card_pos = (screen_width - back_of_card.get_width() - 50, screen_height / 2 - back_of_card.get_height() / 2)
running = True
screen.blit(background, (0, 0))
screen.blit(back_of_card, back_of_card_pos)

#card graph
clock = pygame.time.Clock()
card_width = 180
card_spacing = 100
hand_area_start = 50
hand_area_y = screen_height - 280  # 假設距底部50像素

#跟玩家的牌有關
hand_select = -1
hand_lock = False
hand_dlock = False

#和桌上的牌有關
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
reset_count = True


######################################################GUI
while running:
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
                #4.98秒內出牌
                if num == bigmsg_received['cur']:  
                    bigmsg1['beat'] = 'L'              
                    if first:
                        bigmsg1['hand'] = str(hand_select)
                        first = 0 
                    bigmsg1['table'] = str(table_select)
                    msg_to_send = json.dumps(bigmsg1).encode('utf-8')
                    client.send(msg_to_send)         
                    button_color = RED
                    button_text = "Cards played"
                    button_send_lock = True
                    hand_dlock = True
                    player_timeout = False

                time.sleep(0.001)
            else:
                for i, card_rect in enumerate(hand_card_rects):
                    if card_rect.collidepoint(event.pos) and hand_lock == False:                    
                        hand_select = i + 1 if i > 0 else 0
                        hand_lock = True
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
                        #選卡桌上最後一張bug
                        if i > 0 and i < (len(table_cards) - 1) :
                            table_select = i + 1
                        else:
                            table_select = i
                        table_lock = True
                        break
                    elif card_rect.collidepoint(event.pos) and table_lock == True:
                        table_lock = False
                        table_select = -1
                        break   

#############################################pygame
    try:
        msg = client.recv(buf_size)           # 接收server端发送的当前client编号  
        bigmsg_received = json.loads(msg.decode('utf-8'))
        if bigmsg_received['cur'] == "-1":
            break
        elif bigmsg_received['cur'] == "-2":
            print("有名玩家中斷")
            pygame.quit()
            sys.exit()
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
                    hand_cards.append(number)
                    hand_graph.append(convert_graph(number))
            hand_select = -1
            hand_lock = False
            second = 0
        elif num == bigmsg_received['cur']:
        
            player_timeout = True
            player_wait = False
            
            start_time = time.time()
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
    except json.JSONDecodeError as e:
        # 如果解析錯誤，進入 except 塊
        print(f"JSON 解析錯誤：{e}") 
        print(bigmsg_received)
    except ConnectionError:
        pass
    """except json.JSONDecodeError:
        print("伺服器斷線遊戲中止")
        pygame.quit()
        sys.exit()"""
    if bigmsg_received['cur'] == num:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 0.98 and player_timeout and not player_wait:
            print("超時!!!!!!!!")
            table_select = 0
            hand_lock = True
            table_lock = True
            if first:
                hand_select = 0
                bigmsg1['hand'] = str(hand_select)
                first = 0 
            bigmsg1['table'] = str(table_select)
            msg_to_send = json.dumps(bigmsg1).encode('utf-8')
            client.send(msg_to_send)         
            button_color = RED
            button_text = "Cards played"
            button_send_lock = True
            hand_dlock = True
            player_wait = True
            time.sleep(0.001)

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
client.close()
print("连接已断开！")
# 退出 Pygame
pygame.quit()
sys.exit()


"""
if (num != bigmsg_received['cur'] and second != 0
or num == bigmsg_received['cur']):
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
hand_select = -1"""
"""
當client cur接收到-2 顯示出已有玩家斷線，遊戲中止

-2->show have player disconnect -> while 1-> 3sec -> sys.quit() pygame quit(
"""