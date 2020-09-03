# child window to MainWindow
# allows user to edit selected student information

import tkinter as tk
from postgres_client import PGClient


class EditStudentWindow(tk.Toplevel):
    """Edit student class. A toplevel window to MainWindow.
    Allows for updating student record in DB"""

    def __init__(self, master, studentRecord, updateRecord):
        """Constructor. Takes master: tk.Tk object, studentRecord: tuple(pk, student_id, name, house, points),
        and updateRecord: method from PGClient class"""

        super().__init__(master)

        self._master = master

        lightShade = '#eef0ea'

        # store member variables
        # options for house selection
        self._houseOptions = ['Gryffindor', 'Ravenclaw', 'Slytherin', 'Hufflepuff']

        self._studentRecord = studentRecord
        self._updateRecord = updateRecord
        pk, student_id, name, house, points = studentRecord

        self.pk = pk
        self.student_id = tk.IntVar()
        self.name = tk.StringVar()
        self.house = tk.StringVar()
        self.points = tk.IntVar()

        # prefill tk variables to populate entry fields
        self.student_id.set(student_id)
        self.name.set(name)
        self.house.set(house)
        self.points.set(points)

        # set window dimensions
        self.geometry('325x150+575+300')
        self.minsize(300, 150)
        self.title('Edit {}\' Records'.format(name))
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
        editButton = tk.Button(self, text='Submit', command=self._onSubmit, highlightthickness=0,
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
        editButton.grid(row=4, column=1)

    def _onSubmit(self):
        """Updates record in database"""

        newRecord = (self.pk, self.student_id.get(), self.name.get(), self.house.get(), self.points.get())

        updated = self._updateRecord(newRecord)

        if updated:
            self._master._message.set('Successfully updated: ID: {}, Name: {}, House: {}, Points: {}'.format(
                self.student_id.get(), self.name.get(), self.house.get(), self.points.get()
            ))
            self.master._studentRecord = newRecord  # pass back new record to master window

        else:
            self._master._message.set('Could not update {}\'s record'.format(self._name, ))

        self.destroy()


    def _intValidation(self, P):
        """Integer validation callback that works with Entry widget"""

        if str.isdigit(P) or P == "":
            return True
        else:
            return False