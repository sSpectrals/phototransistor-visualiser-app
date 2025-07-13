

def load_coordinates_from_file():
    coordinates = []
    try:
        with open('sensor_coordinates.json', 'r') as file:
            data = json.load(file)
            for item in data:
                sensor_id = item["sensor_id"]
                coord = item["coordinates"]
                coordinates.append((sensor_id, tuple(coord)))
        return coordinates
    except Exception as e:
        print(f"Error loading coordinates: {e}")

coordinates = load_coordinates_from_file()

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
