import random
from socket import *

G = 17
N = 127
Y = random.randint(1, 5000)

# Calcula o valor da chave R2S
def calcula_r2():
    return (G ** Y) % N

# Função para criptografar usando a Cifra de César
def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            encrypted_char = (ord(char) + key - 97) % 26 + 97 if char.islower() else (ord(char) + key - 65) % 26 + 65
            encrypted_text += chr(encrypted_char)
        else:
            encrypted_text += char
    return encrypted_text

# Função para decriptografar usando a Cifra de César
def decrypt(text, key):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            decrypted_char = (ord(char) - key - 97) % 26 + 97 if char.islower() else (ord(char) - key - 65) % 26 + 65
            decrypted_text += chr(decrypted_char)
        else:
            decrypted_text += char
    return decrypted_text

# Calcula a chave K2
def calcula_k2(r1):
    return (r1 ** Y) % N

serverName = "192.168.56.1"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


# Envio da chave R2 do cliente para o servidor
r2 = calcula_r2()
clientSocket.send(str(r2).encode())

# Recebimento da chave R1 do servidor
r1 = int(clientSocket.recv(1024).decode())

# Criptografia e envio da mensagem usando a chave K2
k2 = calcula_k2(r1)
sentence = input("Input lowercase sentence: ")
encrypted_sentence = encrypt(sentence, k2)
clientSocket.send(encrypted_sentence.encode())

modifiedSentence = clientSocket.recv(1024)
text = decrypt(modifiedSentence.decode(), k2)
print("Received from Make Upper Case Server: ", text)
clientSocket.close()
