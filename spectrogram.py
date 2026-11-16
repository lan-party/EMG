
# https://matplotlib.org/stable/gallery/images_contours_and_fields/specgram_demo.html

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, NoiseTypes


# Init
BoardShim.enable_dev_board_logger() # verbose debugging
params = BrainFlowInputParams()
# board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
params.serial_port = 'COM3'
board = BoardShim(BoardIds.CYTON_BOARD.value, params)

board.prepare_session()
board.start_stream()


data = board.get_current_board_data(250 * 5)[1]

fig, ax = plt.subplots()
graph = ax.specgram(data, NFFT=250, Fs=250)

def update(frame):
    global graph
    global data
    
    data = board.get_current_board_data(250 * 5)[1]
    
    DataFilter.remove_environmental_noise(data, BoardShim.get_sampling_rate(BoardIds.CYTON_BOARD.value), NoiseTypes.SIXTY.value)
    
    DataFilter.detrend(data, 1)
    
    ax.specgram(data, NFFT=250, Fs=250)
    plt.draw()
    fig.canvas.flush_events()


anim = FuncAnimation(fig, update, frames = None)
plt.show()