import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

coordinates = [
    # LOW sensors
    (1, (0, -7)),
    (3, (-2, -6)),
    (6, (-5, -3)),
    (8, (-7, -1)),
    (9, (-7.5, 0)),
    (11, (-6, 2)),
    (14, (-3, 4.5)),
    (31, (-1, 5)),
    (16, (0, 5)),
    (17, (2, 5)),
    (20, (5, 3)),
    (22, (7, 1)),
    (23, (7.5, 0)),
    (25, (6, -2)),
    (28, (3, -5)),
    (30, (1, -7)),
    # HIGH sensors
    (2, (-1, -7)),
    (4, (-3, -5)),
    (5, (-4, -4)),
    (7, (-6, -2)),
    (10, (-7, 1)),
    (12, (-5, 3)),
    (13, (-4, 4)),
    (15, (-2, 5)),
    (32, (1, 5)),
    (18, (3, 4.5)),
    (19, (4, 4)),
    (21, (6, 2)),
    (24, (7, -1)),
    (26, (5, -3)),
    (27, (4, -4)),
    (29, (2, -6))
]

available_ports = [port.device for port in serial.tools.list_ports.comports()]

def start_graph():
    selected_port = port_var.get()
    try:
        ser = serial.Serial(selected_port, 115200, timeout=1)
    except Exception as e:
        messagebox.showerror("Serial Port Error", f"Could not open {selected_port}:\n{e}")
        return

    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = ax.scatter(
        [coord[0] for _, coord in coordinates],
        [coord[1] for _, coord in coordinates],
    s=100
)

    for i, (sensor_id, (x, y)) in enumerate(coordinates):
        label_type = "LOW" if i < 16 else "HIGH"
        ax.text(x, y + 0.4, f"{label_type} {sensor_id}", ha='center', va='center',
                fontsize=6, bbox=dict(facecolor='white', edgecolor='none'))

    ax.set_title("Sensor Visualization\nRed = Active | Blue = Inactive | Yellow = Disabled")
    ax.grid(True)
    ax.set_aspect('equal')

    def update(frame):
        try:
            ser.write(b'R')
            data = ser.readline().decode('utf-8').strip()
            if data:
                values = list(map(int, data.split(',')))
                sensors = values[:32]
                thresholds = values[32:]

                colors = []
                for i in range(32):
                    if thresholds[i] == 0:
                        colors.append('yellow')
                    elif sensors[i] > thresholds[i]:
                        colors.append('red')
                    else:
                        colors.append('blue')
                scatter.set_color(colors)
        except Exception as e:
            print(f"Error: {e}")
        return scatter,

    ani = FuncAnimation(fig, update, interval=200, blit=False)
    plt.tight_layout()
    plt.show()
    ser.close()

root = tk.Tk()
root.title("Sensor COM Port Selector")

tk.Label(root, text="Select COM Port:").pack(pady=5)

port_var = tk.StringVar()
port_dropdown = ttk.Combobox(root, textvariable=port_var)
port_dropdown['values'] = available_ports

if available_ports:
    port_dropdown.current(0)  # Only here

else:
    port_dropdown.set('No COM ports found')
port_dropdown.pack(pady=5)

tk.Button(root, text="Start Graph", command=start_graph).pack(pady=10)

root.mainloop()
