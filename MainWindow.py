import tkFileDialog
import tkMessageBox
import os.path
import math
from Tkinter import *

from Builder import Builder
from Classifier import Classifier


class MainWindow(Frame):
    def createWidgets(self):
        label_dirPath = Label(self, text="Directory Path: ")
        label_discBins = Label(self, text="Discretization Bins: ")
        button_build = Button(self, text="Build", command=self.build)
        button_classify = Button(self, text="Classify", command=self.classify)
        button_browse = Button(self, text="browse", command=self.browse)
        self.entry_dirPath = Entry(self)
        self.entry_bins = Entry(self)

        label_dirPath.grid(row=0, columnspan=2, pady=25)
        label_discBins.grid(row=1, column=1, pady=25)
        self.entry_dirPath.grid(row=0, column=2, )
        self.entry_bins.grid(row=1, column=2)
        button_browse.grid(row=0, column=3)
        button_build.grid(row=3, column=1, sticky=E, pady=15)
        button_classify.grid(row=3, column=2, sticky=E, pady=15)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.bins = None
        self.builder = None
        self.classifier = None
        self.pack()
        self.createWidgets()

    def browse(self):
        print("browse")
        self.entry_dirPath.delete(0, 'end')
        Tk().withdraw()
        self.filename = tkFileDialog.askdirectory()
        self.entry_dirPath.insert(0, self.filename)

    def build(self):
        print("build")
        path = self.entry_dirPath.get()
        if self.checkInput(path):
            self.builder = Builder(path, self.bins)
            try:
                Builder.build(self.builder)
                tkMessageBox.showinfo("Building Done", "Building classifier using train-set is done!")
            except:
                tkMessageBox.showinfo("Failed", "Something went wrong, please try again")

    def classify(self):
        print("classify")
        Builder.readTestSet(self.builder)
        self.classifier = Classifier(self.builder)
        Classifier.classify(self.classifier)
        tkMessageBox.showinfo("Classifying Done", "Finished classifying the test set.")

    def checkInput(self, path):
        print("checkInput")
        # check bins
        try:
            int(self.entry_bins.get())
        except ValueError:
            tkMessageBox.showinfo(title="error", message="Bins must be a number")
            return False

        self.bins = int(float(self.entry_bins.get()))
        if self.bins < 1:
            tkMessageBox.showinfo("Error", "Bad number of bins")
            return False

        # check path
        if not os.path.exists(path):
            tkMessageBox.showinfo("Error", "Path does not exist")
            return False

        # check all needed files exist in path
        pathToFiles = [path + "\\Structure.txt", path + "\\train.csv", path + "\\test.csv"]
        for pathToFile in pathToFiles:
            if os.path.exists(pathToFile) == False or (os.path.getsize(pathToFile) > 0) == False:
                tkMessageBox.showinfo(title="error", message="One or more of the needed files does not exist in the given path")
                return False
            if os.stat(pathToFile).st_size == 0:
                tkMessageBox.showinfo(title="error", message="One or more of the needed files are empty")
                return False

        return True



root = Tk()
root.geometry("350x200")
app = MainWindow(master=root)
app.mainloop()
