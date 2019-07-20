import paho.mqtt.client as mqtt
import configparser
from Crypto.Cipher import AES
import pyscrypt
import ecdsa
from ecdsa import VerifyingKey, BadSignatureError
import hashlib

config = configparser.RawConfigParser()
config.read('config/subscriber.ini')
username = config.get('credential','username')
password = config.get('credential','password')
topic = config.get('credential','topic')
server = config.get('host','server')
port = config.getint('host','port')
keepalive = config.getint('host','keep-alive')
clientid = config.get('credential', 'client')

def on_connect( client, userdata, flags, rc):
    client.subscribe(topic)

password = b"HusnulGantengBangetttttt"
salt = b"asinIh"

N = 1024
r = 1
p = 1

key = pyscrypt.hash(password,salt, N,r,p, 16)
secret = b's\xa4\xc9\xc6\xa1\x0f\x93\xc05\x0b?\x81\x0e\xe2\x0e '
aes = AES.new(key, AES.MODE_CTR, counter=lambda: secret)
vk = VerifyingKey.from_pem(open("keypair-generate/NIST256p/public.pem").read())

def on_message( client, userdata, msg):

    #msg = msg.payload.split(b' ')
    msg = msg.payload
    decrypt = aes.decrypt(msg)
    ciphertext = decrypt.split(b' ')
    signature = ciphertext[0]
    message = ciphertext[1]
    if (vk.verify(signature, message, hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der)):
        mout.append(message.decode('utf-8'))
    else:
        BadSignatureError()

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.connect(server, port, keepalive)
client.on_connect = on_connect
client.on_message = on_message

mout = []
client.loop_start()
while True:
    if len(mout) > 0:
        secret = b's\xa4\xc9\xc6\xa1\x0f\x93\xc05\x0b?\x81\x0e\xe2\x0e '
        aes = AES.new(key, AES.MODE_CTR, counter=lambda: secret)
        print(mout.pop())
client.loop_stop()
