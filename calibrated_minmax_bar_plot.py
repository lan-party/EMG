from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
import time


# Init
BoardShim.enable_dev_board_logger() # verbose debugging
params = BrainFlowInputParams()
# board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
params.serial_port = 'COM3'
board = BoardShim(BoardIds.CYTON_BOARD.value, params)

board.prepare_session()
board.start_stream()


# Calibration
input("Press enter and relax your arm muscles for a moment.")
print("Calibrating", end="", flush=True)
time.sleep(2)
min_avg = 0
for a in range(5):
    time.sleep(1)
    data = board.get_current_board_data(250 * 1)[1]
    DataFilter.detrend(data, 1)
    print(".", end="", flush=True)
    
    min_avg += max(data) - min(data)
min_avg = min_avg / 5

input("\nPress enter and start wiggling your fingers until calibration is complete.")
print("Calibrating", end="", flush=True)
time.sleep(2)
max_avg = 0
for a in range(5):
    time.sleep(1)
    data = board.get_current_board_data(250 * 1)[1]
    DataFilter.detrend(data, 1)
    print(".", end="", flush=True)
    
    max_avg += max(data) - min(data)
max_avg = max_avg / 5

print(f"\nMin avg: {min_avg}\tMax avg: {max_avg}")


# Live plot
y = []
fig, ax = plt.subplots(figsize=(4,6))
bars = ax.bar(['scaled uV min-max difference'], [0])
ax.set_ylim(0,100)

def update(frame):
    global bars
    
    data = board.get_current_board_data(250 * 5)
    y = data[1]
    
    try:
        DataFilter.detrend(y, 1)
        y = y[-250:]
        
        min_max_diff = max(y) - min(y)
        scaled_min_max_diff = (min_max_diff - min_avg) / (max_avg - min_avg) * 100
        
        bars[0].set_height(scaled_min_max_diff)
        
    except:
        pass
    
anim = FuncAnimation(fig, update, frames = None)
plt.show()