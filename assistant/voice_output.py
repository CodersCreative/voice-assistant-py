from sound_effects import play_beep
import sounddevice as sd
import soundfile as sf
import torch
from TTS.api import TTS
import sys
import os
from config import get_config

def text_to_speech_gen(message, filename="ai_output"):
    old_stdout = sys.stdout # backup current stdout
    sys.stdout = open(os.devnull, "w")
    model_config = get_config()["models"]["tts_model"]
    tts = TTS(model_name=model_config["model"], progress_bar=model_config["progress_bar"], gpu=model_config["gpu"])
    tts.tts_to_file(message, file_path=filename+".mp3")
    sys.stdout = old_stdout


def say_text(message, filename="ai_output"):
    text_to_speech_gen(message)
    print("voice started")
    play_beep()
    data, fs = sf.read(filename+".mp3", dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()
    os.remove(filename+".mp3")

