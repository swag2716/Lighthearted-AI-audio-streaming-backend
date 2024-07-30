from pydub import AudioSegment
import numpy as np

def process_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = len(audio) / 1000.0  # Duration in seconds

    # Generate wave data (simplified example)
    samples = audio.get_array_of_samples()
    wave_data = np.array(samples).reshape((-1, 2))
    wave_data = wave_data.mean(axis=1)  # Convert stereo to mono
    wave_data = wave_data[::1000]  # Downsample for visualization

    return duration, wave_data.tolist()