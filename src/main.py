import json
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Custom colors for categories
activeColor = 'red'
inactiveColor = 'blue'
disabledColor = 'yellow'

# COM 1-N or NONE for custom input test data
com_port = 'COM1'

           # first #num-sensors = sensor values, next #num-sensors = thresholds
           #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40
test_data = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# Load sensor coordinates and labels from a JSON file
def load_coordinates_from_file():
    coordinates = []
    try:
        with open('src/coordinates.json', 'r') as file:
            data = json.load(file)
            for item in data:
                label = item["label"]
                coord = item["coordinates"]
                coordinates.append((label, tuple(coord)))
        return coordinates
    except Exception as e:
        print(f"Error loading coordinates: {e}")
        return []

coordinates = load_coordinates_from_file()
NUM_SENSORS = len(coordinates)


def start_graph(selected_port):
    ser = None
    test_mode = False
    
    try:
        ser = serial.Serial(selected_port, 115200, timeout=1)
    except Exception as e:
        print(f"Could not open {selected_port}: {e}")
        print("Using test data mode.")
        test_mode = True

    # Create separate figures for graph and table
    fig_graph, ax_graph = plt.subplots(figsize=(8, 8))
    fig_table, ax_table = plt.subplots(figsize=(7, 8))

    # Scatter plot for sensors
    scatter = ax_graph.scatter(
        [coord[0] for _, coord in coordinates],
        [coord[1] for _, coord in coordinates],
        s=100
    )

    # Create a label for each sensor based on the coordinates
    # You can customize the label position and other elements as needed
    for label, (x, y) in coordinates:
        ax_graph.text(x, y + 0.3, str(label), ha='center', fontsize=8)

    ax_graph.set_title(
        f"Sensor Visualisation\n"
        f"activeColor = {activeColor} | "
        f"inactiveColor = {inactiveColor} | "
        f"disabledColor = {disabledColor}"
    )
    ax_graph.grid(True)
    ax_graph.set_aspect('equal')

    # Table setup
    column_labels = ["Sensor", "Value", "Threshold", "Status"]
    table_data = [["-" for _ in column_labels] for _ in range(NUM_SENSORS)]
    table = ax_table.table(
        cellText=table_data,
        colLabels=column_labels,
        loc='center',
        cellLoc='center'
    )
    ax_table.axis('off')

    def update(frame):
        try:
            if test_mode:

                values = test_data
            else:
                ser.write(b'R')
                data = ser.readline().decode('utf-8').strip()
                if data:
                    values = list(map(int, data.split(',')))
                else:
                    # If no data, disable values
                    values = [-1] * NUM_SENSORS * 2
            if len(values) != NUM_SENSORS * 2:
                print("Invalid data length, amount of values read over serial: ", values)
                print("Expected length from coordinates.json + thresholds: ", NUM_SENSORS * 2)
                return scatter,

            sensors = values[:NUM_SENSORS]
            thresholds = values[NUM_SENSORS:NUM_SENSORS*2]
            colors = []
            table_vals = []

            for i in range(NUM_SENSORS):
                sensor = sensors[i]
                threshold = thresholds[i]
                label = coordinates[i][0]

                if threshold == -1:
                    status = "Disabled"
                    color = disabledColor
                elif sensor > threshold:
                    status = "Active"
                    color = activeColor
                else:
                    status = "Inactive"
                    color = inactiveColor

                colors.append(color)
                table_vals.append([label, sensor, threshold, status])

            scatter.set_color(colors)

            # Update table content and cell background color
            for row in range(NUM_SENSORS):
                for col in range(4):
                    cell = table[row + 1, col]  # Skip header
                    cell.set_text_props(text=str(table_vals[row][col]))
                    cell.set_color(colors[row] if col == 3 else 'white')

        except Exception as e:
            print(f"Error: {e}")
        return scatter,

    ani_graph = FuncAnimation(fig_graph, update, interval=200, blit=False, cache_frame_data=False)
    plt.tight_layout()
    plt.show()
    if ser:
        ser.close()

if __name__ == "__main__":
    # Start immediately at COM2
    start_graph(com_port)

