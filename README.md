# Roblox Font Replacer
Roblox Font Replacer is a program developed in Python that allows users to easily replace their Roblox fonts to make customization easier.
This program and this guide were made for use on Windows ; because seriously, who does gaming on Mac.

**RFR is the easiest and most powerful way to change your roblox fonts, with it's friendly User Interface.**

This is what the program looks like as of 1.3.1 :

![image](https://user-images.githubusercontent.com/116633390/232840786-d0cf6a73-cb33-4086-b5fd-01c147538822.png)

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

If an error occurs, you should be notified by a notification. Make sure to follow the instructions it gives you.
You can try and troubleshoot yourself, just try again and make sure you selected the proper folder/font path.

# Exclusions :
Starting from update 1.3, you can now choose fonts not to replace.

This allows for further customization, by letting you keep the fonts you want, and have multiple different fonts replaced at once!

The possibilities are endless with this new update. To use it, simply select your content folder and you'll be able to select the fonts you'd not want replaced by pressing the Exclusions button, inside the Exclusions sub category, inside the Replace Fonts category.

You can view which fonts you've chosen not to replace by clicking View Excluded Fonts, and you can remove fonts you've accidentally chosen or just don't want to exclude anymore by pressing the Modify Excluded Fonts. The process is extremely similar to choosing exclusions to add.

You can change the font between each replacement now as the program no longer quits after replacing.

**In order to select multiple fonts at once, use Shift+Click or Ctrl+Click. The first one will select the entire range between the first one you selected and the one you clicked on after, while the latter will select them individually.**

# Backups :
Starting from update 1.2, you are now able to save and restore to backups.

Backups are managed from the Backups category.

All the information you need is provided via info boxes, so please read them through if you need help.

To find your contents folder to restore, follow the same steps as the ones you would to select your contents folder normally.

Backups take a second or less to save depending on your computer's performances.

# Developement :

Everything is explained inside of main.py with comments.
To install all necessary packages, use the following command after downloading the full source code :
```
pip install -r requirements.txt
```

Make sure you have all the folders : backups, logs, data, and config.
The file should then run **from an IDE**. It will not run from the Python shell. It does work with IDLE however.

If you need any extra help, contact me on Discord at Uiop3385#4285 (ID : 611557419222302721)

You are free to do whatever you want with this program, as long as you keep original credit to me in the bottom label, for example, if you remake the program with more features, you can replace it with "Modified by [your_name], original by Uiop3385".


**Thanks for using Roblox Font Replacer!**
