import json
import psutil
import time

__inited = False

def cpu():
    global __inited
    if not __inited:
        # Call this once first and ignore the output
        # https://psutil.readthedocs.io/en/latest/#cpu
        psutil.cpu_times_percent(interval=None, percpu=False)
        time.sleep(1)
        __inited = True
    d = psutil.cpu_times_percent(interval=None, percpu=False)._asdict()
    d["source"] = "cpu"
    try:
        d["temperature"] = psutil.sensors_temperatures()['cpu-thermal'][0].current
    except Exception as e:
        print("error: cpu-thermal not available: " + str(e))
    return d

def disk():
    d = psutil.disk_usage('/')._asdict()
    d["source"] = "disk"
    return d

def memory():
    d = psutil.virtual_memory()._asdict()
    d["source"] = "memory"
    return d

def print_all_json():
    """Tests the above code"""
    print("cpu: {0}".format(json.dumps(cpu())))
    print("disk: {0}".format(json.dumps(disk())))
    print("memory: {0}".format(json.dumps(memory())))

if __name__ == "__main__":
    print_all_json()