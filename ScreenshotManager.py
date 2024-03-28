import os
import json
import requests

# Steam API endpoint for getting game details
STEAM_API_URL = "https://store.steampowered.com/api/appdetails?"

# Folder to scan for screenshots (fix raw string syntax)
folder_to_scan = r"F:\Screenshots"

# File to store known app IDs and game names
data_file = "app_data.json"


def get_game_name(app_id):
    """
    Fetches the game name from Steam API or returns a fallback value.
    """
    url = f"{STEAM_API_URL}appids={app_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Check if data exists for the app ID (handle potential KeyError)
        if app_id in data:
            game_data = data[app_id]  # Access the data dictionary using app_id
            if game_data["success"]:
                return game_data["data"]["name"]  # Access name within the data dict
            else:
                print(f"Failed to retrieve data for app ID: {app_id}")
                return "Unknown"  # Return fallback for failed data retrieval
        else:
            print(f"App ID not found on Steam: {app_id}")
            return "Non-Steam Game"  # Return fallback for non-existent app ID
    else:
        print(f"Error: {response.status_code}")
        return "Unknown"  # Return fallback for API errors
    return app_id


def process_file(filename):
    """
    Extracts app ID from filename, checks data file, fetches name if needed,
    creates folder and moves files
    """
    try:
        # Extract app ID, timestamp, and sequence number
        app_id, timestamp, sequence = filename.split("_")
    except ValueError:
        # Skip files that don't follow the expected format
        print(f"Skipping file with unexpected format: {filename}")
        return

    # Load data from JSON file
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Check if app ID already exists in data
    if app_id in data:
        game_name = data[app_id]  # Use cached name if available
    else:
        # Fetch game name from Steam API
        game_name = get_game_name(app_id)
    
        # Handle non-Steam games and API errors
        if game_name == "Non-Steam Game":
            print(f"Ignoring non-Steam game with app ID: {app_id}")
            return  # Skip processing non-Steam games
        elif game_name == "Unknown":
            print(f"Failed to retrieve game name for app ID: {app_id}")
            return  # Skip processing games with unknown names
    
        # Update data dictionary with the retrieved name
        data[app_id] = game_name
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)


    # Create folder for the game (if it doesn't exist)
    # Sanitize game name to remove invalid characters (e.g., colon)
    safe_game_name = game_name.replace(":", "")  # Replace colon with empty string

    game_folder = os.path.join(folder_to_scan, safe_game_name)
    if not os.path.exists(game_folder):
        os.makedirs(game_folder)

    # Skip files that don't start with the expected format (including app ID)
    if not filename.startswith(f"{app_id}_"):
        print(f"Skipping file with unexpected format: {filename}")
        return

    # Move files starting with the app ID to the game folder
    source_file = os.path.join(folder_to_scan, filename)
    destination_file = os.path.join(game_folder, filename)
    os.rename(source_file, destination_file)


# Main loop
for filename in os.listdir(folder_to_scan):
    if os.path.isfile(os.path.join(folder_to_scan, filename)):
        process_file(filename)

print("Finished processing files.")
