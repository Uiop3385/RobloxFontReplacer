# Roblox Font Replacer
Roblox Font Replacer is a program developed in Python that allows users to easily replace their Roblox fonts to make customization easier.
This program and this guide were made for use on Windows ; because seriously, who does gaming on Mac.

# How to use :
**Keep the program open during the entire process.**

In order to use the program, you first need to select a replacement font. This is the font that will overwrite all other fonts in your Roblox fonts folder.
You can find them at DiskLetter://Windows/Fonts, or you can download a font online and use the file straight from your downloads.
**Make sure you copy the font over to another directory as the folder may not appear from the font selection menu.**
In the program, click "Select Replacement Font". Now, head to the directory you've put the font in and select it.

Now, you can move on to selecting your contents folder.

To find your folder location, go to your desktop, right click on the Roblox Player shortcut, and select "Open file location". On Windows 11 you may need to click on "Show more options" to see it.
You should arrive straight in the Roblox folder of the current installation. Double click on the path at the top of the file explorer and copy the path.
Now, in the program, click on "Select contents Folder", and at the top of the file explorer, double click the file path, delete everything and paste the path you obtained.
Finally, make sure you go inside the "content" folder, and click Select folder.
All you have to do is click Replace Fonts and the program will automatically overwrite all the fonts in your content folder and replace them with renamed copies of the font you selected.
Look at the progress bar or the "Progress" label to see how much left is to replace.
On modern computers, this process should take no more than a second to complete.
**You will need to repeat these steps everytime Roblox is updated, as the entire client is redownloaded and therefore the fonts aswell.**

Once finished, just join any Roblox game and you will see all fonts have been replaced, including on the Escape menu, disconnection messages, and even the app itself.

If for any reason the progress hangs, it might mean an error occured. To identify the error, please download the debug program, which should load with the console, and create an issue report on GitHub with a screenshot of the error. We'll look into it.
You can try and troubleshoot yourself, just try again and make sure you selected the proper folder/font path.

# Developement :

Everything is explained inside of main.py with comments. The program uses the following imports : tkinter for the UI, and a combination of os and shutil for the font replacement.

If you need any extra help, contact me on Discord at Uiop3385#4285 (ID : 611557419222302721)

You are free to do whatever you want with this program, as long as you keep original credit to me in the bottom label, for example, if you remake the program with more features, you can replace it with "Modified by [your_name], original by Uiop3385".


**Thanks for using Roblox Font Replacer!**
