import os
import shutil
import datetime
import traceback
import webbrowser
import requests
import tkinter as tk
import base64
from tkinter import filedialog, messagebox, Label
from tkinter import ttk
from tkinter.font import Font
from tkextrafont import Font as CFont
from ttkthemes import themed_tk, ThemedStyle
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Font Replacer by Uiop3385")

        # Set instance variables
        self.selected_font = ""
        self.selected_folder = ""
        self.log_file = None
        self.version = "1.1"
        self.font_path = tk.StringVar()
        self.folder_path = tk.StringVar()

        # Styling and stuff
        font = CFont(file="data/fonts/FredokaOne-Regular.ttf", family = "Fredoka One", size=12)
        ttk.Style().configure("fredoka.TCheckbutton", font = font)
        style = ThemedStyle(root)
        style.theme_use("arc")
      
        # Create widgets
        select_font_button = ttk.Button(text="Select Replacement Font", command=self.select_font)
        select_folder_button = ttk.Button(text="Select content Folder", command=self.select_folder)
        replace_fonts_button = ttk.Button(text="Replace Fonts", command=self.replace_fonts)
        self.logging_checkbox = ttk.Checkbutton(self.root, text="Enable logging", style="fredoka.TCheckbutton", command=self.toggle_logging)
        self.logging_checkbox.state(['!alternate'])
        self.progress = ttk.Progressbar(orient="horizontal", length=200, mode="determinate")

        # Create labels
        me = Label(self.root, text="Made by Uiop3385", font = Font(family = "Fredoka One", size = 7))
        self.running = Label(self.root, text = f"You're currently running version {self.version}", font = Font(family = "Fredoka One", size = 7))
        text = Label(self.root, text="Welcome to Roblox Font Replacer!", font = Font(family = "Fredoka One", size = 10), pady = 10)
        self.progress_label = Label(self.root, text="Progress: 0/64", font = Font(family = "Fredoka One", size = 12), pady = 5)
        self.selected_font_label = Label(self.root, text = f"Selected : {self.font_path.get()}", font = Font(family = "Fredoka One", size = 8), pady = 5)
        self.selected_folder_label = Label(self.root, text = f"Selected : {self.folder_path.get()}", font = Font(family = "Fredoka One", size = 8), pady = 5)
      
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
        self.running.pack(side = "bottom")
        me.pack(side = "bottom")

    def select_font(self):
        # Prompts the user to select a font
        self.selected_font = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf;*.otf")])
        self.font_path.set({self.selected_font})
        self.selected_font_label.config(text=f"Selected : {self.font_path.get()}")
      
    def select_folder(self):
        # Prompts the user to select a folder
        self.selected_folder = filedialog.askdirectory()
        self.folder_path.set({self.selected_folder})
        self.selected_folder_label.config(text=f"Selected : {self.folder_path.get()}")
  
    def toggle_logging(self):
        # Check if the checkbox is selected
        if self.logging_checkbox.instate(['selected']):
            # Create the log file with the current date and time
            now = datetime.datetime.now()
            log_filename = f"rfr-debug-log_{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}.log"
            self.log_file = open("logs/"+log_filename, "w")
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

    def on_yes_clicked(self):
        # Load, open, and log the link, then close the program
        link = "https://github.com/Uiop3385/RobloxFontReplacer/releases/tag/" + self.new_version
        webbrowser.open_new(link)
        self.log(base64.b64encode("GitHub update link opened, ending program : {}".format(link).encode("utf-8")))
        quit()
  
    def replace_fonts(self):
        # First line of error prevention
        if not self.selected_font:
            messagebox.showerror("Error", "No font selected")
            self.log(base64.b64encode("No font selected error displayed".encode("utf-8")))
            return
        if not self.selected_folder:
            messagebox.showerror("Error", "No folder selected")
            self.log(base64.b64encode("No folder selected error displayed".encode("utf-8")))
            return

        # Checking for updates
        try:
            response = requests.get("https://api.github.com/repos/Uiop3385/RobloxFontReplacer/releases/latest")
            self.new_version = response.json()["tag_name"]
            yes = "yes"
        except Exception as e:
            self.log(base64.b64encode("Could not connect, update check aborted, error : {}".format(e).encode("utf-8")))
            yes = "no"
        finally:
            if yes == "yes":
                result = messagebox.askyesno("Update available!", "There's a new update available on GitHub. Do you want to continue to the download page?")
                if result:
                    self.on_yes_clicked()
                else:
                    self.log(base64.b64encode("GitHub update denied, continuing with program.".encode("utf-8")))

            try:
                 # Get the font folder and make a list of all the fonts in it
                font_folder = os.path.join(self.selected_folder, "fonts")
                fonts = os.listdir(font_folder)
            except Exception as e:
                self.log(base64.b64encode("Detection error : {}".format(e).encode("utf-8")))
                traceback.print_exc()
                self.log("Process ended with status code 400")
                self.log(base64.b64encode("Process ended with status code 400".encode("utf-8")))
                messagebox.showerror("Exception", "An exception has occured and replacement could not start.\nYou've most likely chosen the wrong folder, please try again with the correct one.\nIf the issue persists, even with the correct folder, try again with logging enabled.\nPlease forward us this log via a GitHub issue with tag Exception.\nWe're sorry!")
                return
    
            # Update the progress bar to show the number of fonts
            self.progress["maximum"] = len(fonts)
    
            self.log(base64.b64encode("Starting font replacement process.".encode("utf-8")))
    
            # Replace each font
            for i, font in enumerate(fonts):
                try:
                    # Check if the font is one of the two that should be kept
                    if font in ["RobloxEmoji.ttf", "TwemojiMozilla.ttf", "gamecontrollerdb.txt"]:
                        self.log(base64.b64encode("Protected file skipped : {}".format(font).encode("utf-8")))
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
                       print("Skipping directory :", old_font_path)
                       self.log(base64.b64encode("Skipping directory {}".format(old_font_path).encode("utf-8")))
                    else:
                       # old_font_path is a file, rename it
                        try:
                            os.replace(new_font_path, old_font_path)
                            self.log(base64.b64encode("Replacing font {} with {}".format(font, os.path.basename(self.selected_font)).encode("utf-8")))
                        except Exception as e:
                            self.log(base64.b64encode("Error replacing font {} : {}".format(font, e).encode("utf-8")))
                            traceback.print_exc()
                            return
                except Exception as e:
                  self.log(base64.b64encode("Global error with font {} : {}".format(font, e).encode("utf-8")))
                  traceback.print_exc()
                  self.log(base64.b64encode("Process ended with status code 400".encode("utf-8")))
                  messagebox.showerror("Exception", "A fatal exception has occured and the replacement process has been aborted.\nPlease try again with logging enabled.\nIf it still does not work, create a GitHub issue with the tag Exception, and provide us with the log.\nSorry!")
                  return
                # Update the progress bar and label
                self.progress["value"] = i + 1
                self.progress_label["text"] = f"Progress: {i+1}/{len(fonts)}"
                self.root.update()

        # Reset the progress bar
        self.progress["value"] = 0

        self.log(base64.b64encode("Process ended with status code 200".encode("utf-8")))

        # Show a message box thanking the user for using the program
        messagebox.showinfo("Done", "Fonts replaced successfully! Thank you for using Roblox Font Replacer.")
        quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

