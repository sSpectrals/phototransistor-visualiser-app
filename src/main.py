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

# Get all current ports used by the system for serial communication
available_ports = [port.device for port in serial.tools.list_ports.comports()]

def start_graph():
    selected_port = port_var.get()
    try:
        ser = serial.Serial(selected_port, 115200, timeout=1)
    except Exception as e:
        messagebox.showerror("Serial Port Error", f"Could not open {selected_port}:\n{e}")
        return

    # Create figure with two axes: plot + table
    # You can adjust the size etc
    fig = plt.figure(figsize=(8, 8))

    gs = fig.add_gridspec(1, 2, width_ratios=[1, 2])
    
    # Table axis (left)
    ax_table = fig.add_subplot(gs[0])

    # Graph axis (right)
    ax = fig.add_subplot(gs[1])

    # Scatter plot for sensors
    scatter = ax.scatter(
        [coord[0] for _, coord in coordinates],
        [coord[1] for _, coord in coordinates],
        s=100
    )

    # Create a label for each sensor based on the coordinates
    # You can customize the label position and other elements as needed
    for label, (x, y) in coordinates:
        ax.text(x, y + 0.3, str(label), ha='center', fontsize=8)

    ax.set_title(
        f"Sensor Visualisation\n"
        f"activeColor = {activeColor} | "
        f"inactiveColor = {inactiveColor} | "
        f"disabledColor = {disabledColor}"
    )
    ax.grid(True)
    ax.set_aspect('equal')

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
            ser.write(b'R')
            data = ser.readline().decode('utf-8').strip()
            if data:
                values = list(map(int, data.split(',')))

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

    ani = FuncAnimation(fig, update, interval=200, blit=False)
    plt.tight_layout()
    plt.show()
    ser.close()

# Dropdown menu for selecting COM port
root = tk.Tk()
root.title("Sensor COM Port Selector")

tk.Label(root, text="Select COM Port:").pack(pady=5)

port_var = tk.StringVar()
port_dropdown = ttk.Combobox(root, textvariable=port_var)
port_dropdown['values'] = available_ports

# Select the first available port by default if any are found
if available_ports:
    port_dropdown.current(0)
else:
    port_dropdown.set('No COM ports found')
port_dropdown.pack(pady=5)

# Button to start the graph
tk.Button(root, text="Start Graph", command=start_graph).pack(pady=10)

root.mainloop()
