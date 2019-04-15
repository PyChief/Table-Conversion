import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import os
import urllib.request

class App(tk.Frame):
    '''The main application'''
    def __init__(self, master=None):
        super().__init__(master)
        
        master.minsize(500, 300)
        
        #Allows widgets in all frames to expand when window is resized.
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        MenuBar.menu_bar(self)
        
        # Change default window icon
        self.master.iconbitmap(self, default="py.ico")

        # Change window title text
        self.winfo_toplevel().title("Table Conversion")

        # The current visible frame.
        self.current_frame = None
        self.switch_frame(self.current_frame)

    def quit(self):
        "Closes the Application"
        self.master.destroy()

    def switch_frame(self, frame_class):
        '''Destroys the current frame and replaces it with the inputted
        frame_class.  Use if you need to jump to a particular page.
        '''
        if self.current_frame == None:
            '''If the application has just started, this if statement will
            run in order to set the current frame to the start page.
            '''
            self.current_frame = Page1(self)
            self.current_frame.grid(sticky="nsew")
        else:
            self.current_frame.destroy()              # Destroys previous frame
            self.current_frame = frame_class(self)    # Sets the new frame
            self.current_frame.grid(sticky="nsew")    # Displays the new frame


    """    
    def next_frame(self, cframe_class):
        '''Move from the current frame to the next frame in the tuple.
        Pass self for cframe_class (current frame class)'''
        #print(self.frames[0])
        print(self.frames[0]._name)
        print(cframe_class._name)
        cfi = self.frames.index(cframe_class)   # cfi = current frames index.
        cfi += 1
        self.current_frame.destroy()
        self.current_frame = cframe_class(self.frames[cfi])
        self.current_frame.grid()
    """

class MenuBar(tk.Frame):
    '''The class containing the main menu bar for this app'''
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

    def menu_bar(self):
        menubar = tk.Menu(self.master)
        
        # File Menu
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Edit Menu
        editmenu = tk.Menu(menubar, tearoff = False)
        editmenu.add_separator()
        editmenu.add_command(label = "Preferences", command
                             = lambda: print("This is not supported yet."))
        menubar.add_cascade(label = "Edit", menu = editmenu)

        # Command Needed to Display Menu
        menubar.master.config(menu = menubar)

class Button_Style(tk.Button):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.style_config()
        self.bs_toggle()

    def style_config(self):
        self.config(
            borderwidth=0,
            width=20,    # Default size for 'Next' and 'Previous' buttons
            height=2,    # Default size for 'Next' and 'Previous' buttons
            foreground="#f9f9f9",
            background="#2375ef",
            )

    def bs_toggle(self,
            bg_disabled="#aaaaaa",
            fg_disabled="#7f7e7e",
            bg_enabled="#2375ef",
            fg_enabled="#f9f9f9"
            ):
            '''Toggles the background color depending on whether the button is
            enabled or disabled.
            '''
            if self["state"] == "disabled":
                self.config(background=bg_disabled, foreground=fg_disabled)
            else:
                self.config(background=bg_enabled, foreground=fg_enabled)

