import random
import json
import time
from datetime import datetime

class PatternedDataGenerator:
    def __init__(self, base_min=18, base_max=21, fluctuation=3):
        self.base_min = base_min
        self.base_max = base_max
        self.fluctuation = fluctuation
        self.packet_id = 0  # Initialize packet ID
    def set_parameters(self, base_min, base_max, fluctuation):
        """Set the parameters for data generation."""
        self.base_min = base_min
        self.base_max = base_max
        self.fluctuation = fluctuation
    def generate_value(self):
        """Generate a random value following a specified pattern."""
        base_value = random.uniform(self.base_min, self.base_max)
        fluctuation = (random.random() * 2 - 1) * self.fluctuation
        value = base_value + fluctuation
        return value

    def generate_data_packet(self):
        """Generate a data packet with a timestamp and packet ID."""
        data_value = self.generate_value()
        timestamp = datetime.now().isoformat()
        self.packet_id += 1  # Increment packet ID for each new packet
        data_packet = {
            "timestamp": timestamp,
            "packet_id": self.packet_id,
            "data_value": data_value
        }
        return json.dumps(data_packet)  # Convert the packet to JSON string format