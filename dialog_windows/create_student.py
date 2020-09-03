# tkinter child window to tigers_houses
# allows user to add new student to Database

import tkinter as tk

class CreateStudentWindow(tk.Toplevel):
    """Pop-up window to add new students to DB"""

    def __init__(self, master, createRecord):
        """Constructor. Takes 2 arguments. master: MainWindow object, createRecord: function"""

        super().__init__(master)

        lightShade = '#eef0ea'

        # save master for to pass back data to parent window
        self._master = master

        # options for house selection
        self._houseOptions = ['Gryffindor', 'Ravenclaw', 'Slytherin', 'Hufflepuff']
        self._createRecord = createRecord

        # intialize tkinter variables
        self.student_id = tk.IntVar()
        self.name = tk.StringVar()
        self.house = tk.StringVar()
        self.points = tk.IntVar()

        # set default values
        self._setDefault()

        # set window dimensions
        self.geometry('325x150+575+300')
        self.minsize(300, 150)
        self.title('Add a New Student')
        self.configure(bg=lightShade)

        # house
        optionLabel = tk.Label(self, text='House', bg=lightShade)
        optionMenu = tk.OptionMenu(self, self.house, *self._houseOptions, command=lambda value: value)

        # name
        nameLabel = tk.Label(self, text='Name', bg=lightShade)
        nameEntry = tk.Entry(self, textvariable=self.name)

        # student id
        idLabel = tk.Label(self, text='Student ID', bg=lightShade)
        validateCmd = self.register(self._intValidation)
        idEntry = tk.Entry(self, textvariable=self.student_id, validate='all', validatecommand=(validateCmd, '%P'))

        # points
        pointsLabel = tk.Label(self, text='Starting Points', bg=lightShade)
        pointsEntry = tk.Entry(self, textvariable=self.points, validate='all', validatecommand=(validateCmd, '%P'))

        # Buttons
        createButton = tk.Button(self, text='Create', command=self._onCreate, highlightthickness=0,
                              highlightbackground=lightShade)

        # place widgets
        optionLabel.grid(row=0, column=0)
        optionMenu.grid(row=0, column=1)
        nameLabel.grid(row=1, column=0)
        nameEntry.grid(row=1, column=1, columnspan=3)
        idLabel.grid(row=2, column=0)
        idEntry.grid(row=2, column=1, columnspan=3)
        pointsLabel.grid(row=3, column=0)
        pointsEntry.grid(row=3, column=1, columnspan=3)
        createButton.grid(row=4, column=1)

    def _onCreate(self):
        """uploads new record to postgres database"""

        student_id = self.student_id.get()
        name = self.name.get()
        house = self.house.get()
        points = self.points.get()

        uploaded = self._createRecord(student_id, name, house, points)

        # pass back message to Parent Window
        if uploaded:
            self._master._message.set('Successfully created {} in house {}!'.format(name, house))

        else:
            self._master.message.set('Could not create {}\'s record in house {}'.format(name, house))

        self.destroy()

    def _setDefault(self):
        """Set variables to default values"""

        self.student_id.set(0)
        self.name.set('N/A')
        self.house.set(self._houseOptions[0])
        self.points.set(0)

    def _intValidation(self, P):
        """Integer validation callback that works with Entry widget"""

        if str.isdigit(P) or P == "":
            return True
        else:
            return False