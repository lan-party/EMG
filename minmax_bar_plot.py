from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter


# Init
BoardShim.enable_dev_board_logger() # verbose debugging
params = BrainFlowInputParams()
# board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
params.serial_port = 'COM3'
board = BoardShim(BoardIds.CYTON_BOARD.value, params)

board.prepare_session()
board.start_stream()


# Live plot
y = []
fig, ax = plt.subplots(figsize=(4,6))
bars = ax.bar(['uV min-max difference'], [0])
ax.set_ylim(0,1000)

def update(frame):
    global bars
    
    data = board.get_current_board_data(250 * 5)
    y = data[1]
    
    try:
        DataFilter.detrend(y, 1)
        y = y[-250:]
        
        min_max_difference = max(y) - min(y)
        bars[0].set_height(min_max_difference)
        
    except:
        pass

anim = FuncAnimation(fig, update, frames = None)
plt.show()