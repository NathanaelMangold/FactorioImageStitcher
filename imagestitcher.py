from PIL import Image
import os

def main():
    print("Starting Factorio Image Stitcher!")
    path = r"C:\Users\nma\AppData\Roaming\Factorio\script-output\screenshots\3270616413\auto_split_nauvis"

    imageParts = []

    currentScreenshot :str = ""
    with os.scandir(path) as it:
        for entry in it:
            fileName :str = entry.name
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

                        result.save("C:\DEV\FactorioImageStitcher\output\ " + currentScreenshot + ".png")

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

if __name__ == "__main__":
    main()