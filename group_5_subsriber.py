import paho.mqtt.client as mqtt
import group_5_util
import json

PORT = 1883
topic ='Humidity Over Time'  # Adjust topic to match the one used by the publisher

def on_message(client, userdata, message):
    try:
        decoded_message = message.payload.decode('utf-8')
        data_dict = json.loads(decoded_message)
        print(f"Received message from {topic}:")
        group_5_util.print_data(data_dict)
    except Exception as e:
        print(f"Error handling message: {e}")

client = mqtt.Client('sub')
client.on_message = on_message

try:
    client.connect('localhost', PORT)
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")
    client.loop_forever()
except KeyboardInterrupt:
    print("Subscriber stopped by user")
    client.disconnect()
except Exception as e:
    print(f"Error: {e}")
