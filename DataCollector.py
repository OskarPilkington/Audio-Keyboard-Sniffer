import pyaudio
import wave
import keyboard
import time
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy import signal

# Setting up settings for input audio
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100*2
RECORD_SECONDS = 100
OUTPUT_FILENAME = "output.wav"
INPUT_DEVICE = "Microphone (Realtek(R) Audio Codec with THX Spatial Audio)"

p = pyaudio.PyAudio()

# Getting the correct input device registered
device_count = p.get_device_count()
print(f"There are {device_count} devices...")

input_index = None

for i in range(device_count):
    device_info = p.get_device_info_by_index(i)
    # print(f"Device {i}: {device_info['name']}")
    if device_info['name'] == INPUT_DEVICE:
        input_index = i
# Print which microphone has been selected, it must be the same as the one selected as default in windows settings.
print(f"Selected device {input_index}: {p.get_device_info_by_index(input_index)['name']}")


# Defining keyboard interrupt handler
def on_key_press(event):
    if event.name == 'esc':
        # Stop the program when the 'esc' key is pressed
        keyboard.unhook_all()
    else:
        # Print the key name and the elapsed time since the program started
        print(f"Key: {event.name}, Time: {time.time() - start_time:.3f} seconds")
        key_strokes.append((event.name, time.time() - start_time))

# Register the key press event handler
keyboard.on_press(on_key_press)
# Setup list to store key inputs
key_strokes = []


# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
                # input_device_index=input_index
                )
start_time = time.time()



print("Recording audio...")

frames = []
audio_chunks = []
# Record audio for the specified duration
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    audio_chunks.append(np.frombuffer(data, dtype=np.int16))

combined_audio = np.concatenate(audio_chunks)

print("Finished recording.")

# Stop and close the audio stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded audio to a file
wf = wave.open(OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()

# Flushing keyboard so it doesn't print to terminal
# keyboard.flush() # Doesn't work...

print(f"Audio saved to {OUTPUT_FILENAME}.")

pre  = 4096
post = 4096

key_count = {}
for press in key_strokes:
    press_index = int(press[1]*RATE)
    press_key = press[0]
    
    name = ""
    local_time = time.localtime()
    if press_key in key_count:
        name = "output\\" + time.strftime("%Y-%m-%d_%H-%M-%S", local_time) + "_" + press_key + f"_({key_count[press_key]})" +  ".wav"
        key_count[press_key] += 1
    else:
        name = "output\\" + time.strftime("%Y-%m-%d_%H-%M-%S", local_time) + "_" + press_key + "_(0)" + ".wav"
        key_count[press_key] = 1

    print(name)
    wf = wave.open(name, "wb")
    wf.setparams((CHANNELS, p.get_sample_size(FORMAT), RATE, 0, 'NONE', 'not compressed'))
    audio_data = combined_audio[press_index-pre:press_index+post].astype(np.int16)
    wf.writeframes(audio_data.tobytes())
    wf.close()


key_indexes = [int(i[1]*RATE) for i in key_strokes]

plt.figure()
plt.plot(combined_audio)
for pos in key_indexes:
    plt.axvline(x=pos, color='red', linestyle='--')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.title('Audio Stream')
plt.show(block=False)

plt.figure()
# for press in key_indexes:
#     plt.plot(combined_audio[press-pre:press+post])
plt.plot(combined_audio[key_indexes[0]-pre:key_indexes[0]+post])
plt.axvline(x=pre, color='red', linestyle='--')
plt.show(block=False)


# n_mfcc = 13  # Number of MFCC coefficients
# n_mels = 40  # Number of Mel filters
# fmin = 0     # Minimum frequency of the filterbank
# fmax = 300  # Maximum frequency of the filterbank
# hop_length = 64

# mfcc = librosa.feature.mfcc(y=combined_audio[key_indexes[0]-pre:key_indexes[0]+post].astype(np.float32), sr=RATE, hop_length=hop_length, fmin=fmin, fmax=fmax, n_mels=n_mels, n_mfcc=n_mfcc)
# plt.figure(figsize = (10,4))
# librosa.display.specshow(mfcc, x_axis='time', vmax = 60)
# plt.colorbar()
# plt.title('MFCC')
# plt.tight_layout()
# plt.show()

plot_cnt = 5
# plt.figure()
fig, axes = plt.subplots(plot_cnt,1)
for i in range(plot_cnt):
    window_size = int(RATE * 1)  # Window size in samples (e.g., 100 ms)

    frequencies, times, spectrogram = signal.spectrogram(combined_audio[key_indexes[i]-pre:key_indexes[i]+post], fs=RATE, nperseg=64)

    # Plot the spectrogram
    # plt.figure()
    axes[i].pcolormesh(times, frequencies, np.log10(spectrogram))
    # plt.colorbar(label='Power Spectral Density (dB/Hz)')
    # axes[i].set_xlabel('Time (s)')
    # axes[i].set_ylabel('Frequency (Hz)')
    # axes[i].set_title('FFT Spectrogram')
plt.show(block = True)
