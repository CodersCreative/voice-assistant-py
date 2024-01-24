import sounddevice as sd
import soundfile as sf
from config import get_config

def play_beep():
    # Extract data and sampling rate from file
    data, fs = sf.read(get_config()["file_paths"]["beep_file"], dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()