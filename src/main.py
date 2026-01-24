import json
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from direction import get_arrow_direction_defender, get_arrow_direction_attacker

# for defender arrow direction calculation
# Keep within -15 to 15 range
xBall = 2
yBall = 5

# Custom colors for categories
activeColor_attacker = 'red'
activeColor_defender = 'blue'
inactiveColor = 'yellow'
disabledColor = 'grey'

# COM 1-N or NONE for custom input test data
com_port = 'COM1'

           # first #num-sensors = sensor values, next #num-sensors = thresholds
           #  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39
test_data = [10, -1, -1, -1, -1, -1,  1, -1, -1, -1, -1, -1, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, 10, 10, 101, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 100, -1, -1, -1, -1,
              1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1,  1, 1, -1, -1, -1, -1, -1, -1, -1, 1,  1,   1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,   1, -1, -1, -1, -1]

# Validate test_data length
def validate_array_length(test_data, num_sensors):
    expected_length = num_sensors * 2
    if len(test_data) != expected_length:
        error_msg = (
            f"Error: test_data length is {len(test_data)}, but expected {expected_length} "
            f"- NUM_SENSORS * 2, where NUM_SENSORS is the number of objects in the JSON file. Please check your test_data definition.\n"
            f"- First NUM_SENSORS values are sensor readings.\n"
            f"- Next NUM_SENSORS values are thresholds."
        )
        print(error_msg)
        raise ValueError(error_msg)

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
validate_array_length(test_data, NUM_SENSORS)


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
    # Add orange point for ball location
    ball_point = ax_graph.scatter([xBall], [yBall], s=150, c='orange', marker='o', label='Ball')
    
    
    
    red_arrow = None
    blue_arrow = None

    # Create a label for each sensor based on the coordinates
    # You can customize the label position and other elements as needed
    for label, (x, y) in coordinates:
        ax_graph.text(x, y + 0.3, str(label), ha='center', fontsize=8)

    ax_graph.set_title(
        f"Sensor Visualisation\n"
        f"| activeColor_attacker = {activeColor_attacker} | "
        f"activeColor_defender = {activeColor_defender} | \n"
        f"| inactiveColor = {inactiveColor} | "
        f"disabledColor = {disabledColor} | "
        f"\nBall location: ({xBall}, {yBall}) (orange)"
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
            try:
                validate_array_length(values, NUM_SENSORS)
            except ValueError as ve:
                print(ve)
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
                    color = activeColor_attacker if i >= 24 else activeColor_defender
                else:
                    status = "Inactive"
                    color = inactiveColor

                colors.append(color)
                table_vals.append([label, sensor, threshold, status])


            scatter.set_color(colors)

            # Remove previous red arrow if it exists
            nonlocal red_arrow
            if red_arrow is not None:
                red_arrow.remove()
                red_arrow = None
            
            nonlocal blue_arrow
            if blue_arrow is not None:
                blue_arrow.remove()
                blue_arrow = None

            # Get arrow direction from helper function
            arrow_direction_red = get_arrow_direction_attacker(colors, activeColor_attacker=activeColor_attacker)
            if arrow_direction_red:
                red_arrow = ax_graph.arrow(-arrow_direction_red[0], -arrow_direction_red[1], 2*arrow_direction_red[0], 2*arrow_direction_red[1], head_width=0.5, head_length=0.5, fc="red", ec="red", length_includes_head=False)

            arrow_direction_blue = get_arrow_direction_defender(colors, activeColor_defender=activeColor_defender, xBall=xBall, yBall=yBall, coordinates=coordinates)
            if arrow_direction_blue:
                blue_arrow = ax_graph.arrow(-2*arrow_direction_blue[0], -2*arrow_direction_blue[1], 4*arrow_direction_blue[0], 4*arrow_direction_blue[1], head_width=0.5, head_length=0.5, fc="blue", ec="blue", length_includes_head=False)

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
    start_graph(com_port)

