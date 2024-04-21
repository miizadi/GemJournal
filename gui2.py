# LAHacks
# Helena Sun
# helenays@uci.edu

import tkinter.ttk as ttk
import tkinter as tk
import sv_ttk
import threading
import time
from savedata import saveNote, readNotes
import chatbot

totalJournalData = None

journalButtonPointsToTimestamp = {} #this is so stupid
selectedTimestamp = None #probably causing a million bugs
selectedButton = None # also causing a million bugs
currentAIModel = None
currentAIConvo = None


class main(tk.Tk):
    """
    Main window/root
    """
    def __init__(self):
        super().__init__()
        self.geometry("1280x600")
        self.title("GemBook - Pyrobib")
        self.resizable(False, False)
        self.leftSection = LeftSection(self)
        self.rightSection = RightSection(self)
        self.leftSection.newButton.bind("<Button-1>", self.addJournal)
        self.rightSection.text_body.title_entry.bind("<KeyRelease>", self.autosave)
        self.rightSection.text_body.text.bind("<KeyRelease>", self.autosave)
        self.loadExistingJournals()
        sv_ttk.set_theme("dark")
        self.rightSection.text_body.AIButton.bind("<Button-1>", self.create_AI_chat_box)
        self.mainloop()

    def autosave(self, event):
        if selectedButton is None or selectedTimestamp is None:
            return
        thread = threading.Thread(target = saveNote, args = (
        self.rightSection.text_body.title_entry.get(), selectedTimestamp, "NoGroup",
            self.rightSection.text_body.text.get("1.0", tk.END)))
        thread.start()
        selectedButton.config(text = self.chaLim(self.rightSection.text_body.title_entry.get()))

    def chaLim(self, string):
        if len(string) > 20:
            return string[:20] + "..."
        return string

    def highlightButton(self, button):
        for child in self.leftSection.winfo_children():
            if child != self.leftSection.newButton and child != self.leftSection.search_bar:
                child.config(bg="#3d3d3d")
        button.config(bg="#1c1c1c")

    def openJournal(self, creationTime, buttonObject):
        global totalJournalData
        totalJournalData = readNotes()
        global selectedButton
        selectedButton = buttonObject
        self.highlightButton(selectedButton)
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

                if journalData['body'].strip() != "Add body" or not journalData["body"]:
                    self.rightSection.text_body.text.configure(fg="white")

                if journalData["body"] != "" and journalData["body"] != "\n":
                    self.rightSection.text_body.text.delete("1.0", tk.END)
                    self.rightSection.text_body.text.insert("1.0", "Add body")
                    self.rightSection.text_body.text.config(fg="gray")
                else:
                    self.rightSection.text_body.text.delete("1.0", tk.END)
                    self.rightSection.text_body.text.insert("1.0", journalData["body"])
                    self.rightSection.text_body.text.config(fg="white")


                self.rightSection.text_body.pack(padx = 30, pady = 20, side = tk.LEFT)

    def create_AI_chat_box(self, event):
        # record old note
        title_text = self.rightSection.text_body.title_entry.get()
        body_text = self.rightSection.text_body.text.get("1.0", tk.END)
        # redo all of right section
        self.rightSection.scroller.destroy()
        self.rightSection.text_body.destroy()
        self.rightSection.AI_chat = AIChat(self.rightSection)
        self.rightSection.scroller = self.rightSection.create_scroll()
        self.rightSection.text_body = TextBody(self, True)
        self.rightSection.text_body.text.bind("<Button-1>", self.autosave)
        self.rightSection.text_body.title_entry.bind("<Button-1>", self.autosave)
        self.rightSection.text_body.text["yscrollcommand"] = self.rightSection.scroller.set

        self.rightSection.scroller.config(command = self.rightSection.text_body.text.yview)
        self.rightSection.text_body.title_entry.delete(0, tk.END)
        if title_text != "Add Title":
            self.rightSection.text_body.title_entry.configure(fg = "white")
        if body_text.strip() != "Add body":
            self.rightSection.text_body.text.configure(fg = "white")
        self.rightSection.text_body.title_entry.insert(tk.END, title_text)
        self.rightSection.text_body.text.delete("1.0", tk.END)
        self.rightSection.text_body.text.insert(tk.END, body_text)
        self.rightSection.text_body.text["yscrollcommand"] = self.rightSection.scroller.set
        self.rightSection.scroller.config(command = self.rightSection.text_body.text.yview)
        self.rightSection.AI_chat.close_AI.bind("<Button-1>", self.close_AI_chat_box)
        # user cannot edit note while chatting with AI
        self.rightSection.text_body.text.configure(state = 'disabled')
        self.rightSection.text_body.title_entry.configure(disabledbackground="#1c1c1c", state = 'disabled',
                                                          disabledforeground="white")
        self.rightSection.initializeAI()

    def close_AI_chat_box(self, event):
        title_text = self.rightSection.text_body.title_entry.get()
        body_text = self.rightSection.text_body.text.get("1.0", tk.END)
        if self.rightSection.AI_chat:
            self.rightSection.AI_chat.destroy()
        self.rightSection.text_body.destroy()
        self.rightSection.text_body = TextBody(self, False)
        self.rightSection.text_body.text["yscrollcommand"] = self.rightSection.scroller.set
        self.rightSection.scroller.config(command = self.rightSection.text_body.text.yview)
        self.rightSection.text_body.title_entry.delete(0, tk.END)
        if title_text != "Add Title":
            self.rightSection.text_body.title_entry.configure(fg = "white")
        if body_text.strip() != "Add body":
            self.rightSection.text_body.text.configure(fg = "white")
        self.rightSection.text_body.title_entry.insert(tk.END, title_text)
        self.rightSection.text_body.text.delete("1.0", tk.END)
        self.rightSection.text_body.text.insert(tk.END, body_text)
        self.rightSection.text_body.text["yscrollcommand"] = self.rightSection.scroller.set
        self.rightSection.scroller.config(command = self.rightSection.text_body.text.yview)
        self.rightSection.text_body.AIButton.bind("<Button-1>", self.create_AI_chat_box)

    def addJournal(self, event):
        #journalButton = tk.Button(master = self.leftSection, text = "Unnamed Journal", borderwidth = 0, bg="")
        #journalButton.pack(side = tk.TOP, fill = tk.X)
        title = "Unnamed Journal"
        creationTime = time.time()
        group = "NoGroup"
        body = ""
        saveNote(title, creationTime, group, body)
        self.loadExistingJournals() # this will automatically open the new journal

    def lambdaMaker(self, thing, buttonObject):
        return lambda e: self.openJournal(thing, buttonObject)

    # Load existing notes
    def loadExistingJournals(self):
        global totalJournalData
        totalJournalData = readNotes()

        for child in self.leftSection.winfo_children():
            if child != self.leftSection.newButton and child != self.leftSection.search_bar:
                child.destroy()

        createdFirstButton = False

        for noteData in totalJournalData:
            journalButton = tk.Button(master = self.leftSection, text = self.chaLim(noteData["title"]),
                                      borderwidth = 0, bg="#3d3d3d")
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
        self.text_body = TextBody(self, False)
        self.text_body.text["yscrollcommand"] = self.scroller.set
        self.scroller.config(command = self.text_body.text.yview)
        self.AI_chat = None


    def initializeAI(self):
        # set up AI
        global currentAIModel
        chatbot.configure_api()
        currentAIModel = chatbot.initialize_model()
        chatbot.ai_prompt_training(currentAIModel)
        global currentAIConvo
        currentAIConvo = chatbot.start_conversation(currentAIModel)

    def create_scroll(self):
        # Scrollbar
        scrollbar = ttk.Scrollbar(master=self, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return scrollbar


class AIChat(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=100)
        self.pack(padx=10, side = tk.RIGHT, fill = tk.Y)
        self.button_frame = tk.Frame(master = self)
        self.button_frame.pack(pady = 5, side = tk.BOTTOM, fill = tk.X, expand = True)
        self.chat_frame = tk.Frame(master=self)
        self.chat_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.display_frame = tk.Frame(master=self.chat_frame)
        self.display_frame.pack(side=tk.TOP, fill=tk.X)
        self.scroller = self.create_scroller()
        self.chat_box = self.create_chat_box()
        self.scroller.config(command = self.chat_box.yview)
        self.msg_box = self.create_messanger()
        self.close_AI = self.create_close_AI()
        self.send_msg_button = self.create_send_msg()
        self.send_msg_button.bind("<Button-1>", self.send_msg)


    def create_scroller(self):
        scroller = ttk.Scrollbar(master=self.display_frame)
        scroller.pack(side=tk.RIGHT, fill=tk.Y)
        return scroller

    def create_chat_box(self):
        box = tk.Text(self.display_frame, state='disabled', yscrollcommand=self.scroller.set,
                      font=("Arial", 10))
        box.tag_configure('ai', justify = 'left')
        box.tag_config('user', justify = 'right')
        box.pack(pady = 10, side=tk.TOP, fill=tk.BOTH, expand=True)
        return box

    def create_messanger(self):
        box = tk.Text(self.chat_frame,font=("Arial", 10))
        box.pack(pady=5, side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        return box

    def create_close_AI(self):
        AIButton = ttk.Button(master=self.button_frame, text="Goodbye AI")
        AIButton.pack(pady=5, side= tk.LEFT)
        return AIButton

    def create_send_msg(self):
        button = ttk.Button(self.button_frame, text="Send")
        button.pack(pady=5, side=tk.RIGHT)
        return button

    def send_msg(self, event):
        msg = self.msg_box.get("1.0", tk.END)
        self.msg_box.delete("1.0", tk.END)
        timed_msg = time.ctime(time.time()) + "\n" + msg + "\n"
        self.chat_box.configure(state = 'normal')
        self.chat_box.insert(tk.END, timed_msg, 'user')
        self.chat_box.configure(state = 'disabled')

        totalJournalData = readNotes()
        contextMessage = "Here is the content of the journal entries that I have done recently: \n"
        for journalData in totalJournalData:
            contextMessage += "\n"
            contextMessage += "Title: " + journalData["title"] + "\n"
            contextMessage += journalData["body"] + "\n"

        contextMessage += "\nHere is what I am saying to you now: \n\""
        msg = contextMessage + msg + "\""

        print("sending response")
        print(msg)
        currentAIConvo.send_message(msg)
        response = currentAIConvo.last.text
        self.display_AI_msg(response)


    def display_AI_msg(self, msg):
        timed_msg = time.ctime(time.time()) + "\n" + msg + "\n"
        self.chat_box.configure(state = 'normal')
        self.chat_box.insert(tk.END, timed_msg, 'ai')
        self.chat_box.configure(state = 'disabled')


class TextBody(tk.Frame):
    def __init__(self, parent, AI):
        if not AI:
            super().__init__(parent)
            self.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        else:
            super().__init__(parent, width=50)
            self.pack(side=tk.BOTTOM, expand=False)
        self.pack(padx = 30, pady = 20, side = tk.LEFT)
        self.title_entry = self.create_title_entry()
        if not AI:
            self.AIButton = self.create_ask_ai()
        self.text = self.create_body_text()
        self.title_entry.bind("<Button-1>", self.onTitleTextEntryClick)
        self.title_entry.bind("<FocusOut>", self.onTitleTextEntryUnfocus)
        self.text.bind("<Button-1>", self.onTextEntryClick)
        self.text.bind("<FocusOut>", self.onTextEntryUnfocus)
        self.AI_chat = None

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