import paho.mqtt.client as mqtt
import configparser

config = configparser.RawConfigParser()
config.read('config/publisher.ini')


from ecdsa import SigningKey, VerifyingKey, BadSignatureError
sk = SigningKey.from_pem(open("config/private192.pem").read())
vk = VerifyingKey.from_pem(open("config/public192.pem").read())

messageS = 'sds'
message = messageS.encode('utf-8')

sig = sk.sign(message)

try:
    vk.verify(sig, message)
    print("good signature")
except BadSignatureError:
    print("BAD SIGNATURE")