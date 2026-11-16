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
bars1 = ax.bar(['Mean Slope'], [0])
bars2 = ax.bar(['Mean Slope'], [0])
ax.set_ylim(-10,10)

def update(frame):
    global bars1
    global bars2
    
    data = board.get_current_board_data(250 * 5)
    y = data[1]
    
    try:
        DataFilter.detrend(y, 1)
        y = y[-250:]
        
        positive_slopes = []
        negative_slopes = []
        for a in range(len(y)):
            if a < len(y)-1:
                slope = y[a+1] - y[a]
                if slope > 0:
                    positive_slopes.append(slope)
                elif slope < 0:
                    negative_slopes.append(slope)
        
        positive_mean_slope = sum(positive_slopes) / len(positive_slopes)
        negative_mean_slope = sum(negative_slopes) / len(negative_slopes)
        
        bars1[0].set_height(positive_mean_slope)
        bars2[0].set_height(negative_mean_slope)
        
    except:
        pass

anim = FuncAnimation(fig, update, frames = None)
plt.show()