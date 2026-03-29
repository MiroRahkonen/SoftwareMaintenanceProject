from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
import config
import components


def createDecorations(self):
    # --------------- title ---------------------
    headerLabel = components.createLabel(
        self.root,
        text="View Customer Bills",
        font=("goudy old style", 30),
        background="#184a45",
        fg="white"
    )
    headerLabel.bd = 3
    headerLabel.relief = RIDGE
    headerLabel.pack(side=TOP, fill=X, padx=10, pady=20)

    searchLabel = components.createLabel(self.root,text="Invoice No.",position=[50,100])
    self.billSearchText = components.createEntry(self.root,textvariable=self.searchStringVar,position=[160,100],height=28)

    searchButton = components.createButton(
        self.root,
        text="Search",
        command=self.searchBill,
        font=("goudy old style",18),
        background="#2196f3",
        position=[360,100],
        width=120,
        height=28
    )

    clearTextButton = components.createButton(
        self.root, 
        text="Clear", 
        command=self.clearTextFields,
        font=("times new roman", 15, "bold"),
        background="lightgray",
        position=[490,100],
        width=120,
        height=28
    )

    self.billImage = components.createImage(path="images/cat2.jpg",size=[450,300])
    imageLabel = components.createImageLabel(self.root,image=self.billImage,position=[700,110])

def createBillsListFrame(self):
    # ----------------- bill list -------------------
    billFrame = components.createFrame(
        self.root,
        bd=3,
        position=[50,140],
        width=200,
        height=330
    )
    self.billList = components.createListbox(billFrame,self.getDataFromList)

def createBillDisplayFrame(self):
    # --------------- bill area ----------------------
    billFrame = components.createFrame(self.root,bd=3,position=[280,140],width=410,height=330)

    components.createLabel(
        billFrame,
        text="Customer Bill Area",
        font=("goudy old style",20),
        background="orange"
    ).pack(side=TOP, fill=X)

    billScrollbar = Scrollbar(billFrame, orient=VERTICAL)
    self.billTextArea = Text(billFrame, background="lightyellow", yscrollcommand=billScrollbar.set)
    billScrollbar.pack(side=RIGHT, fill=Y)
    billScrollbar.config(command=self.billTextArea.yview)
    self.billTextArea.pack(fill=BOTH, expand=1)


class Sales:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(background="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # Reused variables
        self.allBills = []

        # Tkinter StringVar variables
        self.searchStringVar = StringVar()

        # Initialize Interface
        createDecorations(self)
        createBillsListFrame(self)
        createBillDisplayFrame(self)
        self.updateBillsList()

    # -------------------------------------------------------
    def updateBillsList(self):
        del self.allBills[:]
        self.billList.delete(0, END)

        for bill in os.listdir(config.billsDirectory):
            if bill.split('.')[-1] == 'txt':
                self.billList.insert(END, bill)
                self.allBills.append(bill.split('.')[0])
            
    def getDataFromList(self, ev):
        index = self.billList.curselection()
        if not index:
            return

        fileName = self.billList.get(index)
        self.billTextArea.delete('1.0', END)

        filePath = os.path.join(config.billsDirectory, fileName)
        with open(filePath, 'r') as fp:
            for bill in fp:
                self.billTextArea.insert(END, bill)

    def searchBill(self):
        searchInput = self.searchStringVar.get()

        if searchInput == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
            return

        if searchInput in self.allBills:
            filePath = os.path.join(config.billsDirectory, f"{searchInput}.txt")
            self.billTextArea.delete('1.0', END)

            with open(filePath, 'r') as fp:
                for bill in fp:
                    self.billTextArea.insert(END, bill)
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clearTextFields(self):
        self.updateBillsList()
        self.searchStringVar.set("")
        self.billTextArea.delete('1.0', END)

if __name__ == "__main__":
    root = Tk()
    obj = Sales(root)
    root.mainloop()