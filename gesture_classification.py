# https://www.geeksforgeeks.org/deep-learning/time-series-classification/
# https://www.geeksforgeeks.org/data-analysis/feature-engineering-for-time-series-data-methods-and-applications/
# https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html

import numpy as np
from sklearn import model_selection, metrics, preprocessing, ensemble, svm, neighbors
import time
import json
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, NoiseTypes, FilterTypes, DetrendOperations


def extract_features(data, sampling_rate):
    signal = np.copy(data)

    # Preprocessing: Detrend and Bandpass filter
    DataFilter.detrend(signal, DetrendOperations.CONSTANT.value)
    DataFilter.perform_bandpass(signal, sampling_rate, 10.0, 250.0, 4, FilterTypes.BUTTERWORTH.value, 0)

    # Root Mean Square
    rms = np.sqrt(np.mean(signal**2))

    # Mean Absolute Value
    mav = np.mean(np.abs(signal))

    # Variance
    var = np.var(signal)

    # Waveform Length
    wl = np.sum(np.abs(np.diff(signal)))

    return [rms, mav, var, wl]

def collect_samples(board, sample_count, label=0):
    samples = []
    labels = []
    time.sleep(2)
    
    for a in range(sample_count):
        time.sleep(1)
        data = board.get_current_board_data(sampling_rate)[1]
        samples.append( extract_features(data, sampling_rate) )
        labels.append(label)
        print(f"Sample {a} collected.")
        
    return (samples, labels)


# Init
BoardShim.enable_dev_board_logger() # verbose debugging
params = BrainFlowInputParams()
board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
# params.serial_port = 'COM3'
# board = BoardShim(BoardIds.CYTON_BOARD.value, params)
sampling_rate = BoardShim.get_sampling_rate(BoardIds.CYTON_BOARD.value)

board.prepare_session()
board.start_stream()


x = []
y = []

# Collect training data

input("Press [Enter] and relax your arm muscles for a few moments")
(samples, labels) = collect_samples(board, 12, 0)
x.extend(samples)
y.extend(labels)

input("Press [Enter] and clench your fist for a few moments")
(samples, labels) = collect_samples(board, 12, 1)
x.extend(samples)
y.extend(labels)

with open("gesture_data.json", "w") as file:
    file.write(json.dumps({'x': x, 'y': y}))

# Reuse training data
# with open("gesture_data.json", "r") as file:
#     data = json.loads(file.read())
#     x = data['x']
#     y = data['y']


# Train model
seed=123456
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=seed)

scaler = preprocessing.StandardScaler()

x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

classifier = ensemble.RandomForestClassifier(n_estimators=50, random_state=seed)
# classifier = svm.SVC(kernel='linear', C=1.0, random_state=seed)
# classifier = svm.SVC(kernel="linear", C=0.025, random_state=seed)
# classifier = svm.SVC(gamma=2, C=1, random_state=seed)
# classifier = neighbors.KNeighborsClassifier(3)
classifier.fit(x_train_scaled, y_train)


# Evaluate model
y_pred = classifier.predict(x_test_scaled)
print(f"Model Accuracy: {metrics.accuracy_score(y_test, y_pred) * 100:.2f}%")


input("#")
# Live classification
while True:
    time.sleep(0.5)
    
    data = board.get_current_board_data(sampling_rate)[1]
    features = extract_features(data, sampling_rate)
    features_scaled = scaler.transform([features])
    
    prediction = classifier.predict(features_scaled)[0]
    probabilities = classifier.predict_proba(features_scaled)[0]
    
    print(f"Prediction: {prediction} | Confidence: {probabilities[prediction]*100:.1f}%")