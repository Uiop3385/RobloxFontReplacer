import os
import shutil
import datetime
import traceback
import webbrowser
import requests
import tkinter as tk
import base64
import sys
import threading
from tkinter import filedialog, messagebox, Label
from tkinter import ttk
from tkinter.font import Font
from tkextrafont import Font as CFont
from ttkthemes import themed_tk, ThemedStyle
class App:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False,False)
        self.root.title("Roblox Font Replacer by Uiop3385")

        # Set instance variables
        self.selected_font = ""
        self.selected_folder = ""
        self.log_file = None
        self.version = "1.3"
        self.font_path = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.excluded_fonts = []

        # Styling and stuff
        font = CFont(file = "data/fonts/Roboto-Regular.ttf", family = "Roboto", size=12)
        ttk.Style().configure("varela.TCheckbutton", font = Font(family = "Roboto", size = 12))
        style = ThemedStyle(root)
        style.theme_use("arc")
      
        # Create widgets
        
        select_font_button = ttk.Button(text="Select Replacement Font", command=self.select_font)
        select_folder_button = ttk.Button(text="Select content Folder", command=self.select_folder)
        replace_fonts_button = ttk.Button(text="Replace Fonts", command=self.replace_fonts)
        self.logging_checkbox = ttk.Checkbutton(self.root, text="Enable logging", style="varela.TCheckbutton", command=self.toggle_logging)
        self.logging_checkbox.state(['!alternate'])
        self.progress = ttk.Progressbar(orient="horizontal", length=200, mode="determinate")
        revert_button = ttk.Button(root, text="Revert from Backup", command=self.revert_from_backup)
        delete_backups_button = ttk.Button(root, text="Clear Backups", command=self.remove_backups)
        exceptions_button = ttk.Button(root, text = "Exclusions", command = self.exceptions)
        view_excluded_button = ttk.Button(root, text = "View Excluded Fonts", command = self.view_exceptions)
        remove_exclusions_button = ttk.Button(root, text = "Change Excluded Fonts", command = self.remove_exceptions)

        # Create labels
        me = Label(self.root, text="Made by Uiop3385", font = Font(family = "Roboto", size = 7))
        self.running = Label(self.root, text = f"You're currently running version {self.version}", font = Font(family = "Roboto", size = 7))
        text = Label(self.root, text="Welcome to Roblox Font Replacer!", font = Font(family = "Roboto", size = 11), pady = 10)
        self.progress_label = Label(self.root, text="Progress: 0/??", font = Font(family = "Roboto", size = 12), pady = 5)
        self.selected_font_label = Label(self.root, text = f"Selected : {self.font_path.get()}", font = Font(family = "Roboto", size = 8), pady = 5)
        self.selected_folder_label = Label(self.root, text = f"Selected : {self.folder_path.get()}", font = Font(family = "Roboto", size = 8), pady = 5)
        font_replacer = Label(self.root, text="Replace fonts :", font = Font(family = "Roboto", size = 11), pady = 5)
        backup_reverter = Label(self.root, text="Backups :", font = Font(family = "Roboto", size = 11), pady = 5)
        exceptions = Label(self.root, text="Exclusions :", font = Font(family = "Roboto", size = 10))
        frame_top = ttk.Frame(root, height=2, relief=tk.SUNKEN)
        mini_frame_top = ttk.Frame(root, height=2, relief=tk.SUNKEN)
        mini_frame_middle = ttk.Frame(root, height=2, relief=tk.SUNKEN)
        mini_frame_bottom = ttk.Frame(root, height=2, relief=tk.SUNKEN)
        frame_middle = ttk.Frame(root, height=2, relief=tk.SUNKEN)
        frame_bottom = ttk.Frame(root, height=2, relief=tk.SUNKEN)

        # Lay out widgets
        text.pack(side = "top")
        frame_top.pack(fill=tk.X, padx = 15)
        font_replacer.pack(side = "top")
        select_font_button.pack(side = "top")
        self.selected_font_label.pack(side = "top")
        mini_frame_top.pack(fill=tk.X, padx = 60, pady = 5)
        select_folder_button.pack(side = "top")
        self.selected_folder_label.pack(side = "top")
        mini_frame_middle.pack(fill=tk.X, padx = 60, pady = 5)
        exceptions.pack(side = "top")
        exceptions_button.pack(side = "top", pady = 5)
        view_excluded_button.pack(side = "top")
        remove_exclusions_button.pack(side = "top", pady = 5)
        mini_frame_bottom.pack(fill=tk.X, padx = 60, pady = 5)
        replace_fonts_button.pack(side = "top", pady = 5)
        self.logging_checkbox.pack(side = "top")
        self.progress.pack(side = "top", pady = 5)
        self.progress_label.pack(side = "top")
        self.running.pack(side = "bottom")
        frame_middle.pack(fill=tk.X, padx = 15)
        backup_reverter.pack(side = "top")
        me.pack(side = "bottom")
        frame_bottom.pack(fill=tk.X, padx = 15, pady = 5, side = "bottom")
        revert_button.pack(side = "bottom", pady = 5)
        delete_backups_button.pack(side = "bottom")

    def select_font(self):
        # Prompts the user to select a font
        self.selected_font = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf;*.otf")], title = "Select a replacement font")
        self.font_path.set({self.selected_font})
        self.selected_font_label.config(text=f"Selected : {self.font_path.get()}")
      
    def select_folder(self):
        # Prompts the user to select a folder
        self.selected_folder = filedialog.askdirectory(title = "Select your Roblox contents folder")
        self.folder_path.set({self.selected_folder})
        self.selected_folder_label.config(text=f"Selected : {self.folder_path.get()}")

    def quit(self):
        sys.exit()
  
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
        self.quit()

    def revert_from_backup(self):
        global backup_window
        messagebox.showinfo("Backup", "You will be prompted to select your backup folder, after which you will be prompted to choose the contents folder you would like to revert.")
        self.backup_folder = filedialog.askdirectory(initialdir=os.path.join(os.getcwd(), "backups"), title="Select Backup Folder")
        self.contents_folder = filedialog.askdirectory(title="Select contents folder to overwrite")
        if self.backup_folder:
            try:
                backup_window = tk.Tk()
                backup_window.title("Working on it...")
                backup_window.geometry("100x10")
                style = ThemedStyle(backup_window)
                style.theme_use("arc")
                self.progress = ttk.Progressbar(backup_window, mode="indeterminate")
                self.progress.pack()
                self.progress.start()
                thread = threading.Thread(target=self.backup)
                thread.start()
                backup_window.after(100, lambda: self.check_thread(thread, self.progress, backup_window))
                backup_window.mainloop()
            except Exception as e:
                backup_window.destroy()
                messagebox.showerror("Exception", "An error occured when reverting. Please try again, and make sure you've selected the proper folders.")

    def check_thread(self, thread, progress, backup_window):
        if thread.is_alive():
            backup_window.after(100, lambda: self.check_thread(thread, progress, backup_window))
        else:
            self.progress.stop()
            self.progress.pack_forget()
            backup_window.destroy()
            messagebox.showinfo("Success!", "The revert was successful.")

    def backup(self):
        try:
            global backup_window
            shutil.copytree(self.backup_folder, self.contents_folder, dirs_exist_ok=True)
        except Exception as e:
            backup_window.destroy()
            messagebox.showerror("Exception", "An error occured when reverting. Please try again, and make sure you've selected the proper folders.")

    def remove_backups(self):
        result = messagebox.askyesno("Warning", "Are you sure you want to remove all backups? This is irreversible!")
        if result:
            try:
                messagebox.showinfo("Preparing to delete", "The backups will now be deleted. Expect a few seconds of unresponsiveness.")
                backups_folder = "backups"
                shutil.rmtree(backups_folder)
                os.mkdir("backups")
                messagebox.showinfo("Success", "The backups have been cleared.")
            except Exception as e:
                messagebox.showerror("Exception", "An error occured when deleting. Please try again, and if it still does not work, delete the backups folder manually.")
        else:
            messagebox.showinfo("Cancelled", "The operation was cancelled.")

    def exceptions(self):
        # Check if content folder has been selected
        if self.selected_folder == "":
            messagebox.showerror("Error", "Please select the content folder.")
            return

        # Create a new window for the exceptions function
        exceptions_window = tk.Tk()
        exceptions_window.resizable(False,False)
        exceptions_window.title("Select exceptions")
        style = ThemedStyle(exceptions_window)
        style.theme_use("arc")

        # String explaining the function
        Label(exceptions_window, text="Select the fonts you want to exclude from the replacement :").pack(pady = 5)

        # List to display all the fonts that passed the check
        font_list = tk.Listbox(exceptions_window, selectmode="extended")

        # Get all the fonts in the content/fonts folder and ignore the exceptions
        try:
            fonts = os.listdir(os.path.join(self.selected_folder, "fonts"))
            exceptions = ["RobloxEmoji.ttf", "TwemojiMozilla.ttf", "gamecontrollerdb.txt"]
            for font in fonts:
                if os.path.isfile(os.path.join(self.selected_folder, "fonts", font)) and font not in exceptions:
                    font_list.insert(tk.END, font)
        except Exception as e:
            exceptions_window.destroy()
            messagebox.showerror("Exception", "An error has occured loading the fonts. You may have selected an incorrect folder.")

        def search_fonts(event=None):
            try:
                search_term = search_bar.get()
                filtered_fonts = list(filter(lambda x: search_term in x, fonts))
                font_list.delete(0, tk.END)
                for font in filtered_fonts:
                    font_list.insert(tk.END, font)
            except Exception as e:
                exceptions_window.destroy()
                messagebox.showerror("Exception", "An error has occured searching for fonts. Try again.")

        def on_focus_out(event, entry):
            if not entry.get():
                entry.insert(0, "Search (Caps Sensitive!)")

        def on_focus_in(event, entry):
            if entry.get() == "Search (Caps Sensitive!)":
                entry.delete(0, tk.END)

        # Search bar
        search_bar = ttk.Entry(exceptions_window, width = 25)
        search_bar.pack(pady = 5)
        search_bar.insert(0, "Search (Caps Sensitive!)")
        search_bar.bind("<FocusOut>", lambda event: on_focus_out(event, search_bar))
        search_bar.bind("<FocusIn>", lambda event: on_focus_in(event, search_bar))
        search_bar.bind("<KeyRelease>", search_fonts)

        font_list.pack()

        # Confirm button to save the changes
        def confirm():
            try:
                for index in font_list.curselection():
                    self.excluded_fonts.append(font_list.get(index))
                messagebox.showinfo("Info", f"The following fonts will not be replaced : {self.excluded_fonts}")
                exceptions_window.destroy()
            except Exception as e:
                exceptions_window.destroy()
                messagebox.showerror("Exception", "An error occured while confirming changes. Please try again.")

        confirm_button = ttk.Button(exceptions_window, text="Confirm", command=confirm)
        confirm_button.pack(pady = 5)

        exceptions_window.mainloop()

    def view_exceptions(self):
        if self.excluded_fonts:
            messagebox.showinfo("Exclusions selected", f"The following fonts will be excluded from the next replacement : {self.excluded_fonts}")
        else:
            messagebox.showwarning("No exclusions selected", "You have not yet chosen any fonts to exclude. You can exclude fonts by pressing the 'Exclusions' button.")

    def remove_exceptions(self):
        # Check if there are excluded fonts
        if not self.excluded_fonts:
            messagebox.showwarning("No exclusions selected", "You have not yet chosen any fonts to exclude. You can exclude fonts by pressing the 'Exclusions' button.")
            return

        # Create a new window for the exceptions function
        remove_exceptions_window = tk.Tk()
        remove_exceptions_window.resizable(False,False)
        remove_exceptions_window.title("Remove exceptions")
        style = ThemedStyle(remove_exceptions_window)
        style.theme_use("arc")

        # String explaining the function
        Label(remove_exceptions_window, text="Select the fonts you want to remove from your list of exclusions :").pack(pady = 5)

        # List to display all the excluded fonts
        font_list = tk.Listbox(remove_exceptions_window, selectmode="extended")

        # Get all the excluded fonts
        try:
            fonts = self.excluded_fonts
            for font in fonts:
                font_list.insert(tk.END, font)
        except Exception as e:
            remove_exceptions_window.destroy()
            messagebox.showerror("Exception", "An error has occured loading the fonts. You may have selected an incorrect folder.")

        def search_fonts(event=None):
            try:
                search_term = search_bar.get()
                filtered_fonts = list(filter(lambda x: search_term in x, fonts))
                font_list.delete(0, tk.END)
                for font in filtered_fonts:
                    font_list.insert(tk.END, font)
            except Exception as e:
                remove_exceptions_window.destroy()
                messagebox.showerror("Exception", "An error has occured searching for fonts. Try again.")

        def on_focus_out(event, entry):
            if not entry.get():
                entry.insert(0, "Search (Caps Sensitive!)")

        def on_focus_in(event, entry):
            if entry.get() == "Search (Caps Sensitive!)":
                entry.delete(0, tk.END)

        # Search bar
        search_bar = ttk.Entry(remove_exceptions_window, width = 25)
        search_bar.pack(pady = 5)
        search_bar.insert(0, "Search (Caps Sensitive!)")
        search_bar.bind("<FocusOut>", lambda event: on_focus_out(event, search_bar))
        search_bar.bind("<FocusIn>", lambda event: on_focus_in(event, search_bar))
        search_bar.bind("<KeyRelease>", search_fonts)

        font_list.pack()

        # Confirm button to save the changes
        def confirm():
            try:
                unexcluded_fonts = []
                for index in font_list.curselection():
                    self.excluded_fonts.remove(font_list.get(index))
                    unexcluded_fonts.append(font_list.get(index))
                messagebox.showinfo("Info", f"The following fonts will still be excluded : {self.excluded_fonts}, and the following fonts will no longer be excluded : {unexcluded_fonts}")
                remove_exceptions_window.destroy()
            except Exception as e:
                remove_exceptions_window.destroy()
                messagebox.showerror("Exception", "An error occured while confirming changes. Please try again.")

        confirm_button = ttk.Button(remove_exceptions_window, text="Confirm", command=confirm)
        confirm_button.pack(pady = 5)

        remove_exceptions_window.mainloop()

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
            if self.new_version != self.version:
                yes = "yes"
            else:
                yes = "no"
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
                self.log(base64.b64encode("Process ended with status code 400".encode("utf-8")))
                messagebox.showerror("Exception", "An exception has occured and replacement could not start.\nYou've most likely chosen the wrong folder, please try again with the correct one.\nIf the issue persists, even with the correct folder, try again with logging enabled.\nPlease forward us this log via a GitHub issue with tag Exception.\nWe're sorry!")
                return

            messagebox.showwarning("Disclaimer", "Roblox Font Replacer does not take responsibility for any issues encountered while using the program, or after using the program. If you disagree, or prefer not to take any risks, then please exit now.")
    
            result = messagebox.askyesno("Save Backup", "Would you like to save a backup of your contents folder?")
            if result:
                try:
                    now = datetime.datetime.now()
                    messagebox.showinfo("Preparing to save", "Your backup will now be saved. Expect a few seconds of unresponsiveness. If nothing happens after 5 seconds, try clicking on the program.")
                    shutil.copytree(self.selected_folder, f"backups/contents_backup_{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}")
                    messagebox.showinfo("Success", "Backup saved successfully. Replacement will now begin.")
                except Exception as e:
                    self.log(base64.b64encode("Backup error : {}".format(e).encode("utf-8")))
                    traceback.print_exc()
                    messagebox.showerror("Exception", "An error occured when saving the backup. The program will ignore this error and start replacing the fonts. If you'd like to cancel this process, please close the program.")
            else:
                messagebox.showinfo("Cancelled", "Backup not saved")

            # Update the progress bar to show the number of fonts
            self.progress["maximum"] = len(fonts)
    
            self.log(base64.b64encode("Starting font replacement process.".encode("utf-8")))
    
            # Replace each font
            for i, font in enumerate(fonts):
                try:
                    # Check if the font is one of the three that should be kept
                    if font in ["RobloxEmoji.ttf", "TwemojiMozilla.ttf", "gamecontrollerdb.txt"]:
                        self.log(base64.b64encode("Protected file skipped : {}".format(font).encode("utf-8")))
                        continue

                    # Check if the font has been excluded
                    if font in self.excluded_fonts:
                        self.log(base64.b64encode("Excluded file skipped : {}".format(font).encode("utf-8")))
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
                print(self.progress["value"])
                self.progress_label["text"] = f"Progress: {i+1}/{len(fonts)}"
                self.root.update()

        # Reset the progress bar
        self.progress["value"] = 0

        self.log(base64.b64encode("Process ended with status code 200".encode("utf-8")))

        # Show a message box thanking the user for using the program
        messagebox.showinfo("Done", "Fonts replaced successfully! Thank you for using Roblox Font Replacer. Exceptions have been reset.")
        self.excluded_fonts = []

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
