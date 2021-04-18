import socket
from threading import Thread

clients = {}
addresses = {}

HOST = ''
PORT = 7777
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)



def recebe_conexao():
    # Trata das conexoes para o cliente
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s conectou." % client_address)
        client.send(bytes("Olá!"+"Digite seu nome e aperte ENTER!", "utf8"))
        addresses[client] = client_address
        Thread(target=gerencia_client, args=(client,)).start()

def gerencia_client(client):  # client = socket do cliente
    # Trata uma unica conexao
    nome = client.recv(BUFSIZ).decode("utf8")
    bemvindo = 'Bem-vindo %s! Quando quiser sair digite {sair}.' % nome
    client.send(bytes(bemvindo, "utf8"))
    msg = "%s entrou na sala!" % nome
    broadcast(bytes(msg, "utf8"))
    clients[client] = nome
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{sair}", "utf8"):
            broadcast(msg, nome+": ")
        else:
            client.send(bytes("{sair}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s saiu da sala." % nome, "utf8"))
            break

def broadcast(msg, nome=""):
    # Envia msg para o cliente
    for sock in clients:
        sock.send(bytes(nome, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5)  # Escuta até 5 conexões
    print("Aguardando conexao...")
    ACCEPT_THREAD = Thread(target=recebe_conexao)
    ACCEPT_THREAD.start()  # Inicia o laço
    ACCEPT_THREAD.join()
    SERVER.close()