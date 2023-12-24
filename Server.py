import socket
import random
import json
import time
import  ServerGame as sm 
import Talkroom.ServerRoomMd as SR
#########################通訊
clients = []
IP = '127.0.0.1'
PORT = 6666
server = SR.set_server(IP,PORT)
clients = SR.room(server)
server.settimeout(8)
buf_size = 1024             #設定預設buf文字區大小
connect_num= 0
cur_p = 0
first_lose_card = True

########################## 遊戲
players = []
table_cards = []
all_msg = {
    'table' : '0',
    'hand' : '0',
    'cur' : '',
}
score = [0,0] 
def init():
    #洗牌
    global poker
    poker = list(range(1, 53)) 
    random.shuffle(poker)
    poker.append(0)
    poker.append(0)
    #init 玩家
    for j in range(2):
        row = []
        for hand in range(12):
            row.append(poker[0])
            poker.pop(0)
        players.append(row)  
    #init 桌上
    for j in range(4):
        table_cards.append(poker[0])
        poker.pop(0)
init()

try:
    print("開始遊戲")
    print("p1:",players[0])
    print("p2",players[1])
    print("table",table_cards)
    result = players[0] + table_cards
    result.append('1')
    data_to_send = json.dumps(result).encode('utf-8')
    clients[0].send(data_to_send)
    result = players[1] + table_cards
    result.append('2')
    data_to_send = json.dumps(result).encode('utf-8')
    clients[1].send(data_to_send)
    time.sleep(0.005)
    cur_p = 0
    all_msg['cur'] = str(cur_p + 1)
    msg_to_send = json.dumps(all_msg).encode('utf-8')
    time.sleep(0.005)
    for j in clients:
        j.send(msg_to_send)
    time.sleep(0.005)

    while poker[0] != 0:
        try:
            if cur_p == len(clients):
                for send_close in clients:  
                    send_close.send(msg_to_send)
                time.sleep(3)
                break
            msg0 = clients[cur_p].recv(buf_size)
            bigmsg_received = json.loads(msg0.decode('utf-8'))      
        except BlockingIOError:
            continue
        except ConnectionAbortedError: #藍方斷線
            del clients[cur_p]       
            all_msg['cur'] = "-2"
            msg_to_send = json.dumps(all_msg).encode('utf-8') #廣播通知遊戲結束
            time.sleep(0.5)
            for send_close in clients:  
                send_close.send(msg_to_send)
            strat_time = time.time()
            while 1:
                current_time = time.time()
                if current_time - strat_time > 8:
                    break
            break   
        except json.JSONDecodeError as e: #綠方斷線 #綠方先斷，藍方後斷
            del clients[cur_p]       
            all_msg['cur'] = "-2"
            msg_to_send = json.dumps(all_msg).encode('utf-8') 
            time.sleep(0.5)
            for send_close in clients:  #廣播通知遊戲結束
                send_close.send(msg_to_send)
            strat_time = time.time()
            while 1:
                current_time = time.time()
                if current_time - strat_time > 8:
                    break
            break
        try:
            number1 = bigmsg_received['hand']
            number1 = int(number1)
            print(players[cur_p][number1])
            if len(players[cur_p]) - 1 < number1:
                number1 = 0
            player_card = players[cur_p][number1]
        except:               #玩家亂輸入
            number1 = 0
            player_card = players[cur_p][number1]
        try:
            number2 =  bigmsg_received['table']
            number2 = int(number2)
            if number2 != 0:
                card_key = table_cards[number2]
            else:
                card_key = table_cards[0]
        except :
            number2 = 1
            print("!")
            if len(table_cards) > 1:
                card_key = table_cards[1]
            else:
                number2 = 0 #桌上沒牌，必定失敗
                card_key = table_cards[0]

        all_msg['hand'] = ''
        print("match %2d %2d" %(player_card,card_key))
        if(sm.Match(player_card,card_key) and card_key != 0): 
            print("配對成功")
            score[cur_p] += sm.PlayerScore(player_card,card_key) 
            all_msg['table'] = '-' + str(card_key) #桌上刪除那張牌
            table_cards.pop(number2)
            all_msg['hand'] = '-' + str(player_card) #刪除手上那張牌
            players[cur_p].pop(number1) 
            sm.show_score(cur_p,score)
        else:
            print("配對失敗")
            all_msg['table'] = '+' + str(player_card) #桌上新增玩家那張牌
            table_cards.append(players[cur_p][number1])
            all_msg['hand'] =  '-' + str(player_card) #刪除手上那張牌
            players[cur_p].pop(number1)
            if poker[0] != 0:
                players[cur_p].append(poker[0])  
                all_msg['hand'] = all_msg['hand'] + '+' + str(poker[0]) #補牌，失敗當作pass
                poker.pop(0)  

        if (not players[cur_p]) and poker[0] != 0: 
            players[cur_p].append(poker[0])
            all_msg['hand'] = all_msg['hand'] + '+' + str(poker[0]) #玩家沒牌，自動補牌
            poker.pop(0)         
        msg_to_send = json.dumps(all_msg).encode('utf-8') #廣播
        for j in  clients:
            j.send(msg_to_send)                        
        sucess = True
        while(sucess and poker[0] != 0):                            
            if sucess:
                all_msg['hand'] = ''
            try:
                if cur_p == len(clients):
                    for send_close in clients:  
                        send_close.send(msg_to_send)
                    time.sleep(3)
                    break
                msg0 = clients[cur_p].recv(buf_size)
                bigmsg_received = json.loads(msg0.decode('utf-8'))
            except BlockingIOError:
                continue
            except ConnectionAbortedError: #藍方斷線
                del clients[cur_p]       
                all_msg['cur'] = "-2"
                msg_to_send = json.dumps(all_msg).encode('utf-8') #廣播
                time.sleep(0.5)
                for send_close in clients:  
                    send_close.send(msg_to_send)
                strat_time = time.time()
                while 1:             
                    current_time = time.time()
                    if current_time - strat_time > 8:
                        print("191")
                        break
                break   
            except json.JSONDecodeError as e: #綠方斷線
                del clients[cur_p]       
                all_msg['cur'] = "-2"
                msg_to_send = json.dumps(all_msg).encode('utf-8') #廣播
                time.sleep(0.5)
                for j in clients:
                    try:
                        j.send(msg_to_send)
                    except ConnectionAbortedError: #兩個玩家都中斷了
                        print("兩名玩家都中斷了1")
                       # break
                strat_time = time.time()
                while 1:
                    current_time = time.time()
                    if current_time - strat_time > 8:
                        break
                break
            lenth = len(players[cur_p]) - 1 
            player_card = players[cur_p][lenth]
            try:
                number2 =  bigmsg_received['table'] #玩家選擇那桌上那張             
                number2 = int(number2)
                if  number2 > 0 and len(table_cards) > number2:
                    card_key = table_cards[number2]
                else:
                    card_key = table_cards[0]
            except :
                number2 = 1
                if len(table_cards) > 1:
                    print("無效張，自動選擇第1張<<")
                    card_key = table_cards[1]
                else:
                    print("桌上沒牌，必定失敗<<")
                    number2 = 0
                    card_key = table_cards[0]
            print("match %2d %2d" %(player_card,card_key))
            if(sm.Match(player_card,card_key) and card_key != 0):     
                print("配對成功")
                score[cur_p] += sm.PlayerScore(player_card,card_key)
                sm.show_score(cur_p,score)
                all_msg['table'] = '-' + str(card_key) 
                table_cards.pop(number2)  
                all_msg['hand'] = '-' + str(player_card)
                players[cur_p].pop(lenth)
            else:
                print("配對失敗了")
                all_msg['table'] = '+' + str(player_card)
                table_cards.append(player_card)     
                all_msg['hand'] = '-' + str(player_card) 
                players[cur_p].pop(lenth)
                sucess = False
                cur_p += 1 #下個玩家
                if(cur_p == len(clients)):
                    cur_p = 0                    
                all_msg['cur'] = str(cur_p + 1)

            if sucess:
                if not players[cur_p] and poker[0] != 0:
                    players[cur_p].append(poker[0])
                    all_msg['hand'] = all_msg['hand'] + '+' + str(poker[0])
                    poker.pop(0)  
            else:
                if not players[(cur_p + 1) % len(clients)] and poker[0] != 0:
                    players[(cur_p + 1) % len(clients)].append(poker[0])
                    all_msg['hand'] = all_msg['hand'] + '+' + str(poker[0])
                    poker.pop(0) 
            msg_to_send = json.dumps(all_msg).encode('utf-8')     
            for j in clients:
                try:
                    j.send(msg_to_send)
                except ConnectionAbortedError: #兩個玩家都中斷了
                    break
    print("遊戲結束")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    time.sleep(0.5)
    all_msg['cur'] = '-1'
    #廣播通知遊戲結束
    for i,send_close in enumerate(clients): 
        try:
            all_msg['hand'] = score[i]
            msg_to_send = json.dumps(all_msg).encode('utf-8')
            send_close.send(msg_to_send)
        except ConnectionAbortedError:
            clients.remove(send_close)
    time.sleep(0.5)
except socket.timeout:
    time.sleep(3)
    server.close() #关闭监听主socket，服务端程序结束
    print("连接已断开！")



