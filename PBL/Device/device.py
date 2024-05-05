import socket
import threading
import time
import os
import socket

# Constantes utilizadas para a conexão com o servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT_UDP = 8889
SERVER_PORT_TCP = 9999



#incialização do socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Estado inicial do ar-condicionado
Ar_condicionado = { 
    "estado": "desligado",
    "temperatura": 0
}

# Funções para controlar o ar-condicionado

def modificar_temperatura(nova_temperatura):
    Ar_condicionado["temperatura"] = nova_temperatura
    print("Temperatura modificada para", nova_temperatura, "°C.")


def envio_informações():
    def enviar(): 
        while True:
            estado = ["estado"]
            temperatura = Ar_condicionado["temperatura"]
            mensagem = f"status-{estado}-{temperatura}"
            envio_mensagem_udp(mensagem, SERVER_IP, SERVER_PORT_UDP)
            time.sleep(2)  
    thread = threading.Thread(target=enviar)
    thread.start() 

def envio_mensagem_udp(mensagem, server_ip, server_port_udp): 
    try: 
        #Tenta enviar mensagem ao servidor via UDP
        udp_socket.sendto(mensagem.encode(), (server_ip, server_port_udp)) 
    except socket.error as e:
        print(f"Falha ao enviar mensagem via UDP: {e}") 

def tente_conectar_broker_tcp(server_ip, server_port_tcp): 
    while True:
        try: 
            #Tenta conectar ao servidor 
            global tcp_socket
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((server_ip, server_port_tcp)) 
            print("Sucesso ao conectar") 
            break
        except socket.error as e:
            if hasattr(e, 'winerror') and e.winerror == 10061:
                print("O Servidor ainda não está no ar")
                time.sleep(3)
                print("Tentando Reconexão...")
            else:
                print(f"Falha ao conectar ao servidor via TCP: {e}")  

# Função para tratar mensagens recebidas via TCP
def tratando_mensagens_tcp(): 
    while True:
        try:
            mensagem = tcp_socket.recv(1024).decode('utf-8')
            if not mensagem:
                break
            print(f"Mensagem TCP recebida: {mensagem}")
            #Particiona as mensagens recebidas
            partes = mensagem.split('-')
            receptor_mensagens(partes)
        except ConnectionResetError:
            print("A conexão com o servidor foi redefinida pelo servidor. Aguarde o servidor estar no ar novamente") 
            tente_conectar_broker_tcp(SERVER_IP, SERVER_PORT_TCP)
        except Exception as e:
            print(f"Erro ao processar mensagem TCP: {e}")
            time.sleep(3)


def receptor_mensagens(partes):
    tipo_mensagem = partes[0]

    if tipo_mensagem == 'comando':
        comando = partes[1]

        if comando == 'ligar':
            if Ar_condicionado['estado'] == "desligado":
                Ar_condicionado['estado'] = "ligado"
                tcp_socket.send(bytes(f"comando_recebido-ligar-ligado-{Ar_condicionado['estado']}","utf-8"))
        elif comando == 'desligar':
            if Ar_condicionado['estado'] == "ligado":
                Ar_condicionado['estado'] = "desligado"
                tcp_socket.send(bytes(f"comando_recebido-desligar-desligado-{Ar_condicionado['estado']}","utf-8"))
        elif comando == 'temperatura':
            
            if partes[2]:
                nova_temperatura = partes[2]
                try:
                    nova_temperatura = int(nova_temperatura)
                    print(nova_temperatura)
                    Ar_condicionado['temperatura'] = nova_temperatura
                    print(f"Temperatura modificada para {Ar_condicionado['temperatura']}°C.")
                    tcp_socket.send(bytes(f"comando_recebido-temperatura-{Ar_condicionado['temperatura']}","utf-8"))
                except ValueError:
                    print("Comando de temperatura inválido.")
        elif comando == '4':
            exit()
        else:
            print("Comando inválido")
             
def receptor_mensagens_menu(mensagem): 
    if mensagem == '1':
        if Ar_condicionado['estado'] == "desligado": 
            Ar_condicionado['estado'] = "ligado"
    elif mensagem == '2':
        if Ar_condicionado['estado'] == 'ligado': 
            Ar_condicionado['estado'] = "desligado"
    elif mensagem == '3':
        nova_temperatura = input("Digite a nova temperatura: ")
        try:
            nova_temperatura = int(nova_temperatura)
            Ar_condicionado['temperatura'] = nova_temperatura
        except ValueError:
            print("Comando de temperatura inválido.")
    elif mensagem == '4':
        exit()


#Função que envia informações do dispositivo para o broker a cada dois segundos
def envio_informações():
    def enviar(): 
        while True:
            try:
                estado = Ar_condicionado["estado"]
                temperatura = Ar_condicionado["temperatura"]
                
                mensagem = f"status-{estado}-{temperatura}"
                envio_mensagem_udp(mensagem, SERVER_IP, SERVER_PORT_UDP)
                time.sleep(2)  
            except Exception as e:
                print(f"Erro ao enviar mensagem UDP: {e}") 
            
    thread = threading.Thread(target=enviar)
    thread.daemon = True
    thread.start() 


def exibir_menu():
    while True:

        print("\nMenu de Controle do Ar Condicionado")
        print("[1] - Ligar Ar Condicionado")
        print("[2] - Desligar Ar Condicionado")
        print("[3] - Modificar Temperatura")
        print("[4] - Sair\n")
        escolha = input("Escolha uma opção: ")
        receptor_mensagens_menu(escolha)



def main():
    try:
        # Inicia o servidor TCP em uma thread separada
        
        tente_conectar_broker_tcp(SERVER_IP, SERVER_PORT_TCP)

        receive_thread = threading.Thread(target=tratando_mensagens_tcp)
        receive_thread.start()
        

        #Cria uma thread que fica enviando os dados formatados via UDP para o broker
        envio_informações()

        while True:
            try:
                exibir_menu()
            except Exception as e:
                print(f"Erro ao exibir menu: {e}")
                tcp_socket.close()
                udp_socket.close()
                break
    except Exception as e:  
        print(f"Erro ao processar mensagem TCP: {e}")
         

if __name__ == "__main__":
    main()

    