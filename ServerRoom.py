import ServerRoomMd as SR


IP = '127.0.0.1'
PORT = 6666
server = SR.set_server(IP,PORT)
play_clients = SR.room(server)
