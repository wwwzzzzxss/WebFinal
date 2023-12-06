
import socket

def set_server(IP,PORT):
    back_log = 1                #設定客戶端最大監聽數量         
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 初始化TCP連線的socket
    server.settimeout(50)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # 對socket的配置重複使用ip和連接埠號
    server.bind((IP,PORT))              #綁定連接埠號碼和socket
    server.listen(back_log)           #設定socket端監聽
    print("成功创建socket,等待client端連線中...")
    server.setblocking(False)
    return server