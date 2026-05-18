import json

def load_game_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data