from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
import config
import components

def createWindowLayout(self):
    headerLabel = components.createLabel(
        self.root,
        text="Manage Product Category",
        font=("goudy old style",30),
        background="#184a45",
        fg="white"
    )
    headerLabel.bd = 3
    headerLabel.relief = RIDGE
    headerLabel.pack(side=TOP,fill=X,padx=10,pady=20)


    searchLabel = components.createLabel(
        self.root,
        text="Enter Category Name",
        font=("goudy old style",30),
        position=[50,100]
    )
    searchEntry = components.createEntry(
        self.root,
        textvariable=self.nameStringVar,
        font=("goudy old style",18),
        position=[50,170],
        width=300
    )

    addCategoryButton = components.createButton(
        self.root,
        text="ADD",
        font=("goudy old style",15),
        command=self.addCategory,
        background="#4caf50",
        position=[360,170],
        width=150,
        height=30
    )

    deleteButton = components.createButton(
        self.root,
        text="Delete",
        command=self.deleteCategory,
        font=("goudy old style",15),
        background="red",
        position=[520,170],
        width=150,
        height=30
    )

def createCategoryList(self):
     #------------ category details -------------
    categoryFrame = components.createFrame(
        self.root,
        bd=3,
        position=[700,100],
        width=380,
        height=100
    )

    self.categoryTable = components.createTreeview(
        categoryFrame,
        self.getDataFromList,
        columns=("cid","name"),
        headers=("C ID", "Name"),
        columnWidths=(90,100)
    )

def createImages(self):
    self.imageLeft = components.createImage(path="images/cat.jpg",size=[500,250])
    components.createImageLabel(self.root,image=self.imageLeft,position=[50,220])

    self.imageRight = components.createImage(path="images/category.jpg",size=[500,250])
    components.createImageLabel(self.root,image=self.imageRight,position=[580,220])

class Category:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(background="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        # Tkinter StringVar variables
        self.idStringVar = StringVar()
        self.nameStringVar = StringVar()

        # Initialize Interface
        createWindowLayout(self)
        createCategoryList(self)
        createImages(self)
        
        self.updateCategoryList()
        self.fetchTextFromInputBoxes()
        
    #---Functions---------
    def fetchTextFromInputBoxes(self):
        self.categoryID = self.idStringVar.get()
        self.categoryName = self.nameStringVar.get()

    def addCategory(self):
        self.fetchTextFromInputBoxes()
        if self.categoryName == "":
            messagebox.showerror("Error","Category Name must be required",parent=self.root)
            return

        connection = sqlite3.connect(database=config.databaseURL)
        cursor = connection.cursor()
        try:
            cursor.execute("Select * from category where name=?",(self.categoryName,))
            category=cursor.fetchone()
            if category != None:
                messagebox.showerror("Error","Category already present",parent=self.root)
                return

            cursor.execute("insert into category(name) values(?)",(
                self.categoryName,
            ))
            connection.commit()
            messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
            self.clearTextInputs()
            self.updateCategoryList()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def updateCategoryList(self):
        connection = sqlite3.connect(database=config.databaseURL)
        cursor = connection.cursor()
        try:
            cursor.execute("select * from category")
            storedCategories = cursor.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for category in storedCategories:
                self.categoryTable.insert('',END,values=category)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")
    
    def clearTextInputs(self):
        self.nameStringVar.set("")
        self.updateCategoryList()

    def getDataFromList(self,ev):
        focus = self.categoryTable.focus()
        categories = (self.categoryTable.item(focus))
        category = categories['values']
        self.idStringVar.set(category[0])
        self.nameStringVar.set(category[1])
    
    def deleteCategory(self):
        self.fetchTextFromInputBoxes()
        
        if self.categoryName == "":
            messagebox.showerror("Error","Category name must be required",parent=self.root)
            return

        connection = sqlite3.connect(database=config.databaseURL)
        cursor = connection.cursor()
        try:
            cursor.execute("Select * from category where name=?",(self.categoryName,))
            response = cursor.fetchone()
            if response == None:
                messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                return
                
            confirmation = messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
            if confirmation == False:
                return
            
            cursor.execute("delete from category where name=?",(self.categoryName,))
            connection.commit()
            messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
            self.clearTextInputs()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

if __name__=="__main__":
    root=Tk()
    obj=Category(root)
    root.mainloop()