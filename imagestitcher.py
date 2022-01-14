from multiprocessing import Process
from tkinter.constants import HORIZONTAL
from PIL import Image
import os
import re
import tkinter as tk
from tkinter import Entry, Tk, filedialog, ttk
import threading

def main():
    root = tk.Tk()
    root.title("Factorio Stitcher")

    canvas = tk.Canvas(root) #, width=600, height=300)
    canvas.grid(columnspan=3)

    # Description
    description_label = tk.Label(root, text="Please select the Input and Output folder to start processing the images.")
    description_label.grid(columnspan=3,row=0)

    # Input Folder
    input_label = tk.Label(root, text="Input Folder")
    input_label.grid(column=0, row=1)
    input_desc = tk.Entry(root, text="Input Path")
    input_desc.grid(column=1, row=1)
    input_button = tk.Button(root, text="Browse", command= lambda: selectFolder("Select Input Folder", input_desc))
    input_button.grid(column=2, row=1)

    # Output Folder
    output_label = tk.Label(root, text="Output Folder")
    output_label.grid(column=0, row=2)
    output_desc = tk.Entry(root, text="Output Path")
    output_desc.grid(column=1, row=2)
    output_button = tk.Button(root, text="Browse", command= lambda: selectFolder("Select Output Folder", output_desc))
    output_button.grid(column=2, row=2)

    # Max Process Counts
    processCount_label = tk.Label(root, text="Max Parallel Process Count")
    processCount_label.grid(column=0, row=3)
    processCount_scale = tk.Scale(root, from_=1, to=16, orient=HORIZONTAL)
    processCount_scale.grid(column=1, columnspan=2, row=3)

    #totalFileCount
    progress_label = tk.Label(root, text=)

    progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="determinate")
    progress_bar.grid(column=0, columnspan=3, row=5)

    # Process Button
    process_button = tk.Button(root, text="Start Stitching", command= lambda: startStitcher(root, progress_bar))
    process_button.grid(column=0 , columnspan=3, row=4)    
    
    # Start GUI
    root.mainloop()

# ================= GUI Functions =================

def quit_application(root :Tk):
    print("Quitting!")
    root.quit()
    root.destroy()

def selectFolder(windowTitle: str, e: Entry):
    folder = filedialog.askdirectory(initialdir="", title=windowTitle)
    e.insert(0, folder)
    print("Selected Folder: ", folder)

# ================= Main Program =================

def startStitcher(root :Tk, progressbar):
    print("Starting Factorio Image Stitcher!")
    #inputPath = r".\input"
    inputPath = r".\input" #D:\Filme\Factorio\Raw"
    outputPath = r".\output"
    #path = r"C:\Users\nma\AppData\Roaming\Factorio\script-output\screenshots\3270616413\auto_split_nauvis"

    pattern = re.compile(r"screenshot(\d*)_x(\d*)_y(\d*).png")

    processCount = 8
    processes = []

    currentScreenshotID :str = ""

    totalFileCount = 0
    processedFiles = 0
    progressbar["value"] = 0
    


    # Get Total File Count of folder
    with os.scandir(inputPath) as it:
        totalFileCount = sum(1 for _ in it)

    progressbar["maximum"]=totalFileCount

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
                
            processedFiles += 1
            progressbar['value'] = processedFiles

            imageData.append([inputPath + r"\\" + fileName, coords])
            root.update_idletasks()

        for process in processes:
            process.join()

        # Stitch last image once loop finished
        stitchImage(imageData, outputPath, currentScreenshotID)

        print("Finished Stitching!")



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