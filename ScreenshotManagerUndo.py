import os


def move_images_back(folder_path):
    """
    Moves all image files from the specified folder back to F:\Screenshots
    """
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            source_file = os.path.join(folder_path, filename)
            destination_file = os.path.join("F:\Screenshots", filename)
            # Check if the destination file already exists
            if os.path.exists(destination_file):
                print(f"Skipping {filename} - File already exists in F:\Screenshots")
            else:
                os.rename(source_file, destination_file)
                print(f"Moved {filename} back to F:\Screenshots")


def process_folder(folder_path):
    """
    Moves images back from the folder and deletes the empty folder
    """
    move_images_back(folder_path)
    # Check if the folder is empty after moving files
    if not os.listdir(folder_path):
        os.rmdir(folder_path)
        print(f"Deleted empty folder: {folder_path}")


# Main loop
for root, dirs, files in os.walk("F:\Screenshots"):
    # Skip the original Screenshots folder itself
    if root != "F:\Screenshots":
        process_folder(root)

print("Finished moving images back to F:\Screenshots.")
