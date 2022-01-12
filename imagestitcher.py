from multiprocessing import Process
from tkinter.constants import HORIZONTAL
from PIL import Image
import os
import re

def main():
    print("=====================================================================")                                                                 
    print(" _____         _           _        _____ _   _ _       _            ")
    print("|   __|___ ___| |_ ___ ___|_|___   |   __| |_|_| |_ ___| |_ ___ ___  ")
    print("|   __| .'|  _|  _| . |  _| | . |  |__   |  _| |  _|  _|   | -_|  _| ")
    print("|__|  |__,|___|_| |___|_| |_|___|  |_____|_| |_|_| |___|_|_|___|_|   ")
    print("=====================================================================")
    print("Starting Factorio Image Stitcher!")

    # Get Configuration Data
    inputPathRaw = input("Input Folder:")
    if not inputPathRaw:
        inputPathRaw = "D:\DEV\FactorioImageStitcher\input"
    
    if not os.path.exists(inputPathRaw):
        print(f"Invalid Input Path! '{inputPathRaw}'")
        return

    outputPathRaw = input("Output Folder:")
    if not outputPathRaw:
        outputPathRaw = "D:\DEV\FactorioImageStitcher\output"

    if not os.path.exists(outputPathRaw):
        print(f"Invalid Output Path! '{outputPathRaw}'")
        return

    inputPath  = inputPathRaw
    outputPath = outputPathRaw

    # Process Count
    inputProcessCountRaw = input("Process Count:")
    if not inputProcessCountRaw.isdigit():
        inputProcessCountRaw = 8
    processCount = int(inputProcessCountRaw)

    # Test on https://regex101.com/ - Pattern match: screenshotNUMBER_xNUMBER_yNUMBER.png e.g. screenshot1234_x0_y13.png
    pattern = re.compile(r"screenshot(\d*)_x(\d*)_y(\d*).png")

    processes = []

    currentScreenshotID :str = ""

    totalFileCount = 0
    processedFiles = 0

    # Get Total File Count of folder
    with os.scandir(inputPath) as it:
        totalFileCount = sum(1 for _ in it)

    if totalFileCount == 0:
        print("No files in selected input folder!")
        return

    with os.scandir(inputPath) as it:
        # Image File Name, (x,y)
        imageData = []
        for entry in it:
            # Check for validity 
            fileName :str = entry.name
            match = pattern.match(fileName)
            if match is None:
                print(f"File: '{fileName}' is not a valid screenshot!")
                continue

            #print(f"ID: {match.group(1)} | x: {match.group(2)} | y: {match.group(3)} ")
            screenshotID = match.group(1)
            coords = (match.group(2), match.group(3))

            # Only relevant for first iteration
            if(not currentScreenshotID):
                currentScreenshotID = screenshotID

            # Stitch image
            if(screenshotID != currentScreenshotID):
                while len(processes) > processCount:
                    processToRemove = []
                    for pro in processes:
                        pro.join(timeout=0)
                        if not pro.is_alive():
                            processToRemove.append(pro)
                    for pro in processToRemove:
                        processes.remove(pro)


                #print("Activ running processes:", len(processes))

                #if len(processes) > processCount:
                #    for process in processes:
                #        process.join()
                #    processes.clear()

                process = Process(target=stitchImage, args=(imageData, outputPath, currentScreenshotID))
                process.start()
                processes.append(process)
                #stitchImage(imageData, outputPath, currentScreenshotID)

                imageData.clear()
                currentScreenshotID = screenshotID

                #print(f"Progress: {processedFiles}/{totalFileCount}")
                

            imageData.append([inputPath + r"\\" + fileName, coords])
            processedFiles += 1

        for process in processes:
            process.join()

        # Stitch last image once loop finished
        stitchImage(imageData, outputPath, currentScreenshotID)



def stitchImage(imageParts, outputPath, currentScreenshotID):
    # Get Information about image package
    image :Image = Image.open(imageParts[0][0])
    (width, height) = image.size
    image.close()

    maxX :int = 0
    maxY :int = 0
    # find out max x and max y
    for entry in imageParts:
        maxX = max(maxX, int(entry[1][0]))
        maxY = max(maxY, int(entry[1][1]))

    #print(f"Max X Coord: {maxX} ")
    #print(f"Max Y Coord: {maxY} ")

    imageWidth = width * int(maxY) + width
    imageHeight = height * int(maxX) + height
    sizeTouple = (imageWidth, imageHeight)

    #print(f"Target Image Size: {sizeTouple}")

    # Stitch
    stitched = Image.new('RGB', sizeTouple)
    for entry in imageParts:
        image :Image = Image.open(entry[0])
        # print(f"Putting Image {entry[1][0]}, {entry[1][1]}")
        x = int(entry[1][0]) * width
        y = int(entry[1][1]) * height

        #print(f"Putting Picture {x}, {y}")
        stitched.paste(im= image, box=(x, y))
        image.close()
            

    stitched.save(outputPath + "\\" + currentScreenshotID + ".png", "PNG")

if __name__ == "__main__":
    main()