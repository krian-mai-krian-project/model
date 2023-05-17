import os
import hashlib
from PIL import Image
import shutil

CLEANED_PATH = "train_cleaned"
ORIGINAL_PATH = "train"

# Define a dictionary to store the hash values and file paths
hash_dict = {}

counter = 0
# Recursively iterate through all the files in the folder and its subfolders
for root, dirs, files in os.walk(CLEANED_PATH):
    counter = 0
    for file in files:
        counter +=1
        # print("loading file: " + file)
        if counter % 100 == 0 :
            print(counter)
            # break
            
        file_path = os.path.join(root, file)
        try:
            # Open the file using Pillow to check if it is an image
            with Image.open(file_path) as img:
                # Calculate the hash value of the image file
                hash_value = hashlib.sha256(img.tobytes()).hexdigest()
                # Store the hash value and file path in the dictionary
                hash_dict[hash_value] = file_path
        except:
            # If the file is not an image file, skip it
            print('fail',file)
            pass

# Print the dictionary of hash values and file paths
if not os.path.isdir(ORIGINAL_PATH + "/spam"):
    # use os.makedirs() to create the folder and any intermediate folders
    os.makedirs(ORIGINAL_PATH+ "/spam")

for root, dirs, files in os.walk(ORIGINAL_PATH):
    counter = 0
    for file in files:
        counter +=1
        # print("loading file: " + file)
        if counter % 100 == 0 :
            print(counter)
            # break
        file_path = os.path.join(root, file)
        try:
            # Open the file using Pillow to check if it is an image
            with Image.open(file_path) as img:
                # Calculate the hash value of the image file
                hash_value = hashlib.sha256(img.tobytes()).hexdigest()
                file_path_base = file_path.split("\\")
                file_path_base[-2] = "spam\\"
                new_file_path = "\\".join(file_path_base)
                if hash_value not in hash_dict and "spam" not in file_path:
                    print("Moving", file_path, "->", new_file_path)
                    shutil.move(file_path, new_file_path)
                    
        except:
            print('fail',file)
            pass