"# Sainlogic_WS3500_MQTT" 

This Python script includes a TCP server that receives weather data from the Sainlogic WS3500 weather station, processes it, converts it to European values, and makes it available through MQTT.

To receive weather data using this Python script, the settings on the receiving device must be configured to enable Wunderground Customized mode with port 8077. It is also possible to use a different port, but the script must be updated accordingly.

In addition, the Python script must specify the user's own MQTT broker with the correct IP address, username, and password.

The required packages for this script are as follows: socketserver, datetime, urllib.parse, time, and paho.mqtt.client.
