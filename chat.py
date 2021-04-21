from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

HOST = input('Host: ')
PORT = 7777
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# recebe a mensagem
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Cliente saiu da sala.
            break

# envia a mensagem
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Limpa o input da mensagem
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{sair}":
        client_socket.close()
        top.quit()

# Fechar janela
def on_closing(event=None):
    my_msg.set("{sair}")
    send()

top = tkinter.Tk()
top.title("Mensagem Instantânea")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # mensagens enviadas
my_msg.set("Digite aqui sua mensagem.")
scrollbar = tkinter.Scrollbar(messages_frame)  # mostra mensagens na tela

msg_list = tkinter.Listbox(messages_frame, height=25, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Enviar", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # gui