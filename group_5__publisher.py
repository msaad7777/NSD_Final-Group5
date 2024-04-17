import paho.mqtt.client as mqtt
import json
import time
import tkinter as tk
from tkinter import messagebox
import group_5_util

PORT = 1883

class PublisherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Publisher")

        # Connect and Disconnect Buttons
        self.connect_button = tk.Button(master, text="Connect", command=self.connect_to_broker)
        self.connect_button.grid(row=0, column=0, padx=5, pady=5)

        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_from_broker)
        self.disconnect_button.grid(row=0, column=1, padx=5, pady=5)
        self.disconnect_button.config(state="disabled")  # Initially disabled

        # Min Value, Max Value, Daily Mean, Readings Per Day Labels and Textboxes
        self.min_label = tk.Label(master, text="Min Value:")
        self.min_label.grid(row=1, column=0, sticky="e", padx=5)
        self.min_entry = tk.Entry(master)
        self.min_entry.grid(row=1, column=1, padx=5)

        # Add other GUI elements for max value, daily mean, readings per day

        # Update Button
        self.update_button = tk.Button(master, text="Update", command=self.update_settings)
        self.update_button.grid(row=5, columnspan=2, pady=5)

        # Start Publishing and Stop Publishing Buttons
        self.start_publishing_button = tk.Button(master, text="Start Publishing", command=self.start_publishing)
        self.start_publishing_button.grid(row=6, column=0, padx=5, pady=5)

        self.stop_publishing_button = tk.Button(master, text="Stop Publishing", command=self.stop_publishing)
        self.stop_publishing_button.grid(row=6, column=1, padx=5, pady=5)
        self.stop_publishing_button.config(state="disabled")  # Initially disabled

        # Topic Label and Textbox
        self.topic_label = tk.Label(master, text="Topic:")
        self.topic_label.grid(row=7, column=0, padx=5, pady=5)
        self.topic_entry = tk.Entry(master, state="disabled", disabledbackground="lightgray")
        self.topic_entry.grid(row=7, column=1, padx=5, pady=5)
        self.topic_entry.insert(0, "Humidity Over Time")

        # MQTT client
        self.client = mqtt.Client('pub')
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            messagebox.showinfo("Success", "Connected to broker!")
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")
            self.start_publishing_button.config(state="normal")
        else:
            messagebox.showerror("Error", "Failed to connect to broker!")

    def on_disconnect(self, client, userdata, rc):
        messagebox.showinfo("Info", "Disconnected from broker!")
        self.connect_button.config(state="normal")
        self.disconnect_button.config(state="disabled")
        self.start_publishing_button.config(state="disabled")
        self.stop_publishing()

    def connect_to_broker(self):
        self.client.connect('localhost', PORT)
        self.client.loop_start()

    def disconnect_from_broker(self):
        self.client.disconnect()

    def update_settings(self):
        # Update settings based on GUI inputs
        pass

    def start_publishing(self):
        self.client.loop_start()
        self.publish_data()
        self.start_publishing_button.config(state="disabled")
        self.stop_publishing_button.config(state="normal")

    def stop_publishing(self):
        self.client.loop_stop()
        self.start_publishing_button.config(state="normal")
        self.stop_publishing_button.config(state="disabled")

    def publish_data(self):
        try:
            topic = self.topic_entry.get()
            if not topic:
                raise ValueError("Topic cannot be empty")

            data = group_5_util.create_data()
            string = json.dumps(data)
            self.client.publish(topic, string)
            print(f"Published: {string}")

            messagebox.showinfo("Success", "Data published successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    gui = PublisherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
