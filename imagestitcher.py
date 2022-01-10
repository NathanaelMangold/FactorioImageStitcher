from PIL import Image
import os
import re

def main():
    print("Starting Factorio Image Stitcher!")
    inputPath = r".\input"
    outputPath = r".\output"
    #path = r"C:\Users\nma\AppData\Roaming\Factorio\script-output\screenshots\3270616413\auto_split_nauvis"

    pattern = re.compile(r"screenshot(\d*)_x(\d*)_y(\d*).png")

    currentScreenshotID :str = ""
    # Image File, (x,y)
    imageParts = []

    with os.scandir(inputPath) as it:
        for entry in it:
            fileName :str = entry.name

            match = pattern.match(fileName)
            if match is None:
                print(f"File: '{fileName}' is not a valid screenshot!")
                continue

            print(f"ID: {match.group(1)} | x: {match.group(2)} | y: {match.group(3)} ")

            screenshotID = match.group(1)
            coords = (match.group(2), match.group(3))

            if(not currentScreenshotID):
                currentScreenshotID = screenshotID

            if(screenshotID != currentScreenshotID):
                (width, height) = imageParts[0][0].size
                maxX = 0
                maxY = 0
                # find out max x and max y
                for entry in imageParts:
                    maxX = max(entry[1][0])
                    maxY = max(entry[1][1])

                #print(f"Max X Coord: {maxX} ")
                #print(f"Max Y Coord: {maxY} ")

                imageWidth = width * int(maxY)
                imageHeight = height * int(maxX)
                sizeTouple = (imageWidth, imageHeight)
                # Stitch
                stitched = Image.new('RGB', sizeTouple)
                for entry in imageParts:
                    image :Image = entry[0]
                    x = int(entry[1][0]) * width
                    y = int(entry[1][1]) * height
                    #print(f"Putting Picture {x}, {y}")
                    stitched.paste(im= image, box=(x, y))
                        

                stitched.save(outputPath + "\\" + currentScreenshotID + ".png")

                # Close all Images
                for entry in imageParts:
                    image :Image = entry[0]
                    image.close()

                imageParts.clear()

                currentScreenshotID = screenshotID
            else:
                image = Image.open(inputPath + r"\\" + fileName)
                imageParts.append([image, coords])





            continue
            if not fileName.startswith('.') and entry.is_file() and fileName.endswith(".png"):
                if currentScreenshot != fileName.split("_")[0]:
                    currentScreenshot = fileName.split("_")[0]

                    if currentScreenshot != "" and len(imageParts) > 1:
                        image1 :Image = imageParts[0]
                        image2 :Image = imageParts[1]

                        (width1, height1) = image1.size
                        (width2, height2) = image2.size

                        result_width = width1 + width2
                        result_height = max(height1, height2)

                        result = Image.new('RGB', (result_width, result_height))
                        result.paste(im=image1, box=(0, 0))
                        result.paste(im=image2, box=(width1, 0))

                        result.save(".\output\ " + currentScreenshot + ".png")

                        print("Stitched:")
                        print(image1.filename)
                        print(image2.filename)
                        imageParts.clear()

                if currentScreenshot != "":
                    imageParts.append(Image.open(path + r"\\" + fileName))

    #image1 = Image.open(file1)
    #image2 = Image.open(file2)

    #(width1, height1) = image1.size
    #(width2, height2) = image2.size

    #result_width = width1 + width2
    #result_height = max(height1, height2)

    #result = Image.new('RGB', (result_width, result_height))
    #result.paste(im=image1, box=(0, 0))
    #result.paste(im=image2, box=(width1, 0))
                    


    #print(path)
    #[entry for entry in os.scandir('.') if entry.is_file()]

def stitchImage():
    pass

if __name__ == "__main__":
    main()