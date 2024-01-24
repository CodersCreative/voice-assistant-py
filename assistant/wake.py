from voice_record import *
import re
from math import *
import os
from scipy.io.wavfile import read
import numpy as np
from config import get_config

def record_word():
    return new_wake_record()
    

def check_for_word(recorded_audio_path):
    vad_filter = get_config()["recording_settings"]["wake_settings"]["vad_filter"]
    transcript = transcribe_audio(recorded_audio_path, ai_model=get_config()["models"]["stt_models"]["main_model"], vad=vad_filter)

    # Compile a case-insensitive regular expression for efficient matching
    wake_word_regex = re.compile(r"\b(?:" + "|".join(get_config()["wake_words"]) + r")\b", re.IGNORECASE)

    # Check for wake words directly in the transcript string
    is_activated = bool(wake_word_regex.search(str(transcript)))

    return is_activated