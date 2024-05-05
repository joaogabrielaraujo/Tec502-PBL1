import socket
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import *
import queue 
import time
import os

app = Flask(__name__)
CORS(app)

tcp_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


IP = os.getenv("IP", "127.0.0.1")
SERVER_UDP_PORT =  int(os.getenv("SERVER_UDP_PORT", "8889"))
SERVER_TCP_PORT =  int(os.getenv("SERVER_TCP_PORT", "9999"))


global msg 
msg = ""

clientes_tcp = []

#inicilizando as filas
udp_message_queue = queue.Queue()
http_messages = queue.Queue()



def Registrar_dipositivo_TCP(client_socket, address): 
    print(f"Conexão TCP estabelecida com {address}")
    dispositivo = {"socket": client_socket,  "ip": address[0], "porta_tcp": address[1], "estado": "desligado", "temperatura": 0}
    clientes_tcp.append(dispositivo)
    print("Clientes TCP:", clientes_tcp)


def verificar_conexao_dispositivos():
    while True:
        for dispositivo in clientes_tcp:
            try:
                # Enviar uma mensagem de verificação para o dispositivo
                dispositivo['socket'].send(bytes("Verificando",'utf-8'))
            except Exception as e:
                print(f"Erro: {e}")
                print(f"Conexão perdida com {dispositivo['ip']}:{dispositivo['porta_tcp']}")
                clientes_tcp.remove(dispositivo)
                print("Clientes TCP atualizados:", clientes_tcp)
        
        # Aguardar um tempo antes da próxima verificação
        time.sleep(20)  # Verificar a conexão a cada 20 segundos


# Função para armazenar as mensagens que chegam via udp em uma fila
def handle_udp_connection(udp_socket):
    print("Aguardando mensagens UDP...")
    while True:
        data, address = udp_socket.recvfrom(1024)
        # Coloca a mensagem na fila
        udp_message_queue.put((data.decode('utf-8'), address)) 


def process_udp_messages():
    while True:
        if not udp_message_queue.empty():
            # Obtém a mensagem e o endereço da fila
            message, address = udp_message_queue.get()
            # Processa a mensagem como desejado
            #print(f"Processando mensagem UDP de {address}: {message}")
            partes = message.split('-') 
            tipo = partes[0] 
            estado = partes[1] 
            temperatura = partes[2]
            

            if tipo == "status": 
                for dispositivo in clientes_tcp: 
                    if dispositivo['ip'] == address[0]: 
                        dispositivo["estado"] = estado
                        dispositivo["temperatura"] = temperatura

            print(clientes_tcp)


def process_http_messages():
    while True:
        if not http_messages.empty():
            partes = http_messages.get()
            comando = partes[0] 
            ip_dispositivo = partes[1] 
            porta = int(partes[2]) 
            comando_dispositivo = partes[3]
            temperatura = int(partes[4])
            
            # Enviar a mensagem para os dispositivos TCP conectados
            for dispositivo in clientes_tcp:
                if comando == "comando_para_dispositivo":
                    if dispositivo["ip"] == ip_dispositivo: 
                        message = f"comando-{comando_dispositivo}-{temperatura}"
                        dispositivo["socket"].send(message.encode()) 
                        msg = Recebimento_mensagem(dispositivo["socket"]) 

def Recebimento_mensagem(socket): 
    try: 
        global msg 
        msg = socket.recv(1024).decode('utf-8') 
        return msg
    except Exception as e: 
        print(f"Erro ao processar mensagem TCP: {e}")
        time.sleep(3)

    
# Função para armazenar as mensagens recebidas via HTTP
@app.route("/send-message/", methods=["POST"])
def send_message():
    try:
        data = request.json
        message = data.get("message")
        if message is None:
            return jsonify({"success": False, "message": "Mensagem não recebida"}), 400
        primeira_parte = message.split("-")
        # Coloca a mensagem na fila de mensagens HTTP
        http_messages.put(primeira_parte)
        

        tipo_comando_http = primeira_parte[0]
        ip_dispositivo = primeira_parte[1]
        porta = int(primeira_parte[2])
        comando_dispositivo = primeira_parte[3]
        

        if tipo_comando_http == "comando_para_dispositivo":
            if comando_dispositivo != "ligar" and comando_dispositivo!= "desligar" and comando_dispositivo!= "temperatura":
                return jsonify({"success": False, "message": "Erro ao enviar"}), 400
            else:
                return jsonify({"success": True, "message": "Mensagem enviada com sucesso"}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Função para obter a lista de dispositivos TCP
@app.route("/tcp-clients/", methods=["GET"])
def get_tcp_clients():
    try:
        # Criar uma lista de dicionários com informações dos dispositivos TCP
        devices_info = []
        for device in clientes_tcp:
            device_info = {
                "ip": device["ip"],
                "porta_tcp": device["porta_tcp"],
                "estado": device["estado"],
                "temperatura": device["temperatura"] 
            }
            devices_info.append(device_info)
        
        return jsonify({"success": True, "devices": devices_info}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def start_api():
    app.run(host = IP, port=5005, debug=False, use_reloader=False)

def main():

    try:
        
        # Configuração do socket TCP
        tcp_socket.bind((IP, SERVER_TCP_PORT))
        tcp_socket.listen(5)
        print("Servidor TCP aguardando conexões...")

        # Configuração do socket UDP
        udp_socket.bind((IP, SERVER_UDP_PORT))
        print("Servidor UDP aguardando mensagens...")
        
        #Inicia uma thread para armazenar as mensagens Udp em uma Fila
        udp_thread = threading.Thread(target=handle_udp_connection, args=(udp_socket,))
        udp_thread.start()

        # Inicia uma thread para processar as mensagens UDP
        process_udp_thread = threading.Thread(target=process_udp_messages)
        process_udp_thread.start() 

        # Inicia uma thread para processar as mensagens HTTP
        http_thread = threading.Thread(target=process_http_messages)
        http_thread.start()
        
        verifição_conexão_thread = threading.Thread(target=verificar_conexao_dispositivos, daemon=True)
        verifição_conexão_thread.start()
        
        while True: 
            client_socket, address = tcp_socket.accept() 
            tcp_thread = threading.Thread(target=Registrar_dipositivo_TCP, args=(client_socket, address))
            tcp_thread.start()  

    except KeyboardInterrupt:
        print("Encerrando servidor...")
        udp_socket.close()
        tcp_socket.close()
        print("Servidor encerrado.")


if __name__ == "__main__":
    thread_api = threading.Thread(target=start_api, daemon=True)
    thread_api.start()
    main()
   