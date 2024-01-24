from chat import input_message, setup_chat
from voice_output import say_text
from voice_record import transcribe_audio, new_record_audio
from sound_effects import play_beep
from config import get_config, load_config
from wake import check_for_word, record_word
import time

global word_found
word_found = False

def main():
    load_config()
    config = get_config()
    setup_chat()
    
    while True:
        if config["general_settings"]["text_mode"]:
            user_input = input("> ")
            if user_input.lower() == "quit":
                break
            print(input_message(user_input))
        else:
            global word_found
            if word_found:
                word_found_fn()
            else:
                word_not_found()
                

def word_found_fn():
    global word_found
    config = get_config()
    play_beep()
    recorded_audio_path = new_record_audio()
    play_beep()
    transcript = ""
    vad_filter = config["recording_settings"]["wake_settings"]["vad_filter"]
    transcript = transcribe_audio(recorded_audio_path, ai_model=config["models"]["stt_models"]["main_model"], vad=vad_filter)
    if str(transcript) != "":
        start_time = time.time()
        output = input_message(transcript)
        print("Chatbot time: {0}".format(time.time() - start_time))
        print(output)
        say_text(output, config["file_paths"]["output_file"])
        word_found = False

def word_not_found():
    global word_found
    path = record_word()
    word_found = check_for_word(path)


if __name__ == "__main__":
    main()

