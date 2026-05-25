import json

def save_game_data(filepath, data):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        print("Data saved successfully")

    except Exception as e:
        print(f"Error saving data: {e}")