# Publish Sensirion SHT31 sensor and psutil data to a MQTT server

## Building

```sh
$ docker build -t sysmon .
```

## Running

```sh
$ docker run -d --name sysmonpublisher --restart=unless-stopped --device /dev/i2c-1 sysmon -s host.example.com -t mytopic/mysubtopic
```

This runs pub.py which publishes measurements to host.example.com.
Default port is 1883.
Default topic prefix is "/skycam".

## Example published data

```
asgaut@vps1:~$ mosquitto_sub -h host.example.com -t "/skycam/#" -v
/skycam/sysmon/sht31 {"source": "sht31", "temperature": 35.502403295948724, "humidity": 30.826276035706112}
/skycam/sysmon/cpu {"user": 4.9, "nice": 0.0, "system": 1.7, "idle": 93.3, "iowait": 0.0, "irq": 0.0, "softirq": 0.1, "steal": 0.0, "guest": 0.0, "guest_nice": 0.0, "source": "cpu", "temperature": 57.996}
/skycam/sysmon/disk {"total": 61786140672, "used": 2573451264, "free": 56032083968, "percent": 4.4, "source": "disk"}
/skycam/sysmon/memory {"total": 781795328, "available": 422313984, "percent": 46.0, "used": 437141504, "free": 52350976, "active": 249565184, "inactive": 328560640, "buffers": 19116032, "cached": 273186816, "shared": 6283264, "slab": 87916544, "source": "memory"}
```