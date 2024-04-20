# LAHacks
# Helena Sun
# helenays@uci.edu

import tkinter.ttk as ttk
import tkinter as tk

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
        self.mainloop()


class LeftSection(tk.Frame):
    """
    Left section frame which includes search bar, notes treeview,
    new journal button
    """
    def __init__(self, parent):
        super().__init__(parent, bg="green")
        self.width = 230
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.search_bar = self.create_search_bar()
        self.notesList = self.create_notes_list()
        self.newButton = self.create_new_button()

    def create_search_bar(self):
        #GroupFrame -> SearchBar
        groupSearchBar = ttk.Entry(master=self)
        groupSearchBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=16)
        return groupSearchBar

    def create_notes_list(self):
        # create the treeview of list of journals
        journalList = ttk.Treeview(master=self)
        journalList.pack(side=tk.TOP, fill=tk.BOTH)
        return journalList

    def create_new_button(self):
        #GroupFrame -> NewJournalButton
        newJournalButton = ttk.Button(master=self, text="New Journal")
        newJournalButton.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        return newJournalButton


class RightSection(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="blue")
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.scroller = self.create_scroll()
        self.text_body = TextBody(self)

    def create_scroll(self):
        # Scrollbar
        scrollbar = ttk.Scrollbar(master=self, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return scrollbar


class TextBody(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.title_entry = self.create_title_entry()
        self.AIButton = self.create_ask_ai()
        self.text_entry = self.create_body_entry()
    def create_title_entry(self):
        #TextEntryFrame -> titleEntry
        entry = tk.Entry(master=self, font=("Arial", 16, "bold"), fg="gray", borderwidth=0, highlightthickness=0)
        entry.pack(side=tk.TOP, fill=tk.BOTH)
        return entry

    def create_ask_ai(self):
        AIButton = ttk.Button(master=self, text="Ask AI")
        AIButton.pack(side=tk.RIGHT)
        return AIButton

    def create_body_entry(self):
        entry = tk.Entry(master=self, font=("Arial", 12), fg='gray', borderwidth=0, highlightthickness=0)
        entry.pack(side=tk.TOP, fill=tk.BOTH)
        return entry


if __name__ == "__main__":
    root = main()