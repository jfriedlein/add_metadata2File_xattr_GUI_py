#!/usr/bin/env python3

# drafted by [perplexity.ai]

# active version located under: ~/.config/caja/scripts/xattr_gui.py
#  to have it available in right-click menue of caja file explorer


import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, StringVar, OptionMenu
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os
import sys

class XAttrApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        # Set this GUI as "always on top" to simplify drag&drop
        self.attributes("-topmost", 1)

        self.title("xattr Note Setter")
        self.geometry("500x500+1200+300")
        self.file_path = None

        # Instructions label
        tk.Label(self, text="Drag and drop a file here:", font=("Arial", 12)).pack(pady=(10, 5))

        # Drag and drop area (a label)
        self.drop_area = tk.Label(self, text="Drop file here", relief="ridge", width=50, height=4, bg="white")
        self.drop_area.pack(pady=5)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.drop)

        # Fallback: click to open file dialog
        self.drop_area.bind("<Button-1>", self.browse_file)

        # Show selected file path
        self.file_label = tk.Label(self, text="No file selected", fg="red")
        self.file_label.pack(pady=(5,10))

        # Attribute selection
        self.attr_var = StringVar()
        self.attr_menu = None  # Will be created dynamically
        self.attr_label = tk.Label(self, text="Attribute name:", anchor="w")
        self.attr_label.pack(fill="x", padx=10, after=self.file_label)
        self.attr_entry = tk.Entry(self)
        self.attr_entry.pack_forget()  # Hide initially

        # Note text box
        tk.Label(self, text="Note:", anchor="w").pack(fill="x", padx=10)
        self.note_text = scrolledtext.ScrolledText(self, height=5)
        self.note_text.pack(fill="both", padx=10, pady=(0,10), expand=True)

        # Create a frame to hold both buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)  # Centered by default

        # Store button
        self.store_btn = tk.Button(button_frame, text="Store", command=self.store_xattr)
        self.store_btn.pack(side='left', padx=10)

        # Delete button
        self.delete_btn = tk.Button(button_frame, text="Delete", command=self.delete_xattr)
        self.delete_btn.pack(side='left', padx=10)

        # If the script was started with an input argument, then this is the chosen filepath and will be loaded
        if len(sys.argv) > 1:
            # Get the first argument
            path = sys.argv[1]
            self.load_file(path)

    def update_note_text( self, attr_selected ):
        text = self.get_xattr_value(self.file_path, attr_selected)
        self.note_text.delete("1.0", "end")
        self.note_text.insert("1.0", text if text is not None else "")

    def clear_fields(self):
        # Clear attribute entry, note, and remove attribute menu if exists
        self.attr_entry.delete(0, 'end')
        self.note_text.delete("1.0", "end")
        if self.attr_menu:
            self.attr_menu.pack_forget()
            self.attr_menu = None
        self.attr_entry.pack_forget()

    def setup_attr_menu(self, attrs):
        # Create the OptionMenu for attributes
        options = attrs + ["Add new attribute…"]
        self.attr_var.set(options[0])
        if self.attr_menu:
            self.attr_menu.pack_forget()
        self.attr_menu = OptionMenu(self, self.attr_var, *options, command=self.on_attr_select)
        #tk.Label(self, text="Attribute name:", anchor="w").pack(fill="x", padx=10)
        self.attr_menu.pack(fill="x", padx=10, pady=(0,10), after=self.attr_label)
        self.attr_entry.pack_forget()
        self.on_attr_select(options[0])

    def on_attr_select(self, selected):
        if selected == "Add new attribute…":
            self.attr_entry.pack(fill="x", padx=10, pady=(0,10), after=self.attr_menu)
            self.attr_entry.delete(0, 'end')
            self.note_text.delete("1.0", "end")
            #self.update_note_text( selected )
        else:
            self.attr_entry.pack_forget()
            # Show value for selected attribute
            self.update_note_text( selected )

    def get_xattr_list(self, path):
        try:
            result = subprocess.run(["xattr", path], capture_output=True, text=True, check=True)
            attrs = result.stdout.strip().split('\n')
            attrs = [a for a in attrs if a]
            return attrs
        except subprocess.CalledProcessError:
            return []

    def get_xattr_value(self, path, attr):
        try:
            result = subprocess.run(["xattr", "-p", attr, path], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return None

    def drop(self, event):
        files = self.tk.splitlist(event.data)
        if files:
            path = files[0]
            self.load_file(path)
        return "break"

    def load_file(self, path):
        if path.startswith('file://'):
            path = path[7:]
        path = path.strip()
        if os.path.isfile(path):
            self.file_path = path
            self.file_label.config(text=self.file_path, fg="green",wraplength=480, justify="left")
            self.clear_fields()
            attrs = self.get_xattr_list(path)
            if attrs:
                self.setup_attr_menu(attrs)
            else:
                # No attributes, show entry to add new
                if self.attr_menu:
                    self.attr_menu.pack_forget()
                    self.attr_menu = None
                #tk.Label(self, text="Attribute name:", anchor="w").pack(fill="x", padx=10)
                self.attr_entry.pack(fill="x", padx=10, pady=(0,10), after=self.attr_label)
        else:
            messagebox.showerror("Error", "Dropped item is not a file.")

    def browse_file(self, event=None):
        path = filedialog.askopenfilename()
        if path:
            self.file_path = path
            self.file_label.config(text=self.file_path, fg="green")
            self.clear_fields()
            attrs = self.get_xattr_list(path)
            if attrs:
                self.setup_attr_menu(attrs)
            else:
                # No attributes, show entry to add new
                if self.attr_menu:
                    self.attr_menu.pack_forget()
                    self.attr_menu = None
                #tk.Label(self, text="Attribute name:", anchor="w").pack(fill="x", padx=10)
                self.attr_entry.pack(fill="x", padx=10, pady=(0,10), after=self.attr_label)

    def store_xattr(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        # Determine attribute name
        attr = None
        if self.attr_menu and self.attr_var.get() != "Add new attribute…":
            attr = self.attr_var.get().strip()
        else:
            attr = self.attr_entry.get().strip()

        note = self.note_text.get("1.0", "end").strip()
        if not attr:
            messagebox.showerror("Error", "Attribute name cannot be empty.")
            return
        #if not note:
        #    messagebox.showerror("Error", "Note cannot be empty.")
        #    return

        # Use 'user.' namespace if not provided
        if '.' not in attr:
            attr = "user." + attr

        try:
            subprocess.run(["xattr", "-w", attr, note, self.file_path], check=True)
            # Refresh attribute menu
            attrs = self.get_xattr_list(self.file_path)
            if attrs:
                self.setup_attr_menu(attrs)
            else:
                if self.attr_menu:
                    self.attr_menu.pack_forget()
                    self.attr_menu = None
                #tk.Label(self, text="Attribute name:", anchor="w").pack(fill="x", padx=10)
                #self.attr_entry.pack(fill="x", padx=10, pady=(0,10))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to set xattr:\n{e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "xattr command not found. Please install it.")

        self.attr_var.set( attr )
        self.update_note_text( attr )


    def delete_xattr(self):
        """Delete the selected extended attribute from the current file."""
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        attr = self.attr_var.get().strip()
        if not attr or attr == "Add new attribute…":
            messagebox.showerror("Error", "No valid attribute selected to delete.")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Delete attribute '{attr}' from:\n{self.file_path}?"):
            return

        try:
            subprocess.run(["xattr", "-d", attr, self.file_path], check=True)
            # Refresh attribute menu
            attrs = self.get_xattr_list(self.file_path)
            if attrs:
                self.setup_attr_menu(attrs)
            else:
                if self.attr_menu:
                    self.attr_menu.pack_forget()
                    self.attr_menu = None
                #tk.Label(self, text="Attribute name:", anchor="w").pack(fill="x", padx=10)
                self.attr_entry.pack(fill="x", padx=10, pady=(0,10), after=self.attr_label)
            self.note_text.delete("1.0", "end")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to delete xattr:\n{e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "xattr command not found. Please install it.")

        attrs = self.get_xattr_list(self.file_path)
        if len(attrs)>0:
            # Since the selected entry was removed, we show the first entry and corresponding note
            self.attr_var.set( attrs[0] )
            self.update_note_text( attrs[0] )
        else:
            # The attribute list is empty, so we remove the shown entry in the text input
            self.attr_entry.delete(0, 'end')

if __name__ == "__main__":
    app = XAttrApp()
    app.mainloop()

