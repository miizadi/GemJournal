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
selectedTimestamp = None #probably causing a million bugs
selectedButton = None # also causing a million bugs

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

#GroupFrame -> JournalList
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


def openJournal(creationTime, buttonObject):

    global totalJournalData
    totalJournalData = readNotes()
    global selectedButton
    selectedButton = buttonObject

    for journalData in totalJournalData:
        print(journalData["creationTime"])
        if journalData["creationTime"] == creationTime:
            print("found it")
            global selectedTimestamp
            selectedTimestamp = journalData["creationTime"]
            titleTextEntry.delete(0, tk.END)


            if journalData["title"] != "Unnamed Journal":
                titleTextEntry.configure(fg="white")
                titleTextEntry.insert(tk.END, journalData["title"])
            else:
                titleTextEntry.configure(fg="gray")
                titleTextEntry.insert(tk.END, "Add Title")

            bodyTextEntry.delete("1.0", tk.END)
            bodyTextEntry.insert("1.0", journalData["body"])
            textEntryFrame.pack(padx=30, pady=20, side=tk.LEFT)

#On Note Add:
#GroupFrame -> NoteList -> NoteButton
def addJournal(event):
    journalButton = tk.Button(master=journalList, text="Unnamed Journal", borderwidth=0)
    journalButton.pack(side=tk.TOP, fill=tk.X)
    title = "Unnamed Journal"
    creationTime = time.time()
    group = "NoGroup"
    body = ""
    saveNote(title, creationTime, group, body)
    global totalJournalData
    totalJournalData = readNotes()
    print(creationTime)
    openJournal(creationTime)

newJournalButton.bind("<Button-1>", addJournal)


def lambdaMaker(thing, buttonObject):
    return lambda e: openJournal(thing, buttonObject)

#Load existing notes
def loadExistingJournals():
    global totalJournalData
    totalJournalData = readNotes()

    for noteData in totalJournalData:
        journalButton = tk.Button(master=journalList, text=noteData["title"], borderwidth=0)
        journalButton.pack(side=tk.TOP, fill=tk.X)
        journalButton.bind("<Button-1>", lambdaMaker(noteData["creationTime"], journalButton))

#autosave
def autosave(event):
    thread = threading.Thread(target=saveNote, args=(titleTextEntry.get(), selectedTimestamp, "NoGroup", bodyTextEntry.get("1.0", tk.END)))
    thread.start()
    selectedButton.config(text=titleTextEntry.get())


titleTextEntry.bind("<KeyRelease>", autosave)
bodyTextEntry.bind("<KeyRelease>", autosave)

loadExistingJournals()
scrollbar.config(command=bodyTextEntry.yview)
sv_ttk.set_theme("dark")
root.mainloop()