import argparse
import json
import os
import paho.mqtt.client as paho
import time

import diag
import sht31

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server, flags: "+str(flags)+" result code "+str(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected with rtn code {0}".format(rc))

def on_publish(client, userdata, mid):
    print("Message id {0} published".format(mid))

parser = argparse.ArgumentParser()
sensor = sht31.Sensor(address = 0x44)

parser.add_argument("-s", "--server", help="MQTT server to connect to", default=os.environ["MQTT_SERVER"])
parser.add_argument("-p", "--port", type=int, help="Port number to connect to", default=1883)
parser.add_argument("-t", "--topic", help="Topic prefix", default="/skycam")
parser.add_argument("-i", "--interval", help="Publish time interval in seconds", default=60)
parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
args = parser.parse_args()

topic_prefix = args.topic
print("Topic prefix: " + topic_prefix)

client = paho.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

if args.verbose:
    client.on_publish = on_publish

client.connect(args.server, args.port)
client.loop_start()

while True:
    (temperature, humidity) = sensor.read_temperature_humidity()
    sht31 = {
        "source": "sht31",
        "temperature": temperature,
        "humidity": humidity
    }

    # Publish topics with all data as JSON
    (rc, mid) = client.publish(topic_prefix + "/sysmon/sht31", json.dumps(sht31), qos=1)
    (rc, mid) = client.publish(topic_prefix + "/sysmon/cpu", json.dumps(diag.cpu()), qos=1)
    (rc, mid) = client.publish(topic_prefix + "/sysmon/disk", json.dumps(diag.disk()), qos=1)
    (rc, mid) = client.publish(topic_prefix + "/sysmon/memory", json.dumps(diag.memory()), qos=1)

    time.sleep(args.interval)