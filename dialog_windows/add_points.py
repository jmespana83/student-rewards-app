# child window to tigers_houses
# allows user to add a defined number of points awarded to the student

import tkinter as tk
from postgres_client import PGClient

class AddPointsWindow(tk.Toplevel):
    """Toplevel window that allows teacher to points to selected student profile"""

    def __init__(self, master, studentRecord, updateRecord):
        """Constructor. Accepts studentRecord: tuple(pk, student_id, name, house, points) as argument to update and add
        points to profile and updateRecord from postgres client to upload to database"""

        super().__init__(master)

        self._master = master

        lightShade = '#eef0ea'

        # create member and store any class variables
        self._updateRecord = updateRecord      # method from pgClient
        self._record = studentRecord
        self._points = tk.IntVar()
        self._points.set(0)                     # default variable to 0

        # set window dimensions
        self.geometry('300x80+600+300')
        self.title('Add Points for {}'.format(studentRecord[2]))
        self.configure(bg=lightShade)

        # label for entry
        pointsLabel = tk.Label(self, text='Points', bg=lightShade)

        # entry for points
        validateCmd = self.register(self._intValidation)
        pointsEntry = tk.Entry(self, textvariable=self._points, validate='all', validatecommand=(validateCmd, '%P'))

        # add button
        addButton = tk.Button(self, text="Add", command=self._addPoints, highlightthickness=0,
                              highlightbackground=lightShade)

        # place widgets inside frame
        pointsLabel.pack()
        pointsEntry.pack()
        addButton.pack()


    def _addPoints(self):
        """Add new points to current points in student record"""
        newPoints = self._points.get()

        # student records destructured
        pk, student_id, name, house, points = self._record

        # add new points to student's current points
        points += newPoints

        # create new record, save locally, and update to database
        newRecord = (pk, student_id, name, house, points)
        self._updateRecord(newRecord)

        # pass back new record to master window
        self._master._studentRecord = newRecord

        # notify of how many points added with the parent window's label
        self._master._message.set('{} has been award to {}. Total: {}'.format(newPoints, name, points))

        # exit child window after updating record and saving message to parent window
        self.destroy()

    def _intValidation(self, P):
        """Integer validation callback that works with Entry widget"""

        if str.isdigit(P) or P == "":
            return True
        else:
            return False
