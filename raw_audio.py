
# https://people.csail.mit.edu/hubert/pyaudio/docs/
# https://github.com/timbatt/music_maker
# https://python-sounddevice.readthedocs.io/en/0.5.3/


from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, NoiseTypes
import numpy as np
import sounddevice
import time


# Init
BoardShim.enable_dev_board_logger() # verbose debugging
params = BrainFlowInputParams()
# board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
params.serial_port = 'COM3'
board = BoardShim(BoardIds.CYTON_BOARD.value, params)

board.prepare_session()
board.start_stream()


ephys_sample_rate = BoardShim.get_sampling_rate(BoardIds.CYTON_BOARD.value)
audio_sample_rate = sounddevice.query_devices(kind='output')['default_samplerate']


with sounddevice.OutputStream(samplerate=audio_sample_rate, channels=1) as stream:

    while True:
        
        try:
            data = board.get_current_board_data(250)[1]
            
            DataFilter.detrend(data, 1)
            
            data_stretched = []
            for sample in data:
                for a in range(int(audio_sample_rate / ephys_sample_rate)):
                    data_stretched.append(sample)
            
            stream.write(np.array(data_stretched).astype('float32'))
        except Exception as e:
            print(e)