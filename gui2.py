# LAHacks
# Helena Sun
# helenays@uci.edu

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


class main(tk.Tk):
    """
    Main window/root
    """
    def __init__(self):
        super().__init__()
        self.geometry("1280x600")
        self.title("Pyrobib")
        self.resizable(False, False)
        self.leftSection = LeftSection(self)
        self.rightSection = RightSection(self)
        self.leftSection.newButton.bind("<Button-1>", self.addJournal)
        self.rightSection.text_body.title_entry.bind("<KeyRelease>", self.autosave)
        self.rightSection.text_body.text.bind("<KeyRelease>", self.autosave)
        self.loadExistingJournals()
        sv_ttk.set_theme("dark")
        self.mainloop()

    def autosave(self, event):
        if selectedButton is None or selectedTimestamp is None:
            return
        thread = threading.Thread(target = saveNote, args = (
        self.rightSection.text_body.title_entry.get(), selectedTimestamp, "NoGroup",
            self.rightSection.text_body.text.get("1.0", tk.END)))
        thread.start()
        selectedButton.config(text = self.rightSection.text_body.title_entry.get())


    def openJournal(self, creationTime, buttonObject):
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
                self.rightSection.text_body.title_entry.delete(0, tk.END)

                if journalData["title"] != "Unnamed Journal":
                    self.rightSection.text_body.title_entry.configure(fg = "white")
                    self.rightSection.text_body.title_entry.insert(tk.END, journalData["title"])
                else:
                    self.rightSection.text_body.title_entry.configure(fg = "gray")
                    self.rightSection.text_body.title_entry.insert(tk.END, "Add Title")

                self.rightSection.text_body.text.delete("1.0", tk.END)
                self.rightSection.text_body.text.insert("1.0", journalData["body"])
                self.rightSection.text_body.pack(padx = 30, pady = 20, side = tk.LEFT)

    def addJournal(self, event):
        journalButton = tk.Button(master = self.leftSection, text = "Unnamed Journal", borderwidth = 0)
        journalButton.pack(side = tk.TOP, fill = tk.X)
        title = "Unnamed Journal"
        creationTime = time.time()
        group = "NoGroup"
        body = ""
        saveNote(title, creationTime, group, body)
        global totalJournalData
        totalJournalData = readNotes()
        print(creationTime)
        self.openJournal(creationTime, journalButton)

    def lambdaMaker(self, thing, buttonObject):
        return lambda e: self.openJournal(thing, buttonObject)

    # Load existing notes
    def loadExistingJournals(self):
        global totalJournalData
        totalJournalData = readNotes()

        createdFirstButton = False

        for noteData in totalJournalData:
            journalButton = tk.Button(master = self.leftSection, text = noteData["title"],
                                      borderwidth = 0)
            journalButton.pack(side = tk.TOP, fill = tk.X)
            journalButton.bind("<Button-1>", self.lambdaMaker(noteData["creationTime"], journalButton))
            if not createdFirstButton:
                self.openJournal(noteData["creationTime"], journalButton)

            createdFirstButton = True



class LeftSection(tk.Frame):
    """
    Left section frame which includes search bar, notes treeview,
    new journal button
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#3d3d3d")
        self.width = 230
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.search_bar = self.create_search_bar()
        self.newButton = self.create_new_button()


    def create_new_button(self):
        #GroupFrame -> NewJournalButton
        newJournalButton = ttk.Button(master=self, text="New Journal")
        newJournalButton.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        return newJournalButton

    def create_search_bar(self):
        #GroupFrame -> SearchBar
        groupSearchBar = ttk.Entry(master=self)
        groupSearchBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=16)
        return groupSearchBar


class RightSection(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.scroller = self.create_scroll()
        self.text_body = TextBody(self)
        self.text_body.text["yscrollcommand"] = self.scroller.set
        self.scroller.config(command = self.text_body.text.yview)

    def create_scroll(self):
        # Scrollbar
        scrollbar = ttk.Scrollbar(master=self, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return scrollbar


class TextBody(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.pack(padx = 30, pady = 20, side = tk.LEFT)
        self.title_entry = self.create_title_entry()
        self.AIButton = self.create_ask_ai()
        self.text = self.create_body_text()
        self.title_entry.bind("<Button-1>", self.onTitleTextEntryClick)
        self.title_entry.bind("<FocusOut>", self.onTitleTextEntryUnfocus)
        self.text.bind("<Button-1>", self.onTextEntryClick)
        self.text.bind("<FocusOut>", self.onTextEntryUnfocus)

    def create_title_entry(self):
        #TextEntryFrame -> titleEntry
        entry = tk.Entry(master=self, font=("Arial", 16, "bold"), fg="gray", borderwidth=0, highlightthickness=0)
        entry.pack(side=tk.TOP, fill=tk.BOTH, pady=(0, 10))
        entry.insert(tk.END,"Add Title")
        return entry

    def onTitleTextEntryClick(self,event):  # clear Add Title text on focus
        if self.title_entry.get() == "Add Title":
            self.title_entry.delete(0, tk.END)
            self.title_entry.configure(fg = "white")

    def onTitleTextEntryUnfocus(self, event):
        if self.title_entry.get() == "":
            self.title_entry.insert(0, "Add Title")
            self.title_entry.configure(fg = "gray")

    def onTextEntryClick(self,event):  # clear Add body text on focus
        if self.text.get("1.0", tk.END) == "Add body\n":
            self.text.delete("1.0", tk.END)
            self.text.configure(fg = "white")

    def onTextEntryUnfocus(self, event):
        if self.text.get("1.0", tk.END).strip() == "":
            self.text.insert("1.0", "Add body")
            self.text.configure(fg = "gray")

    def create_ask_ai(self):
        AIButton = ttk.Button(master=self, text="Ask AI")
        AIButton.pack(side= tk.RIGHT, anchor="ne", pady=(20, 0))
        return AIButton

    def create_body_text(self):
        entry = tk.Text(master=self, font=("Arial"), borderwidth=0, highlightthickness=0,
                        spacing1 = 8, spacing3 = 8, spacing2=5, fg="gray")
        entry.pack(side=tk.TOP, fill=tk.BOTH)
        entry.insert(tk.END, "Add body")
        return entry




if __name__ == "__main__":
    root = main()