

# Create Controllers
![createController]<img width="375" height="636" alt="Screenshot 2026-05-02 133520" src="https://github.com/user-attachments/assets/2caf60ff-0522-4aa2-8118-d5045e5e791f" />


Welcome to the Maya Custom Controller UI script! This tool simplifies your rigging workflow with an intuitive interface for creating and modifying control curves in Autodesk Maya 2022, 2023, 2024, 2025.

### Features<br/>
Only Ctrl: Quickly create and parent controllers to your selected objects.<br/>
Constraint: Automatically set up controllers with constraints.<br/>
Joint Based: Easily generate joint-based controllers.<br/>
Connection: Create controllers that directly connect to object attributes for precise control.<br/>
Change Shape: Need a different look? Swap out the shape of existing controllers with just a few clicks.<br/>

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

