import tkinter as tk
from tkinter import simpledialog
import threading
import time
import random
import paho.mqtt.client as mqtt

class DataPublisher:
    def __init__(self, broker, port, topic, interval=5, base_value=100.0, fluctuation=10.0):
        # MQTT Setup
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        
        # Publishing parameters
        self.topic = topic
        self.interval = interval
        self.base_value = base_value
        self.fluctuation = fluctuation
        
        self.publishing = False
        self.thread = None

    def start_publishing(self):
        self.publishing = True
        self.thread = threading.Thread(target=self.publish_data)
        self.thread.start()

    def stop_publishing(self):
        self.publishing = False
        self.thread.join()

    def publish_data(self):
        while self.publishing:
            fluctuated_value = self.base_value + (random.random() * 2 * self.fluctuation - self.fluctuation)
            self.client.publish(self.topic, fluctuated_value)
            time.sleep(self.interval)

    def disconnect(self):
        self.client.disconnect()

def create_publisher():
    broker = "test.mosquitto.org"
    port = 1883
    topic = simpledialog.askstring("Settings", "Enter MQTT topic:")
    interval = simpledialog.askinteger("Settings", "Enter interval (s):", minvalue=1, maxvalue=60)
    base_value = simpledialog.askfloat("Settings", "Enter base value:")
    fluctuation = simpledialog.askfloat("Settings", "Enter fluctuation range:")

    publisher = DataPublisher(broker, port, topic, interval, base_value, fluctuation)
    publishers.append(publisher)
    publisher.start_publishing()
    update_status()

def stop_all_publishers():
    for pub in publishers:
        pub.stop_publishing()
        pub.disconnect()
    publishers.clear()
    update_status()

def update_status():
    status = f"Running {len(publishers)} publishers."
    status_label.config(text=status)

root = tk.Tk()
root.title("Multiple MQTT Publishers")

publishers = []

tk.Button(root, text="Create New Publisher", command=create_publisher).pack(pady=10)
tk.Button(root, text="Stop All Publishers", command=stop_all_publishers).pack(pady=10)
status_label = tk.Label(root, text="No publishers running.")
status_label.pack(pady=10)

root.mainloop()