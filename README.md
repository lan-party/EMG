A collection of scripts developed to showcase the possibilities for real-time Electromyography (EMG) analysis. I used [this setup guide](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EMGSetup/) to decide on electrode placement and hardcoded all of these scripts to use the data stream from channel 1 on the Cyton board.

- raw_time_series.py - Realtime time series plot of uV samples from a single electrode
- minmax_bar_plot.py - Realtime bar plot of the difference between minimum and maximum time series values
- callibrated_minmax_bar_plot.py - Minmax bar plot with a calibration step to get the relative value range
- mean_slope_bar_plot.py - Mean slope is used for measuring muscle fatigue
- raw_audio.py - Raw time series data converted to sound waves
- spectrogram.py - Realtime spectral analysis
- gesture_classification.py - Binary classifier for clenched fist vs. resting state