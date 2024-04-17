import json
from tkinter import *
from tkinter import messagebox
from data_generator import PatternedDataGenerator

class DisplayStaticDataSeries:
    def __init__(self, base_min=18, base_max=21, fluctuation=3):
        self.generator = PatternedDataGenerator(base_min, base_max, fluctuation)
        self.values = [self.generator.generate_data_packet() for _ in range(20)]
        self.init_ui()

    def init_ui(self):
        self.root = Tk()
        self.root.title("Historical Data")
        self.root.geometry("600x400")

        self.canvas = Canvas(self.root, width=600, height=300)
        self.canvas.pack()

        self.label = Label(self.root, text="Enter New Value:")
        self.label.place(x=20, y=320)

        self.entry = Entry(self.root)
        self.entry.place(x=130, y=320, width=100)

        self.button = Button(self.root, text="Update Chart", bg="lightgrey", command=self.update_chart)
        self.button.place(x=250, y=315)

        self.draw_chart()

    def draw_chart(self):
        self.canvas.delete("all")
        rect_width = 25
        rect_gap = 20
        x_start = 50
        x = x_start
        prev_x = prev_y = None

        for packet in self.values:
            value = json.loads(packet)['data_value']  # Decode JSON to get value
            rect_height = (value - self.generator.base_min) / (self.generator.base_max - self.generator.base_min) * 250
            self.canvas.create_rectangle(x, 250 - rect_height, x + rect_width, 250, fill="lightgreen")
            if prev_x is not None:
                self.canvas.create_line(prev_x, prev_y, x + rect_width // 2, 250 - rect_height, fill="red")
            prev_x, prev_y = x + rect_width // 2, 250 - rect_height
            x += rect_width + rect_gap

    def update_chart(self):
        try:
            new_value = float(self.entry.get())
            assert self.generator.base_min <= new_value <= self.generator.base_max
        except (ValueError, AssertionError):
            messagebox.showinfo("Error", "Invalid Input: Enter a number within the range.")
            return
        new_packet = self.generator.generate_data_packet()  # Generate new packet
        self.values.pop(0)
        self.values.append(new_packet)
        self.draw_chart()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    data_series = DisplayStaticDataSeries()
    data_series.run()