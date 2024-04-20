# terrible code sorry
# - daniel


import tkinter.ttk as ttk
import tkinter as tk
import sv_ttk
import threading
import time
from savedata import saveNote, readNotes

totalJournalData = None
journalButtonPointsToTimestamp = {} #this is so stupid

root = tk.Tk()

root.geometry("1280x600")
root.title("Pyrobib")
root.resizable(False, False)

#GroupFrame
groupFrame = tk.Frame(master=root, bg="#3d3d3d", width=230)
groupFrame.pack(side=tk.LEFT, fill=tk.Y)

#GroupFrame -> SearchBar
groupSearchBar = ttk.Entry(master=groupFrame)
groupSearchBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=16)

#GroupFrame -> NoteList
journalList = tk.Frame(master=groupFrame)
journalList.pack(side=tk.TOP, fill=tk.BOTH)

#GroupFrame -> NewJournalButton
newJournalButton = ttk.Button(master=groupFrame, text="New Journal")
newJournalButton.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(master=root, orient="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#TextEntryFrame -> titleEntry
textEntryFrame = ttk.Frame(master=root)
aibutton = ttk.Button(master=textEntryFrame, text="Ask AI")
aibutton.pack(side= tk.RIGHT, anchor="ne", pady=(20, 0))
titleTextEntry = tk.Entry(master=textEntryFrame, font=("Arial", 16, "bold"), fg="gray", borderwidth=0, highlightthickness=0)
def onTitleTextEntryClick(event): #clear Add Title text on focus
    titleTextEntry.delete(0, tk.END)
    titleTextEntry.configure(fg="white")
titleTextEntry.insert(tk.END, "Add Title")
titleTextEntry.pack(side=tk.TOP, anchor="nw", pady=(0, 10))
titleTextEntry.bind("<Button-1>", onTitleTextEntryClick)

#TextEntryFrame -> bodyEntry
bodyTextEntry = tk.Text(master=textEntryFrame, yscrollcommand=scrollbar.set, font=("Arial"), borderwidth=0, highlightthickness=0
                        , spacing1 = 8, spacing3 = 8, spacing2=5)
bodyTextEntry.pack(fill=tk.BOTH, side=tk.TOP)

#textEntryFrame.pack(padx=30, pady=20, side=tk.LEFT)


def openJournal(creationTime):
    print(creationTime)

#On Note Add:
#GroupFrame -> NoteList -> NoteButton
def addJournal(event):
    journalButton = tk.Button(master=journalList, text="Unnamed Journal", borderwidth=0)
    journalButton.pack(side=tk.TOP, fill=tk.X)
    journalButton.bind("<Button-1>", lambda event: addJournal(noteData["creationTime"]))
    title = "Unnamed Journal"
    creationTime = time.time()
    group = "NoGroup"
    body = ""
    titleTextEntry.delete(0, tk.END)
    titleTextEntry.insert(tk.END, "Add Title")
    bodyTextEntry.delete("1.0", tk.END)
    textEntryFrame.pack(padx = 30, pady = 20, side=tk.LEFT)
    thread = threading.Thread(target=saveNote, args=(title, creationTime, group, body))
    thread.start()

newJournalButton.bind("<Button-1>", addJournal)

#Load existing notes
def loadExistingJournals():
    totalJournalData = readNotes()
    for noteData in totalJournalData:
        journalButton = tk.Button(master=journalList, text=noteData["title"], borderwidth=0)
        journalButton.pack(side=tk.TOP, fill=tk.X)
        journalButton.bind("<Button-1>", lambda event: addJournal(noteData["creationTime"]))


loadExistingJournals()
scrollbar.config(command=bodyTextEntry.yview)
sv_ttk.set_theme("dark")
root.mainloop()