####################################################
#  Network Programming - Unit 8 Non-blocking Socket         
#  Program Name: 1-NonblockingClient.py                                      			
#  The program is a simple non-blocking TCP client.            		
#  2021.07.29                              
#python 1-NonblockingClient.py 127.0.0.1                    									
####################################################
import sys
import socket
import time
import pygame
pygame.init()
input_x = 10
input_box = pygame.Rect(10, 320, 380, 50)
font = pygame.font.Font(None, 36)
from Talkroom.cursor import Cursor

buff_size = 1024
def set_client(serverIP,PORT):
	serverIP = socket.gethostbyname(serverIP)
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))
	cSocket.setblocking(False)
	return cSocket

def insert_text(string,pos,instring):
    position_to_insert = (len(string) + pos)
    new_string = string[:position_to_insert] + instring + string[position_to_insert:]
    return new_string

def delete_text(string,pos):
    position_to_remove = (len(string) + pos) - 1
    if position_to_remove < 0:
        return string
    else:
        new_string = string[:position_to_remove ] + string[position_to_remove + 1:]
        return new_string

def main(cSocket):
	global input_x
	global input_box
	global font
	# 创建文本输入框和聊天框的初始文本
	input_text = ""
	BLACK = (0,0,0)
	YELLOW = (255,255,0)
	WHITE = (255,255,255)
	input_color = BLACK
	input_active = False

	chat_history = []
	cursor_pos = 0

	# 创建光标对象
	cursor = Cursor(font, input_box)
	
	# 设置窗口大小和标题
	window_width = 400
	window_height = 440
	window_size = (window_width,window_height)
	window = pygame.display.set_mode(window_size)
	pygame.display.set_caption("小聊天室")
	start_button = pygame.Rect(window_width - 105 , window_height - 55 , 100, 50)
	start_text = font.render("Start", True, WHITE)

	# "Exit" 按鈕
	exit_button = pygame.Rect(5, window_height - 55 , 100, 50)
	exit_text = font.render("Exit", True, WHITE)

	# 创建用于显示聊天消息的文本框和用于输入消息的文本框
	chat_box = pygame.Rect(10, 15, 380, 300)

	started = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				cSocket.close()
				return False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if (input_box.x < event.pos[0] < input_box.x + input_box.width and 
					input_box.y < event.pos[1] < input_box.y + input_box.height):
					if input_active:
						input_active = False
						input_color = BLACK
					else:
						input_active = True
						input_color = YELLOW
				elif exit_button.collidepoint(event.pos):
					cSocket.close()
					pygame.quit()
					sys.exit()
				elif start_button.collidepoint(event.pos):
					if not started:
						response_msg = '-*-start-*-'
						print("傳了")
						cSocket.send(response_msg.encode('utf-8'))
						response_msg = ''
						started = True
					
			elif event.type == pygame.KEYDOWN:
				if input_active:
					if event.key == pygame.K_RETURN and input_text:
						# 用户按下回车键，发送消息
						chat_history.append("You: " + input_text )
						cSocket.send(input_text.encode('utf-8'))
						input_text = ""
					elif event.key == pygame.K_BACKSPACE:
						# 用户按下Backspace键，删除最后一个字符
						input_text = delete_text(input_text,cursor_pos)
					elif pygame.key.get_pressed()[pygame.K_LEFT]:
						if len(input_text) + cursor_pos - 1 >= 0:
							cursor_pos -= 1
					elif pygame.key.get_pressed()[pygame.K_RIGHT]:
						if cursor_pos < 0:
							cursor_pos += 1
					else:
						if len(input_text) < 20:
							input_text =  insert_text(input_text,cursor_pos,event.unicode)            
		try:
			server_reply = cSocket.recv(buff_size).decode('utf-8')
			if server_reply[0] == "C":
				chat_history.append("Other: " + server_reply[1:])
			elif server_reply[0] == "S":
				if server_reply[1:] == "start":
					chat_history.append("Server: " + server_reply[1:])
					chat_history.append("Server: " + "will start")
					time.sleep(2)	
					return True
				elif server_reply[1:] == "exit":
					chat_history.append("Server: " + server_reply[1:])
					chat_history.append("Server: " + "The room will close")
					time.sleep(2)	
					return False
				else:
					chat_history.append("Server: " + server_reply[1:])
			server_reply = ""
		except BlockingIOError:
			pass
		# 清空屏幕FG
		window.fill((255, 255, 255))

		# 绘制聊天消息框和输入框
		pygame.draw.rect(window, (0, 0, 0), chat_box, 2)
		pygame.draw.rect(window, input_color, input_box, 2)
		pygame.draw.rect(window, BLACK, start_button)
		pygame.draw.rect(window, BLACK, exit_button)
	
		if len(chat_history) > 10:
			chat_history.pop(0)

		# 显示聊天消息和输入文本
		for i , chat_sigle in enumerate(chat_history):
			chat_surface = font.render(chat_sigle, True, (0, 0, 0))
			window.blit(chat_surface, (chat_box.x + 5, chat_box.y + 30 * i))
		window.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
		window.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))


		position_to_remove = (len(input_text) + cursor_pos) 
		cursor_track_input_surface = font.render("You: " + input_text[:position_to_remove], True, BLACK)	
		# 更新和绘制光标
		cursor.update()
		cursor.draw(window, cursor_track_input_surface)
		
		input_surface = font.render("You: " + input_text, True, BLACK)
		window.blit(input_surface, (input_box.x + 5, input_box.y + 5))
		
		pygame.display.flip()
# end of main

if __name__ == '__main__':
	buff_size = 1024			
	IP = '127.0.0.1'
	PORT = 6666
	client = set_client(IP,PORT)
	time.sleep(0.01)
	try:
		id = client.recv(buff_size).decode('utf-8')
		if id == 'close':
			print("伺服器拒絕服務")
	except BlockingIOError:
		pass
	main(client)

