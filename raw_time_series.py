from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
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


# Live plot
x = []
y = []
fig, ax = plt.subplots()
graph = ax.plot(x,y)[0]
ax.set_ylim(-1000,1000)
ax.set_ylabel('uV')

def update(frame):
    global graph
    
    data = board.get_current_board_data(250 * 5)
    x = list(range(len(data[1])))
    y = data[1]
    
    try:
        # DataFilter.remove_environmental_noise(y, BoardShim.get_sampling_rate(BoardIds.CYTON_BOARD.value), NoiseTypes.SIXTY.value)
        DataFilter.detrend(y, 1)
        
        graph.set_xdata(x)
        graph.set_ydata(y)
        plt.xlim(x[0], x[-1])
        
    except Exception as e:
        print(e)

anim = FuncAnimation(fig, update, frames = None)
plt.show()