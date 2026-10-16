"""
L1: Basic Speech-to-Text
Record → Save → Transcribe → Visualize Waveform
"""
import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData

stop_event = threading.Event()

def wait_for_enter():
    input("\n🎤 Press Enter to stop recording...\n")
    stop_event.set()

def spinner():
    chars = '|/-\\'
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r🔴 Recording... {chars[i % 4]}')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    print("\r✅ Recording complete!          ")

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=1024)
    frames = []
    
    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()
    
    while not stop_event.is_set():
        frames.append(stream.read(1024))
    
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b''.join(frames), 16000, width

def save_audio(data, rate, width, filename="recording.wav"):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"💾 Saved: {filename}")

def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    audio = AudioData(data, rate, width)
    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 Transcription: {text}")
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")

def plot_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, len(samples))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color='blue')
    plt.title("Your Voice Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 40)
    print("🎙️  HELLO AI, CAN YOU HEAR ME?")
    print("=" * 40)
    print("\nSpeak into your microphone...")
    
    audio_data, rate, width = record_audio()
    save_audio(audio_data, rate, width)
    transcribe(audio_data, rate, width)
    plot_waveform(audio_data, rate)

if __name__ == "__main__":
    main()

# import threading
# import sys
# import time
# import pyaudio
# import numpy as np
# import matplotlib.pyplot as plt
# import wave
# import speech_recognition as sr
# from speech_recognition import AudioData

# stop_event = threading.Event()

# def wait_for_enter():
#     input("\nPress Enter to stop recording...\n")
#     stop_event.set()

# def spinner():
#     spinner_chars = '|/-\\'
#     idx = 0
#     while not stop_event.is_set():
#         sys.stdout.write('\rRecording... ' + spinner_chars[idx % len(spinner_chars)])
#         sys.stdout.flush()
#         idx += 1
#         time.sleep(0.1)
#     sys.stdout.write('\rRecording stopped.          \n')

# def record_until_enter():
#     p = pyaudio.PyAudio()
#     format = pyaudio.paInt16
#     channels = 1
#     rate = 16000
#     frames_per_buffer = 1024

#     stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
#     frames = []

#     threading.Thread(target=wait_for_enter).start()
#     threading.Thread(target=spinner).start()

#     while not stop_event.is_set():
#         try:
#             data = stream.read(frames_per_buffer)
#             frames.append(data)
#         except Exception as e:
#             print("Error reading stream:", e)
#             break

#     stream.stop_stream()
#     stream.close()
#     sample_width = p.get_sample_size(format)
#     p.terminate()

#     audio_data = b''.join(frames)
#     return audio_data, rate, sample_width

# def save_audio(data, rate, width, filename="audio.wav"):
#     with wave.open(filename, "wb") as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(width)
#         wf.setframerate(rate)
#         wf.writeframes(data)
#     print(f"Saved: {filename}")

# def transcribe_audio(data, rate, width, filename="transcription.txt"):
#     r = sr.Recognizer()
#     audio = AudioData(data, rate, width)
#     try:
#         text = r.recognize_google(audio)
#     except sr.UnknownValueError:
#         text = "Could not understand the audio."
#     except sr.RequestError as e:
#         text = f"API Error: {e}"
#     print("Transcription:", text)
#     with open(filename, "w") as f:
#         f.write(text)
#     print(f"Saved: {filename}")

# def show_waveform(data, rate):
#     samples = np.frombuffer(data, dtype=np.int16)
#     time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
#     plt.plot(time_axis, samples)
#     plt.title("Audio Waveform")
#     plt.xlabel("Time (s)")
#     plt.ylabel("Amplitude")
#     plt.tight_layout()
#     plt.show()

# def main():
#     print("Start speaking. Press Enter to stop.")
#     audio_data, rate, width = record_until_enter()
#     save_audio(audio_data, rate, width)
#     transcribe_audio(audio_data, rate, width)
#     show_waveform(audio_data, rate)

# if __name__ == "__main__":
#     main()