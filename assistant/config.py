CONFIG_FILE = "config.json"
global config
import json

def load_config():
    global config, CONFIG_FILE
    data = open(CONFIG_FILE)
    config = json.load(data)["config"]

def get_config():
    global config
    return config