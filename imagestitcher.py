from PIL import Image
import os
import re

def main():
    print("Starting Factorio Image Stitcher!")
    #inputPath = r".\input"
    inputPath = r"D:\Filme\Factorio\Raw"
    outputPath = r".\output"
    #path = r"C:\Users\nma\AppData\Roaming\Factorio\script-output\screenshots\3270616413\auto_split_nauvis"

    pattern = re.compile(r"screenshot(\d*)_x(\d*)_y(\d*).png")

    currentScreenshotID :str = ""
    # Image File, (x,y)
    imageParts = []

    totalFileCount = 0
    processedFiles = 0

    # Get Total File Count of folder
    with os.scandir(inputPath) as it:
        totalFileCount = sum(1 for _ in it)

    with os.scandir(inputPath) as it:
        for entry in it:
            fileName :str = entry.name

            match = pattern.match(fileName)
            if match is None:
                print(f"File: '{fileName}' is not a valid screenshot!")
                continue

            #print(f"ID: {match.group(1)} | x: {match.group(2)} | y: {match.group(3)} ")

            screenshotID = match.group(1)
            coords = (match.group(2), match.group(3))

            if(not currentScreenshotID):
                currentScreenshotID = screenshotID

            if(screenshotID != currentScreenshotID):
                stitchImage(imageParts, outputPath, currentScreenshotID)
                imageParts.clear()
                currentScreenshotID = screenshotID

                print(f"Progress: {processedFiles}/{totalFileCount}")

            image = Image.open(inputPath + r"\\" + fileName)
            imageParts.append([image, coords])

            processedFiles += 1
        
        stitchImage(imageParts, outputPath, currentScreenshotID)

def stitchImage(imageParts, outputPath, currentScreenshotID):
    (width, height) = imageParts[0][0].size
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
        image :Image = entry[0]
       # print(f"Putting Image {entry[1][0]}, {entry[1][1]}")
        x = int(entry[1][0]) * width
        y = int(entry[1][1]) * height

        #print(f"Putting Picture {x}, {y}")
        stitched.paste(im= image, box=(x, y))
            

    stitched.save(outputPath + "\\" + currentScreenshotID + ".png", "PNG")

    # Close all Images
    for entry in imageParts:
        image :Image = entry[0]
        image.close()


if __name__ == "__main__":
    main()