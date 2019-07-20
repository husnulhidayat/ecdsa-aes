import paho.mqtt.client as mqtt
import configparser
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import argparse
import time

#configuration
config = configparser.RawConfigParser()
config.read('config/publisher.ini')
username = config.get('credential','username')
password = config.get('credential','password')
topic = config.get('credential','topic')
server = config.get('host','server')
port = config.getint('host','port')
keepalive = config.getint('host','keep-alive')
qosval = config.getint('credential','qos')
clientid = config.get('credential','client')

parser = argparse.ArgumentParser()
parser.add_argument("-m",help="message")
args = parser.parse_args()
#####

#mqtt-connect
def on_connect( client, userdata, flags, rc):
    return str(rc)
    #client.subscribe(topic)

def on_message( client, userdata, msg):
    print(str(msg.payload))

def on_log(client, userdata, level, buf):
    print("log: ",buf)


client = mqtt.Client(clientid)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(server, port, keepalive)

client.loop_start()
time.sleep(1)
#end of mqtt connect

#signing-and-verify set
sk = SigningKey.from_pem(open("config/private192.pem").read())

def main():
    client.loop_start()
    try:
        messageS = args.m
        message = messageS.encode('utf-8')
        signature = sk.sign(message)

        joinSig = signature+b' '+message

        client.publish(topic, joinSig, qos=qosval)


        time.sleep(1)

    except BadSignatureError:
        print("Error")

    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()