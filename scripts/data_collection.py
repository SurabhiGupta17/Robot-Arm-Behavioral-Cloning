import time
import csv
import os
from pynput import keyboard
from pynput.keyboard import Key
from lerobot.common.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig
from lerobot.common.teleoperators.so101_leader.so101_leader import SO101Leader

robot_config = SO101LeaderConfig(port='/dev/ttyACM0', use_degrees=True)
robot = SO101Leader(robot_config)

robot.connect()
if robot.is_connected:
    print("Robot is connected.")

stop_trigger = False

def on_press(key):
    global stop_trigger
    if key==Key.enter or key==Key.space:
        stop_trigger = True


listener = keyboard.Listener(on_press=on_press)
listener.start()

file_numbers=[]
for file in os.listdir("../dataset/"):
    if file.endswith("csv"):
        file = file.removesuffix(".csv")
        file_numbers.append(int(file))

if file_numbers:
    file_name = f"{max(file_numbers) + 1:03}.csv"
else:
    file_name = "001.csv"


header = ['shoulder_pan', 'shoulder_lift', 'elbow_flex', 'wrist_flex', 'wrist_roll', 'gripper']
with open(f"../dataset/{file_name}", "w") as f:
    writer=csv.writer(f)
    writer.writerow(header)

    while not stop_trigger:
        data=robot.get_action()
        writer.writerow(data.values())
        time.sleep(0.2)

print("Trajectory recorded.")
listener.stop()