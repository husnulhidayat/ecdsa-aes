import paho.mqtt.client as mqtt
import configparser
import hashlib
import ecdsa
import time
from ecdsa import VerifyingKey, BadSignatureError

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

vk = VerifyingKey.from_pem(open("keypair-generate/NIST256p/public.pem").read())

def on_message( client, userdata, msg):

    msg = msg.payload.split(b' ')
    signature = msg[0]
    message = msg[1]

    if (vk.verify(signature, message, hashfunc=hashlib.sha1, sigdecode=ecdsa.util.sigdecode_der)):
        print(message.decode('utf-8'))
    else:
        BadSignatureError()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(server, port, keepalive)

client.loop_forever()