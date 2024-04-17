import paho.mqtt.client as mqtt
import json
import tkinter as tk
from tkinter import messagebox
import group_5_data_generator
import time
import random
import threading

PORT = 1883

class PublisherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Publisher")

        # Initialize MQTT client
        self.client = mqtt.Client('pub')
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        # Data generator
        self.data_generator = group_5_data_generator.PatternedDataGenerator()

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

        self.max_label = tk.Label(master, text="Max Value:")
        self.max_label.grid(row=2, column=0, sticky="e", padx=5)
        self.max_entry = tk.Entry(master)
        self.max_entry.grid(row=2, column=1, padx=5)

        self.mean_label = tk.Label(master, text="Daily Mean:")
        self.mean_label.grid(row=3, column=0, sticky="e", padx=5)
        self.mean_entry = tk.Entry(master)
        self.mean_entry.grid(row=3, column=1, padx=5)

        self.readings_label = tk.Label(master, text="Readings Per Day:")
        self.readings_label.grid(row=4, column=0, sticky="e", padx=5)
        self.readings_entry = tk.Entry(master)
        self.readings_entry.grid(row=4, column=1, padx=5)

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
        self.topic_entry = tk.Entry(master)  # Remove state="disabled"
        self.topic_entry.grid(row=7, column=1, padx=5, pady=5)
        self.topic_entry.insert(0, "Humidity Over Time")

        # Corrupt Data Checkbox
        self.corrupt_data_var = tk.BooleanVar()
        self.corrupt_data_checkbox = tk.Checkbutton(master, text="Corrupt Data", variable=self.corrupt_data_var)
        self.corrupt_data_checkbox.grid(row=8, columnspan=2)

        # Miss Transmission Rate Label and Entry
        self.miss_rate_label = tk.Label(master, text="Miss Transmission Rate (%)")
        self.miss_rate_label.grid(row=9, column=0, sticky="e", padx=5)
        self.miss_rate_entry = tk.Entry(master)
        self.miss_rate_entry.grid(row=9, column=1, padx=5)

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
        try:
            min_value = float(self.min_entry.get())
            max_value = float(self.max_entry.get())
            daily_mean = float(self.mean_entry.get())
            readings_per_day = int(self.readings_entry.get())

            # Apply user's input to publisher's behavior
            self.data_generator.set_parameters(min_value, max_value, daily_mean, readings_per_day)
            pass
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def start_publishing(self):
        self.client.loop_start()
        # Start publishing data in a separate thread
        self.publishing = True  # Set flag to indicate publishing
        self.publish_thread = threading.Thread(target=self.publish_data_thread)
        self.publish_thread.daemon = True
        self.publish_thread.start()
        self.start_publishing_button.config(state="disabled")
        self.stop_publishing_button.config(state="normal")
    def stop_publishing(self):
        self.publishing = False
        self.start_publishing_button.config(state="normal")
        self.stop_publishing_button.config(state="disabled")

    def publish_data_thread(self):
        try:
            topic = self.topic_entry.get()
            if not topic:
                raise ValueError("Topic cannot be empty")

            while self.publishing:  # Check flag to continue publishing
                data_value = self.data_generator.generate_value()
                timestamp = time.time()
                packet_id = random.randint(1, 1000000)
                data_packet = {
                    "timestamp": timestamp,
                    "packet_id": packet_id,
                    "data_value": data_value
                }
                if self.corrupt_data_var.get():
                    # Corrupt data randomly
                    if random.randint(1, 100) <= int(self.miss_rate_entry.get()):
                        # Skip transmission
                        continue
                    if random.randint(1, 100) <= int(self.miss_rate_entry.get()):
                        # Introduce wild data
                        data_packet["data_value"] *= random.uniform(1.5, 2.0)
                string = json.dumps(data_packet)
                self.client.publish(topic, string)
                print(f"Published: {string}")
                time.sleep(1)  # Adjust sleep time as needed

            # messagebox.showinfo("Success", "Data published successfully!")  # Avoid using messagebox in a thread
        except Exception as e:
            messagebox.showerror("Error", str(e))
def main():
    root = tk.Tk()
    gui = PublisherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
