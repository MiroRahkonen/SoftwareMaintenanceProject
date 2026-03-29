from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
import config
import components

def createSupplierFrame(self):
    # Add Header
    headerLabel = components.createLabel(
        self.root,
        text="Supplier Details",
        font=("goudy old style",20,"bold"),
        background="#0f4d7d",
        fg="white",
        position=[50,10]
    )
    headerLabel.place(
        width = 1000,
        height=40
    )

    # Invoice Field
    components.createLabel(self.root,text="Invoice No.",position=[50,80])
    components.createEntry(self.root,textvariable=self.invoiceStringVar,position=[180,80])

    # Name Field
    components.createLabel(self.root,text="Name",position=[50,120])
    components.createEntry(self.root,textvariable=self.supplierStringVar,position=[180,120])

    # Contact Field
    components.createLabel(self.root,text="Contact",position=[50,160])
    components.createEntry(self.root,textvariable=self.nameStringVar,position=[180,160])

    # Description Field
    components.createLabel(self.root,text="Description",position=[50,200])
    self.descriptionText = components.createText(self.root,position=[180,200],width=470,height=120)

    # Create management buttons
    components.createButton(self.root,text="Save",command=self.addSupplier,background="#2196f3",position=[180,370])
    components.createButton(self.root,text="Update",command=self.updateSupplier,background="#4caf50",position=[300,370])
    components.createButton(self.root,text="Delete",command=self.deleteSupplier,background="#f44336",position=[420,370])
    components.createButton(self.root,text="Clear",command=self.clearTextFields,background="#607d8b",position=[540,370])

def createSearchFrame(self):
    components.createLabel(self.root,text="Invoice No.",position=[700,80])
    components.createEntry(self.root,textvariable=self.searchStringVar,position=[800,80],width=160)
    components.createButton(self.root, text="Search", command=self.searchInvoice,background="#4caf50", position=[980,79],width=100,height=28)
    
def createSupplierList(self):
    listFrame = components.createFrame(self.root,bd=3,position=[700,120], width=380,height=350)

    self.supplierTable = components.createTreeview(
        listFrame,
        command=self.getDataFromList,
        columns=("invoice","name","contact","desc"),
        headers=("Invoice","Name","Contact","Description"),
        columnWidths=(90,100,100,100)
    )

def checkIfInputsValid(self):
    if self.invoiceNumber == "":
        messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
        return False
    
    if(self.invoiceNumber.isdigit() == False):
        messagebox.showerror("Error","Invoice No. must be a number",parent=self.root)
        return False

    if self.supplierName == "" or self.supplierContact == "":
        messagebox.showerror("Error","All fields are required",parent=self.root)
        return False
    
    #All tests pass, return true
    return True


class Supplier:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(background="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        # Tkinter StringVar variables
        self.searchStringVar = StringVar()
        self.invoiceStringVar = StringVar()
        self.supplierStringVar = StringVar()
        self.nameStringVar = StringVar()

        ## Initialize Interface
        createSearchFrame(self)
        createSupplierFrame(self)
        createSupplierList(self)

        # Fetch data from database
        self.fetchSuppliers()
        self.fetchTextFromInputBoxes()

    def fetchTextFromInputBoxes(self):
        self.searchInput = self.searchStringVar.get()
        self.invoiceNumber = self.invoiceStringVar.get()
        self.supplierName = self.supplierStringVar.get()
        self.supplierContact = self.nameStringVar.get()
        self.supplierDescription = self.descriptionText.get('1.0',END)

    def fetchSuppliers(self):
        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("select * from supplier")
            response=cursor.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for supplier in response:
                self.supplierTable.insert('',END,values=supplier)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def addSupplier(self):
        self.fetchTextFromInputBoxes()
    
        if(checkIfInputsValid(self) == False):
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from supplier where invoice=?",(self.invoiceNumber,))
            response=cursor.fetchone()
            if response!=None:
                messagebox.showerror("Error","Invoice no. is already assigned",parent=self.root)
                return

            cursor.execute("insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                self.invoiceNumber,
                self.supplierName,
                self.supplierContact,
                self.supplierDescription,
            ))
            
            connection.commit()
            messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
            self.clearTextFields()
            self.fetchSuppliers()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def updateSupplier(self):
        self.fetchTextFromInputBoxes()

        if(checkIfInputsValid(self) == False):
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from supplier where invoice=?",(self.invoiceNumber,))
            response=cursor.fetchone()
            if response==None:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                return
            
            cursor.execute("update supplier set name=?,contact=?,desc=? where invoice=?",(
                self.supplierName,
                self.supplierContact,
                self.supplierDescription,
                self.invoiceNumber,
            ))
            connection.commit()
            messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
            self.fetchSuppliers()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def deleteSupplier(self):
        self.fetchTextFromInputBoxes()

        if(checkIfInputsValid(self) == False):
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from supplier where invoice=?",(self.invoiceNumber,))
            response=cursor.fetchone()
            if response==None:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                return
            
            userConfirmation=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
            if userConfirmation == False:
                return

            cursor.execute("delete from supplier where invoice=?",(self.invoiceNumber,))
            connection.commit()
            messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
            self.clearTextFields()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def clearTextFields(self):
        self.invoiceStringVar.set("")
        self.supplierStringVar.set("")
        self.nameStringVar.set("")
        self.descriptionText.delete('1.0',END)
        self.searchStringVar.set("")
        self.fetchSuppliers()

    def getDataFromList(self,ev):
        focus=self.supplierTable.focus()
        content=(self.supplierTable.item(focus))
        supplierListing=content['values']
        if(len(supplierListing) == 0):
            return
            
        self.invoiceStringVar.set(supplierListing[0])
        self.supplierStringVar.set(supplierListing[1])
        self.nameStringVar.set(supplierListing[2])
        self.descriptionText.delete('1.0',END)
        self.descriptionText.insert(END,supplierListing[3])

    def searchInvoice(self):
        self.fetchTextFromInputBoxes()

        if self.searchInput == "":
            messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("select * from supplier where invoice=?",(self.searchInput,))
            response=cursor.fetchone()
            if response!=None:
                self.supplierTable.delete(*self.supplierTable.get_children())
                self.supplierTable.insert('',END,values=response)
            else:
                messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

if __name__=="__main__":
    root=Tk()
    obj=Supplier(root)
    root.mainloop()