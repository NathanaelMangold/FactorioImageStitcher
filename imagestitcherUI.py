import tkinter as tk
from tkinter import filedialog

root :tk.Tk

def setup_ui():
    global root
    root = tk.Tk()
    root.title("Factorio Image Stitcher")

    canvas = tk.Canvas(root)
    canvas.grid()

    # Info Label
    info_label = tk.Label(root, text="Please select output and input folder to start stitching!")
    info_label.grid(columnspan=2, column=0, row=0)

    # Input Folder Selection
    input_label = tk.Label(root, text="Input Folder")
    input_label.grid(column=0, row=1)
    input_desc = tk.Entry(root, text="Input Path")
    input_desc.grid(column=1, row=1)
    input_button = tk.Button(root, text="Browse", command= lambda: selectFolder("Select Input Folder", input_desc))
    input_button.grid(column=2, row=1)

# ================= GUI Functions =================
def selectFolder(windowTitle: str, e: tk.Entry):
    folder = filedialog.askdirectory(initialdir="", title=windowTitle)
    e.insert(0, folder)
    print("Selected Folder: ", folder)

# ================= Main Function =================
def main():
    global root
    setup_ui()
    root.mainloop()

if __name__ == "__main__":
    main()