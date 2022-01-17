from multiprocessing import Process
from PIL import Image
import os
import re
import time

def main():
    # Print Welcome Text
    print("=====================================================================")                                                                 
    print(" _____         _           _        _____ _   _ _       _            ")
    print("|   __|___ ___| |_ ___ ___|_|___   |   __| |_|_| |_ ___| |_ ___ ___  ")
    print("|   __| .'|  _|  _| . |  _| | . |  |__   |  _| |  _|  _|   | -_|  _| ")
    print("|__|  |__,|___|_| |___|_| |_|___|  |_____|_| |_|_| |___|_|_|___|_|   ")
    print("=====================================================================")
    print("Starting Factorio Image Stitcher!                        by Nathanael")

    # Get Configuration Data
    input_path = getDirectoryPath("Input Folder: ")
    output_path = getDirectoryPath("Output Folder: ")

    # To understand regex better use e.g. https://regex101.com/
    # Pattern: screenshotNUMBER_xNUMBER_yNUMBER.png e.g. screenshot1234_x0_y13.png
    # Group 0 -> Screenshot ID
    # Group 1 -> X Coordinate
    # Group 2 -> Y Coordinate
    pattern = re.compile(r"screenshot(\d*)_x(\d*)_y(\d*).png")

    # Multi Processing
    processes = []
    process_count = 8

    current_screenshot_id :str = ""
    total_file_count = 0
    processed_files = 0
    start_time = time.time()

    # Get Total File Count of folder
    with os.scandir(input_path) as it:
        total_file_count = sum(1 for _ in it)

    if total_file_count == 0:
        print("No files in selected input folder!")
        return

    with os.scandir(input_path) as it:
        # Image File Name, (x,y)
        image_data = []
        for entry in it:
            # Check for validity 
            file_name :str = entry.name
            match = pattern.match(file_name)
            if match is None:
                print(f"File: '{file_name}' is not a valid screenshot!")
                continue

            screenshot_id = match.group(1)
            coords = (match.group(2), match.group(3))

            # Only relevant for first iteration
            if(not current_screenshot_id):
                current_screenshot_id = screenshot_id

            # Stitch image
            if(screenshot_id != current_screenshot_id):
                # Makes sure only a fixed amount of processes is started
                while len(processes) > process_count:
                    processToRemove = []
                    for pro in processes:
                        pro.join(timeout=0)
                        if not pro.is_alive():
                            processToRemove.append(pro)
                    for pro in processToRemove:
                        processes.remove(pro)

                # Start process with image
                process = Process(target=stitchImage, args=(image_data, output_path, current_screenshot_id))
                process.start()
                processes.append(process)

                image_data.clear()
                current_screenshot_id = screenshot_id

                progress_bar(processed_files, total_file_count)
                #print(f"Progress: {processed_files}/{total_file_count}")
                

            image_data.append([input_path + r"\\" + file_name, coords])
            processed_files += 1

        for process in processes:
            process.join()

        # Stitch last image once loop finished
        stitchImage(image_data, output_path, current_screenshot_id)

        print(f"Finished stitching all images! It took {round((time.time() - start_time) / 60,2)} minutes.")

def progress_bar(current, total, bar_length = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces  = ' ' * (bar_length - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')


def stitchImage(image_parts, output_path, current_screenshot_id):
    # Get Information about image package
    image :Image = Image.open(image_parts[0][0])
    (width, height) = image.size
    image.close()

    maxX :int = 0
    maxY :int = 0

    # find out max x and max y
    for entry in image_parts:
        maxX = max(maxX, int(entry[1][0]))
        maxY = max(maxY, int(entry[1][1]))

    imageWidth = width * int(maxY) + width
    imageHeight = height * int(maxX) + height
    sizeTouple = (imageWidth, imageHeight)

    # Stitch
    stitched = Image.new('RGB', sizeTouple)
    for entry in image_parts:
        image :Image = Image.open(entry[0])

        x = int(entry[1][0]) * width
        y = int(entry[1][1]) * height

        stitched.paste(im= image, box=(x, y))
        image.close()

    stitched.save(output_path + "\\" + current_screenshot_id + ".png", "PNG")

def getDirectoryPath(prompt_message :str):
    while True:
        directory_path = input(prompt_message)
        if not os.path.isdir(directory_path):
            if os.path.isfile(directory_path):
                print("Selected path is a file. Please select a directory instead.")

            print(f"Invalid directory path! '{directory_path}'")
        else:
            print(f"Valid path selected: '{directory_path}'")
            return directory_path

if __name__ == "__main__":
    main()