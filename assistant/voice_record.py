#import whisper
from faster_whisper import WhisperModel
import sounddevice as sd
import soundfile as sf
import time
from pynput import keyboard
import pyaudio
import wave
import speech_recognition as sr
import os
from collections import deque
import math
import audioop
from config import get_config
#import keyboard as key



global current_model, stopped, stt_ai_model, first_time
stopped = False
first_time = True
name = "recording"
stt_ai_model = "tiny.en"
current_model = WhisperModel(stt_ai_model, device="cpu", compute_type="int8")


def get_stt_model():
    global current_model
    return current_model

def change_stt_ai_model(new_model):
    global stt_ai_model, current_model, first_time
    stt_config = get_config()["models"]["stt_models"]
    if stt_ai_model != new_model or first_time:
        current_model = WhisperModel(new_model, device=stt_config["device"], compute_type=stt_config["compute_type"])
        stt_ai_model = new_model
        first_time = False
    return current_model
 
def generate_random_name():
    return name

def get_stopped():
    global stopped
    return stopped

def new_record_audio():
    path = get_config()["file_paths"]["recording_file"]
    settings = get_config()["recording_settings"]["main_settings"]
    return record(settings["silent_secs"], settings["max_secs"], settings["silence_start"], path, settings["rate"], settings["chunk_size"], settings["audio_channels"])

def new_wake_record():
    path = get_config()["file_paths"]["wake_file"]
    settings = get_config()["recording_settings"]["wake_settings"]
    return record(settings["silent_secs"], settings["max_secs"], settings["silence_start"], path, settings["rate"], settings["chunk_size"], settings["audio_channels"])


def record(seconds, max_seconds, silence, audio_name="recording", fs=16000, chunk=1024, audio_channels=1):
    print("recording")
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=audio_channels,
        rate=fs,
        input=True,
        frames_per_buffer=chunk
    )

    frames = []
    start_time = time.time()
    silence_count = 0
    while True:
        data = stream.read(chunk)
        frames.append(data)

        rms = math.sqrt(abs(audioop.avg(data, 4)))

        if rms < silence:
            silence_count += 1
        else:
            silence_count = 0

        if silence_count >= seconds * fs / chunk:
            break  # Stop recording after silence duration

        if max_seconds > 0 and time.time() - start_time >= max_seconds:  # Stop after specified time
            break


    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(f'./{audio_name}.wav', 'wb')
    wf.setnchannels(audio_channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Recording stopped.")
    return f'{audio_name}.wav'



def transcribe_audio(recorded_audio_path, ai_model="tiny.en", vad=True):
    model = change_stt_ai_model(ai_model)

    audio_path = "./"+recorded_audio_path

    segments, _ = model.transcribe(audio=audio_path, beam_size=5, vad_filter=vad) #
    segments = list(segments)
    #print(se)
    transcript = ""
    for segment in segments:
        transcript += segment.text

    print(f"Path: {audio_path}, Transcript: {transcript}")
    os.remove(audio_path)
    return transcript

def on_press(key):
    if key == keyboard.Key.space:
        global stopped
        stopped = True



