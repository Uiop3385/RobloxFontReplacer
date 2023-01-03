import os
import shutil
import datetime
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, Label
from tkinter import ttk
from tkinter.font import Font
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Font Replacer by Uiop3385")

        # Styling and stuff
        font = Font(family="Comic Sans MS", size=12)
        ttk.Style().configure("comicsans.TCheckbutton", font=font)
        ttk.Style().theme_use("winnative")
        self.font_path = tk.StringVar()
        self.folder_path = tk.StringVar()
      
        # Create widgets
        select_font_button = tk.Button(text="Select Replacement Font", command=self.select_font, font = font)
        select_folder_button = tk.Button(text="Select contents Folder", command=self.select_folder, font = font)
        replace_fonts_button = tk.Button(text="Replace Fonts", command=self.replace_fonts, font = font)
        self.logging_checkbox = ttk.Checkbutton(self.root, text="Enable logging", style="comicsans.TCheckbutton", command=self.toggle_logging)
        self.logging_checkbox.state(['!alternate'])
        self.progress = ttk.Progressbar(orient="horizontal", length=200, mode="determinate")

        # Create labels
        me = Label(self.root, text="Made by Uiop3385", font = ("Comic Sans MS", 7), pady = 5)
        text = Label(self.root, text="Welcome to Roblox Font Replacer!", font = ("Comic Sans MS", 10), pady = 10)
        self.progress_label = Label(self.root, text="Progress: 0/64", font = ("Comic Sans MS", 12), pady = 5)
        self.selected_font_label = Label(self.root, text = f"Selected : {self.font_path.get()}", font = ("Comic Sans MS", 8), pady = 5)
        self.selected_folder_label = Label(self.root, text = f"Selected : {self.folder_path.get()}", font = ("Comic Sans MS", 8), pady = 5)
      
        # Lay out widgets
        text.pack(side = "top")
        select_font_button.pack(side = "top")
        self.selected_font_label.pack(side = "top")
        select_folder_button.pack(side = "top")
        self.selected_folder_label.pack(side = "top")
        replace_fonts_button.pack(side = "top")
        self.logging_checkbox.pack(side = "top")
        self.progress.pack(side = "top")
        self.progress_label.pack(side = "top")
        me.pack(side = "bottom")

        # Set instance variables
        self.selected_font = ""
        self.selected_folder = ""
        self.log_file = None

    def select_font(self):
        self.selected_font = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf;*.otf")])
        self.font_path.set({self.selected_font})
        self.selected_font_label.config(text=f"Selected : {self.font_path.get()}")
      
    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        self.folder_path.set({self.selected_folder})
        self.selected_folder_label.config(text=f"Selected : {self.folder_path.get()}")
  
    def toggle_logging(self):
        # Check if the checkbox is selected
        if self.logging_checkbox.instate(['selected']):
            # Create the log file with the current date and time
            now = datetime.datetime.now()
            log_filename = f"rfr-debug-log_{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}.log"
            self.log_file = open(log_filename, "w")
        else:
            # Close the log file
            self.log_file = None

    def log(self, message):
        # Check if logging is enabled
        if self.log_file is not None:
            now = datetime.datetime.now()

            # Format the log messages
            log_message = f"[{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}] {message}"
          
            # Write the message to the log file
            try:
                self.log_file.write(log_message + "\n")
                self.log_file.flush()
            except Exception as e:
                # Log the exception
                self.log_file.write(f"[{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}] Error: {e}\n")
                traceback.print_exc(file=self.log_file)
                self.log_file.flush()

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

        self.log("Starting font replacement process")

        # Replace each font
        for i, font in enumerate(fonts):
            # Check if the font is one of the two that should be kept
            if font in ["RobloxEmoji.ttf", "TwemojiMozilla.ttf", "gamecontrollerdb.txt"]:
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
               self.log(f"Skipping directory {old_font_path}")
            else:
               # old_font_path is a file, rename it
                try:
                    os.replace(new_font_path, old_font_path)
                    self.log(f"Replacing font {font} with {os.path.basename(self.selected_font)}")
                except Exception as e:
                    self.log(f"Error replacing font {font}: {e}")
                    traceback.print_exc()
                    return
            # Update the progress bar and label
            self.progress["value"] = i + 1
            self.progress_label["text"] = f"Progress: {i+1}/{len(fonts)}"
            self.root.update()

        # Reset the progress bar
        self.progress["value"] = 0

        # Show a message box thanking the user for using the program
        messagebox.showinfo("Done", "Fonts replaced successfully! Thank you for using Roblox Font Replacer.")
        quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

