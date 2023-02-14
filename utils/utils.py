import configparser
import json

def load_token(filename : str):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['AUTH']['bot_token']

def load_data(filename : str):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(filename : str, data : dict):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
        
def get_google_drive_url_by_id(file_id : str):
    return f'https://drive.google.com/uc?export=view&id={file_id}'
