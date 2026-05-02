

# Create Controllers
<img width="375" height="636" alt="Screenshot 2026-05-02 133520" src="https://github.com/user-attachments/assets/2caf60ff-0522-4aa2-8118-d5045e5e791f" />


Welcome to the Maya Custom Controller UI script! This tool simplifies your rigging workflow with an intuitive interface for creating and modifying control curves in Autodesk Maya.

## Features<br/>
* **Shape Library:** Create various control shapes via icon buttons.<br/>
* **Auto-Offset:** Automatically generates a hierarchy of offset/SDK groups.<br/>
* **Text Curves:** Quickly turn text strings into clean NURBS control shapes.<br/>
* **Color Palette:** 31-color override palette for quick rig organization.<br/>
* **Utility Tools:** Change existing shapes, combine shapes, and adjust line width.<br/>

### Installation
Download the Script.<br/>
copy createController the script folder to Maya's default "scripts" folder.<br/>

    Windows: Documents/maya/scripts
    macOS: ~/Library/Preferences/Autodesk/maya/scripts
    Linux: ~/maya/scripts

Run the Script in Maya:<br/>
Open Maya and head over to the Script Editor.<br/>
Switch to a Python tab and run the following lines.<br/>

    from createController import createController
    createController.launchUI()

