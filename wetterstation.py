import socketserver
import json
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
import os
import paho.mqtt.client as mqtt


MQTT_SERVER = "10.0.0.10"
MQTT_PORT = 1883
MQTT_TOPIC = "weatherstation/sensors"
MQTT_USER = "mqtt_user"
MQTT_PASSWORD = "mqtt_passwd"


parameter = [
    "ID",
    "PASSWORD",
    "indoortempf",
    "tempf",
    "dewptf",
    "windchillf",
    "indoorhumidity",
    "humidity",
    "windspeedmph",
    "windgustmph",
    "winddir",
    "absbaromin",
    "baromin",
    "rainin",
    "dailyrainin",
    "weeklyrainin",
    "monthlyrainin",
    "solarradiation",
    "UV",
    "dateutc",
    "softwaretype",
    "action",
    "realtime",
    "rtfreq",
]

WINDDIRS=['N', 'NNO', 'NO', 'ONO', 'O', 'OSO', 'SO', 'SSO', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']

querys = []
sensor_dict = {}
sensor_dict_mqtt = {}

def prepare_data_to_mqtt():

    

    sensor_dict_mqtt["UV"] = int(sensor_dict["UV"])
    sensor_dict_mqtt["absbaromin"] = float(sensor_dict["absbaromin"])
    sensor_dict_mqtt["baromin"] = float(sensor_dict["baromin"])
    sensor_dict_mqtt["dailyrainin"] = round(float(sensor_dict["dailyrainin"]) * 254/10, 2)
    sensor_dict_mqtt["rainin"] =  round(float(sensor_dict["rainin"]) * 254/10, 2)
    sensor_dict_mqtt["dewptf"] = round((float(sensor_dict["dewptf"]) -32)*5/9, 2)
    sensor_dict_mqtt["humidity"] = int(sensor_dict["humidity"])
    sensor_dict_mqtt["indoorhumidity"] = int(sensor_dict["indoorhumidity"])
    sensor_dict_mqtt["indoortemp"] = round((float(sensor_dict["indoortempf"]) -32)*5/9, 2)
    sensor_dict_mqtt["monthlyrainin"] = round(float(sensor_dict["monthlyrainin"]) * 254/10, 2)
    sensor_dict_mqtt["solarradiation"] = float(sensor_dict["solarradiation"])
    sensor_dict_mqtt["temp"] = round((float(sensor_dict["tempf"])  -32)*5/9, 2)
    sensor_dict_mqtt["weeklyrainin"] = round(float(sensor_dict["weeklyrainin"]) * 254/10, 2)
    sensor_dict_mqtt["windchillC"] = round((float(sensor_dict["windchillf"]) -32)*5/9, 2)
    sensor_dict_mqtt["winddir"] = int(sensor_dict["winddir"])
    sensor_dict_mqtt["windguskmh"] = round(float(sensor_dict["windgustmph"]) * 16094/10000, 2)
    sensor_dict_mqtt["windspeedkmh"] = round(float(sensor_dict["windspeedmph"]) * 16094/10000, 2)
    sensor_dict_mqtt["dateutc"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sensor_dict_mqtt["softwaretype"] = sensor_dict["softwaretype"]
    sensor_dict_mqtt["rtfreq"] = int(sensor_dict["rtfreq"])
    sensor_dict_mqtt["realtime"] = int(sensor_dict["realtime"])
    sensor_dict_mqtt["action"] = sensor_dict["action"]
    sensor_dict_mqtt["ID"] = sensor_dict["ID"]
    sensor_dict_mqtt["PASSWORD"] = sensor_dict["PASSWORD"]
    sensor_dict_mqtt["Windrichtung"] = WINDDIRS[ int(round((int(sensor_dict["winddir"])  / 22.5) , 0 )) ]


    client = mqtt.Client()
    

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    
    print(sensor_dict_mqtt)
    for name, val in sensor_dict_mqtt.items():
        print(MQTT_TOPIC +"/" + name, val)
        client.publish(MQTT_TOPIC +"/" + name , payload=val , qos=0, retain=False)
        time.sleep(0.1)
   







def create_json(parameter, querys):
    for i in range(len(parameter)):
        sensor_dict[parameter[i]] = querys[i]
    
    


def pares_data(url):
    url = url.replace("GET /", "https://weatherstation.wunderground.com/")
    url = url.replace(" HTTP/1.1", "")

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    querys.clear()

    for i in range(len(parameter)):
        querys.append(params[parameter[i]][0])

    querys[len(parameter) - 1] = "5"

    return querys



class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} write:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

        message = self.data.decode("utf-8")
        pares_data(message)
        create_json(parameter, querys)
  
        prepare_data_to_mqtt()


aServer = socketserver.TCPServer(("", 8077), MyTCPHandler)
aServer.serve_forever()
