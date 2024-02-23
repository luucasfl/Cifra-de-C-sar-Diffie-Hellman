import random
from socket import *

G = 17
N = 127
X = random.randint(1, 5000)

# Calcula o valor da chave R1
def calcula_r1():
    return (G ** X) % N

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

# Calcula o valor da chave K1
def calcula_k1(r2):
    return (r2 ** X) % N

serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.
print("TCP Server\n")
connectionSocket, addr = serverSocket.accept()

# Recebimento da chave pública do cliente
r2 = int(connectionSocket.recv(1024).decode())

# Envio da chave R1 para o client
r1 = calcula_r1()
connectionSocket.send(str(r1).encode())

# Descriptografia da mensagem
k1 = calcula_k1(r2)
sentence = connectionSocket.recv(1024).decode()
received = decrypt(sentence, k1)
print("Received From Client: ", received)

capitalizedSentence = received.upper()  # processamento

# Criptografia da mensagem e envio usando a chave K1
encrypted_sentence = encrypt(capitalizedSentence, k1)
connectionSocket.send(encrypted_sentence.encode())

sent = encrypted_sentence
print("Sent back to Client: ", sent)
connectionSocket.close()
