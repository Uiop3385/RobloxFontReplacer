import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Label
from tkinter import ttk
from tkinter.font import Font
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Font Replacer by Uiop3385")

        font = Font(family="Comic Sans MS", size=12)
        # Create widgets
        select_font_button = tk.Button(text="Select Replacement Font", command=self.select_font, font = font)
        select_folder_button = tk.Button(text="Select contents Folder", command=self.select_folder, font = font)
        replace_fonts_button = tk.Button(text="Replace Fonts", command=self.replace_fonts, font = font)
        self.progress = ttk.Progressbar(orient="horizontal", length=200, mode="determinate")

        #Create labels
        me = Label(self.root, text="Made by Uiop3385", font = ("Comic Sans MS", 7), pady = 5)
        text = Label(self.root, text="Welcome to Roblox Font Replacer!", font = ("Comic Sans MS", 10), pady = 10)
        self.progress_label = Label(self.root, text="Progress: 0/64", font= ("Comic Sans MS", 12), pady = 5)

        # Lay out widgets
        text.pack(side = "top")
        select_font_button.pack(side = "top")
        select_folder_button.pack(side = "top")
        replace_fonts_button.pack(side = "top")
        self.progress.pack(side = "top")
        self.progress_label.pack(side = "top")
        me.pack(side = "bottom")

        # Set instance variables
        self.selected_font = ""
        self.selected_folder = ""

    def select_font(self):
        self.selected_font = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf;*.otf")])

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()

    def replace_fonts(self):
        if not self.selected_font:
            messagebox.showerror("Error", "No font selected")
            return
        if not self.selected_folder:
            messagebox.showerror("Error", "No folder selected")
            return

        # Get the font folder and make a list of all the fonts in it
        font_folder = os.path.join(self.selected_folder, "fonts")
        fonts = os.listdir(font_folder)

        # Update the progress bar to show the number of fonts
        self.progress["maximum"] = len(fonts)

        # Replace each font
        for i, font in enumerate(fonts):
            # Check if the font is one of the two that should be kept
            if font in ["RobloxEmoji.ttf", "TwemojiMozilla.ttf"]:
                continue

            # Get the file extension of the selected font
            new_font_ext = os.path.splitext(self.selected_font)[1]

            # Make a copy of the selected font and move it to the font folder
            copy_path = os.path.join(font_folder, "temp" + new_font_ext)
            shutil.copy(self.selected_font, copy_path)

            # Get the file extension and name of the current font
            old_font_path = os.path.join(font_folder, font)
            old_font_ext = os.path.splitext(old_font_path)[1]
            old_font_name = os.path.splitext(font)[0]

            # Rename the copied font with the same name as the current font
            new_font_name = old_font_name + new_font_ext
            new_font_path = os.path.join(font_folder, new_font_name)
            shutil.move(copy_path, new_font_path)

            # Replace the current font with the selected font
            if os.path.isdir(old_font_path):
               # old_font_path is a directory, do not rename it
               print("Skipping directory:", old_font_path)
            else:
               # old_font_path is a file, rename it
               os.replace(new_font_path, old_font_path)

            # Update the progress bar and label
            self.progress["value"] = i + 1
            self.progress_label["text"] = f"Progress: {i+1}/{len(fonts)}"
            self.root.update()

        # Reset the progress bar
        self.progress["value"] = 0

        # Show a message box thanking the user for using the program
        messagebox.showinfo("Done", "Fonts replaced successfully! Thank you for using the program.")
        quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

