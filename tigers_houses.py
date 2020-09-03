### Tiger's Houses (Harry Potter Themed) ###

# a student reward tracker program using Harry Potter themed houses as teams

### Allows teachers to upload student points from different computers
### All data will be uploaded to HTML page for display

##### Some key notes: Tuples are converted to lists in this class's local storage for to change name to title case.
##### Data structures still operate the same in each method and subsequent child windows even if they were inteded to
##### use tuples or still do.


import tkinter as tk
from tkinter import ttk
import webbrowser
from tkinter import messagebox as tkmb
from postgres_client import PGClient    # import custom class from postgres_client module
from dialog_windows.create_student import CreateStudentWindow
from dialog_windows.add_points import AddPointsWindow
from dialog_windows.edit_students import EditStudentWindow
import os
# from json_serializer import pgToJSON          # no longer needed. Data is parsed directly in PHP file



class MainWindow(tk.Tk):
    """A GUI Program that allows teach to add/edit student profiles and
    points"""

    def __init__(self):
        """initialize main window"""

        super().__init__()

        # Styling variables
        self._app_image = tk.PhotoImage(file='me.png')
        lightShade = '#eef0ea'
        lightAccent = '#bd8f48'
        darkAccent = '#89443e'
        darkShade = '#4d3a3c'
        danger = '#ba2f16'


        # connect to database object with client('DATABASE NAME', 'USER', 'PASSWORD', 'HOST') – Make sure
        self._pgClient = PGClient('rpnrceuz', 'rpnrceuz', 'trxpcf3NlLg-6X6oHYbwgKPYFGI3sO_n', 'salt.db.elephantsql.com')

        # initialize member variables for window
        self._houseOptions = ['All', 'Gryffindor', 'Ravenclaw', 'Slytherin', 'Hufflepuff']

        self._houseChoice = tk.StringVar()              # display list of students in that house
        self._houseChoice.set(self._houseOptions[0])    # default to All Houses

        self._message = tk.StringVar()              # informs user of successful creation, add_points,
        self._message.set('')

        self._studentRecord = None      # selected studentChoice's record
        self._treeStorage = None        # local storage for tree view after fetching from db
        self._prevSort = {'index': None, 'reverse': False} # used to check if prev column was sorted in order to reverse

        # use hosted url for view
        self._url = 'https://murmuring-bayou-87911.herokuapp.com/'

        # initialize window dimensions
        self.geometry('620x580+450+150')
        self.minsize(300, 300)
        self.title('Tigers Houses: Harry Potter Themed!')

        # header of the app
        appTitle = tk.Label(self, text='Tigers Houses', background='black', foreground=lightAccent)
        imgLabel = tk.Label(self, image=self._app_image)

        # create widgets and place inside corresponding frame
        # frame 1: top frame with drop down menu for house selection or add student button
        topFrame = tk.Frame(self, background='black')

        self._optionMenu = tk.OptionMenu(topFrame, self._houseChoice, *self._houseOptions, command=self._populateTree)
        optionMenuLabel = tk.Label(topFrame, text="Choose Your house", background='black', foreground='white')
        addStudentButton = tk.Button(topFrame, text="Add New Student", foreground=lightAccent, highlightthickness=0,
                                     highlightbackground='black', command=self._createStudent)

        optionMenuLabel.grid(row=0, column=0)  # first row
        self._optionMenu.grid(row=0, column=1)
        addStudentButton.grid(row=0, column=3)

        # frame 2: listbox with students in house
        midFrame = tk.Frame(self, background='black')

        scrollBar = tk.Scrollbar(midFrame)
        # build tree with columns, headings, and heading sizes
        self._tree = ttk.Treeview(midFrame, selectmode='browse', columns=['#1', '#2', '#3', '#4'])
        self._tree.column('#0', width=100)
        self._tree.column('#1', width=120)
        self._tree.column('#2', width=200)
        self._tree.column('#3', width=100)
        self._tree.column('#4', width=75)

        self._tree.heading('#0', text='Order Added', anchor=tk.W, command=lambda: self._sortBy(0))
        self._tree.heading('#1', text='Student ID', anchor=tk.W, command=lambda: self._sortBy(1))
        self._tree.heading('#2', text='Name', anchor=tk.W, command=lambda: self._sortBy(2))
        self._tree.heading('#3', text='House', anchor=tk.W, command=lambda: self._sortBy(3))
        self._tree.heading('#4', text='Points', anchor=tk.W, command=lambda: self._sortBy(4))

        self._populateTree('All')
        self._tree.bind("<<TreeviewSelect>>", self._selectTreeVal)

        self._tree.grid()
        scrollBar.config(command=self._tree.yview)
        scrollBar.grid(row=0, column=1, sticky='e')

        # frame 3: button group used with listbox above
        buttonFrame = tk.Frame(self, bg='black')

        addPointsButton = tk.Button(buttonFrame, text='Add Points', command=self._addPoints,
                                    foreground=lightAccent, highlightthickness=0, highlightbackground='black')
        editButton = tk.Button(buttonFrame, text='Edit', command=self._editStudent, foreground=lightAccent,
                               highlightthickness=0, highlightbackground='black')
        deleteButton = tk.Button(buttonFrame, text='Delete', command=self._deleteStudent,
                                 foreground=danger, highlightthickness=0, highlightbackground='black')

        addPointsButton.pack(side=tk.LEFT)
        deleteButton.pack(side=tk.RIGHT)
        editButton.pack(side=tk.RIGHT)

        # frame 4
        finalFrame = tk.Frame(self, bg='black')
        displayButton = tk.Button(finalFrame, text='View Scores', command=self._createView, foreground=darkAccent,
                                  highlightthickness=0, highlightbackground='black')
        displayButton.pack(fill='y')

        # frame 5
        exitFrame = tk.Frame(self, bg='black')
        exitButton = tk.Button(exitFrame, text='Exit', bg='white', foreground=danger, command=self._close,
                               highlightthickness=0, highlightbackground='black')
        exitButton.pack(side=tk.BOTTOM)

        # message label
        messageLabel = tk.Label(self, textvariable=self._message, background='black', foreground=lightShade)

        # Applying styles to widgets
        self.configure(background='black')

        # place frames on window with pack for centering
        appTitle.pack()
        imgLabel.pack()
        topFrame.pack()
        midFrame.pack()
        buttonFrame.pack(fill='x')
        messageLabel.pack(fill='x')
        finalFrame.pack()
        exitFrame.pack()

        # intialize treeview population
        self._populateTree(self._houseChoice.get())

    def _populateTree(self, value):
        """accepts type of house and populates students from that house"""

        # delete all child items before loading new data
        self._tree.delete(*self._tree.get_children())
        self._treeStorage = self._pgClient.fetchHouseRecords(value)

        # change to list to mutate name
        self._treeStorage = [list(tup) for tup in self._treeStorage]

        # use title case for local viewing
        for i in range(0, len(self._treeStorage)):
            self._treeStorage[i][2] = self._treeStorage[i][2].title()

        for record in self._treeStorage:
            pk, student_id, name, house, points = record
            self._tree.insert('', 'end', text=pk, values=(student_id, name, house, points))

    def _refreshTree(self):
        """Similar to populate tree with no DB call to preserve order."""

        # refresh treeview after making db call. Repeat code to keep sort (no db fetch)
        self._tree.delete(*self._tree.get_children())

        for i in range(0, len(self._treeStorage)):
            pk, student_id, name, house, points = self._treeStorage[i]
            # update record with new info
            if pk == self._studentRecord[0]:
                pk, student_id, name, house, points = self._studentRecord
                self._treeStorage[i] = [pk, student_id, name, house, points]
            self._tree.insert('', 'end', text=pk, values=(student_id, name, house, points))

    def _selectTreeVal(self, event):
        """select a row form the tree view"""

        selectedItem = self._tree.focus()

        # dictionary from tree item example:
        # {'text': 16, 'image': '', 'values': [3081, 'Josh', 'Slytherin', 230], 'open': 0, 'tags': ''}
        student_id, name, house, points = self._tree.item(selectedItem)['values']
        pk = self._tree.item(selectedItem)['text']

        self._studentRecord = [pk, student_id, name, house, points]

    def _sortBy(self, index):
        """used with tree value to sort tree value by category. Takes index value of column/record position"""

        # check if last sort was the same category
        if self._prevSort['index'] == index:
            # if so reverse sort order from the last time
            self._prevSort['reverse'] = not self._prevSort['reverse']
        else:
            # else change category of sort and do not reverse
            self._prevSort['index'] = index
            self._prevSort['reverse'] = False


        sortedTree = sorted(self._treeStorage, key=lambda t: t[index], reverse=self._prevSort['reverse'])
        self._treeStorage = sortedTree

        # repopulate tree
        self._tree.delete(*self._tree.get_children())

        for record in self._treeStorage:
            pk, student_id, name, house, points = record
            self._tree.insert('', 'end', text=pk, values=(student_id, name, house, points))


    def _createStudent(self):
        """method to launch CreateStudentWindow object"""

        window = CreateStudentWindow(self, self._pgClient.createRecord)
        window.grab_set()        # disables events for other window
        window.focus_set()       # sets focus on current window
        window.transient(self)   # causes no extra icon when created
        self.wait_window(window) # tells main window to wait for child window

        # adding new student will always fetch from db again since it creates new PK
        self._populateTree(self._houseChoice.get())

    def _addPoints(self):
        """method to launch AddPointsWindow object"""

        # Check if a selection to listbox was made
        if self._studentRecord is not None:
            window = AddPointsWindow(self, self._studentRecord, self._pgClient.updateRecord)
            window.grab_set()       # disables events for other window
            window.focus_set()      # sets focus on current window
            window.transient(self)   # causes no extra icon when created
            self.wait_window(window)  # tells main window to wait for child window

            self._refreshTree()

    def _editStudent(self):
        """method to launch EditStudentsWindow object"""

        # Check if a selection to listbox was made
        if self._studentRecord is not None:
            window = EditStudentWindow(self, self._studentRecord, self._pgClient.updateRecord)
            window.grab_set()   # disables events for other window
            window.focus_set()  # sets focus on current window
            window.transient(self)   # causes no extra icon when created
            self.wait_window(window)  # tells main window to wait for child window

            self._refreshTree()

    def _deleteStudent(self):
        """Deletes selected student from database."""

        # Check if a selection to listbox was made
        if self._studentRecord is not None:

            # destructure variables to extract name and pk
            pk, student_id, name, house, points = self._studentRecord

            # see if user is absolutely positive on deleting student
            confirmDelete = tkmb.askyesnocancel('Deleting {}\'s Record'.format(name),
                                                'Are you sure you want to delete {}\'s record?'.format(name))

            # if user confirmed message box, continue with deleting
            if confirmDelete:
                self._pgClient.deleteRecord(pk)

                # custom refresh for delete
                self._tree.delete(*self._tree.get_children())
                self._treeStorage.remove(list(self._studentRecord))       # remove deleted item from local storage
                for record in self._treeStorage:
                    pk, student_id, name, house, points = record
                    self._tree.insert('', 'end', text=pk, values=(student_id, name, house, points))

    def _createView(self):
        """performs JSON extraction from DB and opens up HTML display in browser."""

        # pgToJSON(self._pgClient.fetchHouseRecords)            # no longer needed
        webbrowser.open_new(self._url)

    def _close(self):
        """Close program on exit"""

        self.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Destructor to remove tkinter StringVar properly"""

        self._houseChoice = None
        self._message = None



def main():
    """Main program"""

    window = MainWindow()
    window.mainloop()


main()