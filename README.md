# add_metadata2File_xattr_GUI_py
Python graphical user interface that allows to easily add metadata to a file using xattr (Linux)


## What this does
Instead of putting some information into the filename of e.g. a picture, you can use this GUI to add all the information you want into the metadata of a file.

This is set up for Linux using xattr and python.

Some limitations for xattr exist (data size ~kByte, etc.)

## How-to
### Usage with file explorer caja
- Download the "xattr_gui.py" script and place it into ~/.config/caja/scripts
- You probably need to add some python packages (tkinter, xattr, ...)
- Select a file in the file explorer caja, right-click on the file -> "Scripts" -> "xattr_gui.py"
- A python GUI opens which loads the file attributes for the selected file, e.g. for the python script itself:

<img src="https://github.com/jfriedlein/add_metadata2File_xattr_GUI_py/blob/main/xattr%20Note%20setter%20-%20start%20screen.png" width="500">

- In the text box after "Attribute name:", you can enter the name of the attribute, e.g. "internal length parameter"
- In the text box after "Note:", you can add your text or value, here e.g. "2 mm"
- Clicking on the button "Store" will save the attribute using xattr
- Once one or more attributes exist for a file, a drop-down menu appears which allows to show/edit existing attributes or "Add new attribute..."

<img src="https://github.com/jfriedlein/add_metadata2File_xattr_GUI_py/blob/main/xattr%20Note%20setter%20-%20existing%20attribute.png" width="500">

- With this window open, you can also drag&drop a different file into it to add or check its attributes
- Note, in the python script the GUI is set as "always on top" to ease drag&drop. In case you don't like this, you remove the Python code line setting the window as topmost.

## Health warning
This is a quick&dirty 2 hour AI-based implementation.

## ToDos
- collect the needed python packages
- This could be packed into a standalone python executable to avoid the need for a python installation and the GUI packages.
