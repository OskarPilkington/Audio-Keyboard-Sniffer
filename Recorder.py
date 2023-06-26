import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
OUTPUT_FILENAME = "output.wav"
INPUT_DEVICE = "Microphone (Realtek(R) Audio Codec with THX Spatial Audio)"

p = pyaudio.PyAudio()

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

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
                # input_device_index=input_index
                )

print("Recording audio...")

frames = []

# Record audio for the specified duration
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

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

print(f"Audio saved to {OUTPUT_FILENAME}.")
