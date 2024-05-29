import os
import shutil

def delete_directories_in_cwd():
    # Get the current working directory
    cwd = os.getcwd()
    
    # List all items in the current working directory
    items = os.listdir(cwd)
    
    # Loop through all items
    for item in items:
        item_path = os.path.join(cwd, item)
        
        # Check if the item is a directory
        if os.path.isdir(item_path) and item != '.git':
            # Delete the directory and its contents
            shutil.rmtree(item_path)

if __name__ == "__main__":
    delete_directories_in_cwd()
