import tkFileDialog
from Tkinter import *


class MainWindow(Frame):
    def createWidgets(self):
        label_dirPath = Label(self, text="Directory Path: ")
        label_discBins = Label(self, text="Discretization Bins: ")
        button_build = Button(self, text="Build", command=self.build)
        button_classify = Button(self, text="Classify", command=self.classify)
        button_browse = Button(self, text="browse", command=self.browse)
        self.entry_dirPath = Entry(self)
        self.entry_discBins = Entry(self)

        label_dirPath.grid(row=0, columnspan=2, pady=25)
        label_discBins.grid(row=1, column=1, pady=25)
        self.entry_dirPath.grid(row=0, column=2, )
        self.entry_discBins.grid(row=1, column=2)
        button_browse.grid(row=0, column=3)
        button_build.grid(row=3, column=1, sticky=E, pady=15)
        button_classify.grid(row=3, column=2, sticky=E, pady=15)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def browse(self):
        print("browse")

        Tk().withdraw()
        self.filename = tkFileDialog.askdirectory()

        self.entry_dirPath.insert(0, self.filename)

    def build(self):
        print("build")

    def classify(self):
        print("classify")


root = Tk()
root.geometry("350x200")
app = MainWindow(master=root)
app.mainloop()
