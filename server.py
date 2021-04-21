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
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s conectou." % client_address)
        client.send(bytes("Olá!"+"Digite seu nome e aperte ENTER!", "utf8"))
        addresses[client] = client_address
        Thread(target=gerencia_client, args=(client,)).start()

# gerencia uma conexao do cliente
def gerencia_client(client): # socket como parametro
    nome = client.recv(BUFSIZ).decode("utf8")
    msgini = 'Bem-vindo %s! Quando quiser sair digite {sair}.' % nome
    client.send(bytes(msgini, "utf8"))
    msg = "%s entrou na sala!" % nome
    envia_msg(bytes(msg, "utf8"))
    clients[client] = nome
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{sair}", "utf8"):
            envia_msg(msg, nome+": ")
        else:
            client.send(bytes("{sair}", "utf8"))
            client.close()
            del clients[client]
            envia_msg(bytes("%s saiu da sala." % nome, "utf8"))
            break

# envia a mensagem para o cliente
def envia_msg(msg, nome=""):
    for sock in clients:
        sock.send(bytes(nome, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5)  # até cinco conexões
    print("Aguardando conexao...")
    ACCEPT_THREAD = Thread(target=recebe_conexao)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()