class Page1(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.current_label = None
        self.init_gui()
    
    def frame1_widgets(self):
        '''Contains the widgets displed in frame1'''
        self.frame1 = tk.Frame(self)
        self.entry1 = tk.ttk.Entry(self.frame1)
        
        #Radio Button Functionality
        self.type_ = tk.StringVar()
        self.type_.set("url")
        #Radio Button Widgets
        self.radiob_url = tk.ttk.Radiobutton(self.frame1)
        self.radiob_filepath = tk.ttk.Radiobutton(self.frame1)

        #Select Input File button
        self.button_select_file = Button_Style(self.frame1)


        #self.export_path = os.chdir(entry2.get())

    def frame2_widgets(self):
        '''Contains the widgets displed in frame2'''
        self.frame2 = tk.Frame(self)
        self.label_e2 = tk.ttk.Label(self.frame2)
        self.entry2 = tk.ttk.Entry(self.frame2)
        self.button_export_path = Button_Style(self.frame2)
    
    def frame_np(self):
        '''Frame containing the 'next' and 'previous' buttons'''
        self.frame_next = tk.Frame(self)
        self.button_next = Button_Style(self.frame_next, text="Next")

    def window_input_dialog(self):
        '''Window: input file selection'''
        self.window_input_file = tk.filedialog.askopenfilename(
                parent=self.master,
                title="Select File"
                )
        print(self.window_input_file)

    def window_export_dialog(self):
        self.window_export_dir = tk.filedialog.askdirectory(
                parent=self.master,
                title="Select Export Directory"
                )
        print(self.window_export_dir)

    def e1_label(self):
        '''Creates the alternate labels that will display when radio buttons
        are selected.
        '''
        self.label_e1_url = tk.ttk.Label(self.frame1,
                text="Enter the URL containing the table you would like to convert.")
        self.label_e1_file = tk.ttk.Label(self.frame1,
                text="Enter the file path for the table that you would like to convert.")

        # If URL radio button is selected, disable file selection button.
        if self.type_.get() == "url":
            self.e1_switch_label(self.label_e1_url)
            self.button_select_file["state"] = "disabled"
            self.button_select_file.bs_toggle()
        # If File radio button is selected, enable file selection button.
        elif self.type_.get() == "file":
            self.e1_switch_label(self.label_e1_file)
            self.button_select_file["state"] = "normal"
            self.button_select_file.bs_toggle()
    
    def e1_switch_label(self, label_class):
        '''Displays the label for entry 1 depending on radio button selected.
        '''
        if self.current_label == None:
            self.current_label = label_class
            self.e1_show_label()
        elif self.current_label == label_class:
            pass
        else:
            self.current_label.destroy()
            self.current_label = label_class
            self.e1_show_label()
    """
    def change_background_color(self, widget, bg_disabled="#aaaaaa", fg_disabled="#7f7e7e", bg_enabled="#2375ef", fg_enabled="#f9f9f9"):
        if widget["state"] == "disabled":
            widget.config(background=bg_disabled, foreground=fg_disabled)
        else:
            widget.config(background=bg_enabled, foreground=fg_enabled)"""

    def e1_show_label(self):
        self.current_label.grid(row=0, column=1, columnspan=3, pady=5)

    def widget_config(self):
        '''Widget configuration options. Call just before grid_placement() method.'''
        #### Input Frame ####
        """
        self.frame1.config(
                borderwidth=1,
                relief="solid"
                )
        self.frame2.config(
                borderwidth=1,
                relief="solid"
                )
        """
        #self.frame_next()
        self.entry1.config(
                width=60
                )
        self.entry2.config(
                width=60
                )
        self.label_e2.config(
                text="Enter the location where you would like to save the converted table."
                )
        self.radiob_url.config(
                text="URL",
                variable=self.type_,
                value="url",
                command=self.e1_label
                )
        self.radiob_filepath.config(
                text="File Path",
                variable=self.type_,
                value="file",
                command= self.e1_label
                )
        self.button_select_file.config(
                text="...",
                width=4,
                height=1,
                command= self.window_input_dialog
                )
        self.button_export_path.config(
                text="...",
                width=4,
                height=1,
                command= self.window_export_dialog
                )
        self.button_next.config(
                text="Next",
                command = lambda: self.master.switch_frame(Page2)
                )
        """
        self.button_next.config(
                text="Next",
                width=20,
                height=2,
                borderwidth=0,
                foreground="#f9f9f9",
                background="#2375ef",
                command = lambda: self.master.switch_frame(Page2)
                )"""
    
    def grid_placement(self):
        '''Organizes the size and placement of widgets in the frame.
        Always call this function last.
        '''
        #### Column Configurations #################
        self.grid_columnconfigure(0, minsize=500, weight=1)
        
        # Frame1 Columns
        self.frame1.grid_columnconfigure(0, minsize=25, weight=1)
        self.frame1.grid_columnconfigure(4, minsize=25, weight=1)

        # Frame2 Columns
        self.frame2.grid_columnconfigure(0, minsize=25, weight=1)
        self.frame2.grid_columnconfigure(4, minsize=25, weight=1)

        # Frame: Next/Previous button Columns
        self.frame_next.grid_columnconfigure(0, minsize=25, weight=1)
        self.frame_next.grid_columnconfigure(1, minsize=225, weight=0)
        self.frame_next.grid_columnconfigure(2, minsize=225, weight=0)
        self.frame_next.grid_columnconfigure(3, minsize=25, weight=1)

        ##### Frame1 Widgets #######################
        '''Widgets are listed in the order that they will appear
        from top to bottom'''
        #For e1_label, see e1_show_label() method.
        self.frame1.grid(row=0, column=0, pady=10)
        self.entry1.grid(row=1, column=1, columnspan=2)
        self.button_select_file.grid(row=1, column=3, sticky="w")
        #Radio Buttons
        self.radiob_url.grid(row=2, column=1)
        self.radiob_filepath.grid(row=2, column=2)

        #### Frame2 Widgets ########################
        self.frame2.grid(row=1, column=0, pady=10)
        self.label_e2.grid(row=0, column=1, columnspan=3, pady=5)
        self.entry2.grid(row=1, column=1, columnspan=2)
        self.button_export_path.grid(row=1, column=3, sticky="w")
        self.frame2.grid_rowconfigure(2, minsize=20, weight=0)
        
        #### Frame For Next/Previous Buttons #######
        self.frame_next.grid(row=2, column=0, pady=10, sticky="nsew")
        self.button_next.grid(row=0, column=2, sticky="e")

    def init_gui(self):
        self.frame1_widgets()
        self.frame2_widgets()
        self.frame_np()
        self.e1_label()
        self.widget_config()
        self.grid_placement()

class Page2(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        #Label: List of tables; Treeview: List of tables; Check box: show preview; New Window: display table preview.
        #Button: Next; Button: Previous.
        tk.ttk.Label(self, text = "Select the tables that you would like to use.").grid()
        
        # Tree Table
        treeview = tk.ttk.Treeview(self)
        treeview.grid()
        """
        ### Tree Table Functionality
        for table in Page1.df1:
            i += 1
            treeview.insert("", i, f"table{i}", text = f"Table {i}")
            treeview.insert("", "i", f"table{i}", text = f"Table {i}")
        """
        # Check box: Show Table Preview when checked.
        chkbutton = ttk.Checkbutton(self, text = "Show Table Preview")
        chkbutton.grid()
        ### Checkbutton functionality
        #Preview function.  Hold bool value. If On show selected table. If Off hide or destroy window.
        #prev variable = preview function.
        #checkbutton.config()


        # Next & Previous Buttons
        Button_Style(self, text = "Next",
                      command = lambda: master.switch_frame(Page3)).grid()
        Button_Style(self, text = "Previous",
                      command = lambda: master.switch_frame(Page1)).grid()

class Page3(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        #Label: Selected tables; Treeview: Show selected tables; Checkboxes: List options.
        #Button: Next; Button: Previous.
        tk.ttk.Label(self, text = "Select the tables and the functions you would like to perform on them").grid()

        ### Left Frame ###
        Left_Frame = tk.Frame(self)
        Left_Frame.grid()
        ### Treeview
        treeview = tk.ttk.Treeview(Left_Frame)
        treeview.grid()
        # Treeview Functionality:

        Button_Style(Left_Frame, text = "Select All")
        # Select and deselect all when button is clicked.

        ### Right Frame ###
        Right_Frame = tk.Frame(self)
        Right_Frame.grid()
        ### Check Buttons:
        chk_n_excel = tk.ttk.Checkbutton(Right_Frame, text = "Export to New Excel File")
        chk_e_excel = tk.ttk.Checkbutton(Right_Frame, text = "Export to Existing Excel File")
        chk_html = tk.ttk.Checkbutton(Right_Frame, text = "Export to HTML")
        chk_sql = tk.ttk.Checkbutton(Right_Frame, text = "Export to SQL")

        # chk_list = [chk_n_excel, chk_e_excel, chk_html, chk_sql] #Store bool values from chk Buttons

        chk_n_excel.grid()
        chk_e_excel.grid()
        chk_html.grid()
        chk_sql.grid()
        
        ### Next & Previous Buttons
        Button_Style(self, text = "Next", command = lambda: master.switch_frame(Page4)).grid()
        Button_Style(self, text = "Previous", command = lambda: master.switch_frame(Page2)).grid()

class Page4(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        #Label: New label for each option selected in previous window. Entry: new for each option. Select save file path.
        #Button: attached to entry field. Select save path folder.
        #Button: Next; Button: Previous.
        
        #if chk_list[0] == False:
        tk.ttk.Label(self, text = "Select destination folder for exported tables").grid()
        tk.ttk.Entry(self).grid()
        Button_Style(self, text = "Browse").grid()
        #if chk_list[0] == True:
        # Select existing Excel file.

        

        # Next & Previous Buttons
        Button_Style(self, text = "Next", command = lambda: master.switch_frame(Page5)).grid()
        Button_Style(self, text = "Previous", command = lambda: master.switch_frame(Page3)).grid()

class Page5(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        #Treeview: Selected tables. 2 Entry Fields: Row and column for table export location.
        #Button: Confirm entry button. Button: "Reset All" table entries.
        #Button: Next; Button: Previous.
        tk.ttk.Label(self, text = "This is Page 5").grid()
        
        # Next & Previous Buttons
        Button_Style(self, text = "Next", command = lambda: master.switch_frame(Page6)).grid()
        Button_Style(self, text = "Previous", command = lambda: master.switch_frame(Page4)).grid()

class Page6(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        #Icon: Green check mark; Label: Complete; Button: Quit; Button: New Process
        tk.ttk.Label(self, text = "Complete!").grid()
        Button_Style(self, text = "Quit", command = self.master.quit).grid()    #Why doesn't this quit the application?
        Button_Style(self, text = "New Process", command = lambda: master.switch_frame(Page1)).grid()

def main():
    root = tk.Tk()     # Use Tk() constructor method to create top level tk window.
    app = App(root)    # Pass root to your App class to serve as the master window.
    root.mainloop()     # Call mainloop on your top level window to enter into tk event loop.


if __name__ == "__main__":
    main()