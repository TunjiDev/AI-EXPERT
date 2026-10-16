import threading
import sys

# Dependency check
try:
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    import speech_recognition as sr
    from speech_recognition import AudioData

except ImportError as e:
    print(f"Missing library: {e.name}")
    print("\nInstall commands:")
    print("Windows: pip install SpeechRecognition pyaudio numpy matplotlib")
    print("macOS: brew install portaudio && pip install SpeechRecognition pyaudio numpy matplotlib")
    sys.exit(1)


# Create the event outside the exception block
stop_event = threading.Event()


def wait_for_enter():
    input()
    stop_event.set()


def record_audio(label):
    stop_event.clear()

    p = pyaudio.PyAudio()
    stream = None
    frames = []

    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )

        print(f"\n{label}")
        print("Press Enter to stop...")

        threading.Thread(
            target=wait_for_enter,
            daemon=True
        ).start()

        print("Recording", end="", flush=True)

        while not stop_event.is_set():
            try:
                data = stream.read(
                    1024,
                    exception_on_overflow=False
                )
                frames.append(data)
                print(".", end="", flush=True)

            except OSError as e:
                print(f"\nAudio recording error: {e}")
                break

        print(" Recording stopped.")

        width = p.get_sample_size(pyaudio.paInt16)
        return b"".join(frames), 16000, width

    finally:
        if stream is not None:
            if stream.is_active():
                stream.stop_stream()
            stream.close()

        p.terminate()


def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)

    if len(samples) == 0:
        return {
            "duration": 0,
            "avg_volume": 0,
            "max_volume": 0,
            "samples": samples
        }

    return {
        "duration": len(samples) / rate,
        "avg_volume": np.mean(np.abs(samples)),
        "max_volume": np.max(np.abs(samples)),
        "samples": samples
    }


def transcribe(data, rate, width):
    if not data:
        return "[No audio recorded]"

    recognizer = sr.Recognizer()

    try:
        return recognizer.recognize_google(
            AudioData(data, rate, width)
        )
    except sr.UnknownValueError:
        return "[Speech could not be understood]"
    except sr.RequestError as e:
        return f"[Speech recognition service error: {e}]"


def display_stats(stats, text, label):
    print(f"\n{'─' * 40}")
    print(f"{label}")
    print(f"{'─' * 40}")

    print(f"Duration: {stats['duration']:.2f} seconds")
    print(f"Average Amplitude: {stats['avg_volume']:.0f}")
    print(f"Maximum Amplitude: {stats['max_volume']:.0f}")
    print(f"Transcription: {text}")


def compare(stats1, stats2):
    print("\n" + "=" * 40)
    print("COMPARISON RESULTS")
    print("=" * 40)

    # Duration comparison
    duration1 = stats1["duration"]
    duration2 = stats2["duration"]

    if duration1 > duration2:
        longer = "Recording 1"
        diff = (
            (duration1 - duration2) / duration2 * 100
            if duration2 > 0 else 0
        )
        print(f"{longer} is longer by {diff:.1f}%")

    elif duration2 > duration1:
        longer = "Recording 2"
        diff = (
            (duration2 - duration1) / duration1 * 100
            if duration1 > 0 else 0
        )
        print(f"{longer} is longer by {diff:.1f}%")

    else:
        print("Both recordings have the same duration.")

    # Average volume comparison
    volume1 = stats1["avg_volume"]
    volume2 = stats2["avg_volume"]

    if volume1 > volume2:
        louder = "Recording 1"
        diff = (
            (volume1 - volume2) / volume2 * 100
            if volume2 > 0 else 0
        )
        print(f"{louder} has a higher average amplitude by {diff:.1f}%")

    elif volume2 > volume1:
        louder = "Recording 2"
        diff = (
            (volume2 - volume1) / volume1 * 100
            if volume1 > 0 else 0
        )
        print(f"{louder} has a higher average amplitude by {diff:.1f}%")

    else:
        print("Both recordings have the same average amplitude.")


def plot_both(stats1, stats2, rate):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

    # Plot Recording 1
    samples1 = stats1["samples"]
    t1 = np.arange(len(samples1)) / rate

    ax1.plot(t1, samples1, color="blue", linewidth=0.5)
    ax1.set_title(
        f"Recording 1 (Normal) - Duration: "
        f"{stats1['duration']:.2f}s, "
        f"Avg: {stats1['avg_volume']:.0f}"
    )
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-35000, 35000)

    # Plot Recording 2
    samples2 = stats2["samples"]
    t2 = np.arange(len(samples2)) / rate

    ax2.plot(t2, samples2, color="red", linewidth=0.5)
    ax2.set_title(
        f"Recording 2 (Modified) - Duration: "
        f"{stats2['duration']:.2f}s, "
        f"Avg: {stats2['avg_volume']:.0f}"
    )
    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-35000, 35000)

    plt.tight_layout()
    plt.show()


def main():
    print("=" * 40)
    print("VOICE ANALYSIS LAB")
    print("=" * 40)
    print("Record twice and compare your voice!")

    # Recording 1: Normal voice
    audio1, rate, width = record_audio(
        "Recording 1: Speak NORMALLY"
    )

    stats1 = analyze_audio(audio1, rate)
    text1 = transcribe(audio1, rate, width)

    display_stats(stats1, text1, "Recording 1 Results")

    # Prompt for Recording 2
    input(
        "\nPress Enter to begin Recording 2. "
        "Then speak LOUDER or FASTER..."
    )

    # Recording 2: Changed voice
    audio2, rate, width = record_audio(
        "Recording 2: CHANGE your voice!"
    )

    stats2 = analyze_audio(audio2, rate)
    text2 = transcribe(audio2, rate, width)

    display_stats(stats2, text2, "Recording 2 Results")

    # Compare and visualize
    compare(stats1, stats2)
    plot_both(stats1, stats2, rate)


if __name__ == "__main__":
    main()
