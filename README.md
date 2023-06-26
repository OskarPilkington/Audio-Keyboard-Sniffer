# Audio Keyboard Sniffer
This is an experimental method of developing software to detect keyboard key presses by audio and decode English text from it.

Keyboard.py and Recorder.py are test scripts to test isolated components of the final DataCollector.py, testing live keyboard input and audio recording respectively.

DataCollector.py records keyboard input, as well as audio input and cuts out audio clips surrounding each keyboard event to use to train a simese network to test whether to key strokes are of the same key.
