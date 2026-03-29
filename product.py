from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
import config
import components

def createProductFrame(self):
    labelFont = ("goudy old style",18)

    # Create frame for products
    self.productFrame = components.createFrame(
        self.root,
        bd=2,
        position=[10,10],
        width=450,
        height=480
    )

    headerLabel = components.createLabel(
        self.productFrame,
        text="Manage Product Details",
        font=("goudy old style",18),
        background="#0f4d7d",
        fg="white"
    )
    headerLabel.pack(side=TOP,fill=X)
    
    components.createLabel(self.productFrame,text="Category",font=labelFont, position=[30,60])
    components.createLabel(self.productFrame,text="Supplier",font=labelFont,position=[30,110])
    components.createLabel(self.productFrame,text="Name",font=labelFont,position=[30,160])
    components.createLabel(self.productFrame,text="Price",font=labelFont,position=[30,210])
    components.createLabel(self.productFrame,text="Quantity",font=labelFont,position=[30,260])
    components.createLabel(self.productFrame,text="Status",font=labelFont,position=[30,310])

    categoryCombobox = components.createCombobox(
        self.productFrame,
        textvariable=self.categoryStringVar,
        values=self.availableCategories,
        position=[150,60]
    )

    supplierCombobox = components.createCombobox(
        self.productFrame,
        textvariable=self.supplierStringVar,
        values=self.availableSuppliers,
        position=[150,110]
    )

    components.createEntry(self.productFrame, textvariable=self.nameStringVar, position=[150,160], width=200)
    components.createEntry(self.productFrame, textvariable=self.priceStringVar, position=[150,210], width=200)
    components.createEntry(self.productFrame, textvariable=self.quantityStringVar, position=[150,260], width=200)

    statusCombobox = components.createCombobox(
        self.productFrame,
        textvariable=self.statusStringVar,
        values=("Active","Inactive"),
        position=[150,310]
    )

    # Create product management buttons
    components.createButton(self.productFrame,text="Save",command=self.addProduct,background="#2196f3",position=[10,400],width=100,height=40)
    components.createButton(self.productFrame,text="Update",command=self.updateProduct,background="#4caf50",position=[120,400],width=100,height=40)
    components.createButton(self.productFrame,text="Delete",command=self.deleteProduct,background="#f44336",position=[230,400],width=100,height=40)
    components.createButton(self.productFrame,text="Clear",command=self.clearTextFields,background="#607d8b",position=[340,400],width=100,height=40)
    
def createSearchFrame(self):
    # Create search frame
    searchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,background="white")
    searchFrame.place(x=480,y=10,width=600,height=80)

    #------------ options ----------------
    searchCombobox = components.createCombobox(
        searchFrame,
        textvariable=self.searchTypeStringVar,
        values=("Select","Category","Supplier","Name"),
        position=[10,10],
        width=180
    )

    components.createEntry(searchFrame, textvariable=self.searchNameStringVar, position=[200,10])
    searchButton = components.createButton(searchFrame,text="Search",command=self.searchProduct,background="#4caf50",position=[410,9],width=150,height=30)

def createProductList(self):
    self.productTableFrame = components.createFrame(self.root,position=[480,100],width=600,height=390)

    self.productTable = components.createTreeview(
        self.productTableFrame,
        command=self.getDataFromList,
        columns=("pid","Category","Supplier","name","price","qty","status"),
        headers=("P ID","Category","Suppler","Name","Price","Quantity","Status"),
        columnWidths=(90,100,100,100,100,100,100)
    )

def fetchCategories(self):
    self.availableCategories.append("Empty")

    connection=sqlite3.connect(database=config.databaseURL)
    cursor=connection.cursor()
    try:
        cursor.execute("select name from category")
        response=cursor.fetchall()
        if len(response)>0:
            del self.availableCategories[:]
            self.availableCategories.append("Select")
            for category in response:
                self.availableCategories.append(category[0])
    except Exception as error:
        messagebox.showerror("Error",f"Error due to : {str(error)}")

def fetchSuppliers(self):
    self.availableSuppliers.append("Empty")
    connection=sqlite3.connect(database=config.databaseURL)
    cursor=connection.cursor()
    try:
        cursor.execute("select name from supplier")
        response=cursor.fetchall()
        if len(response)>0:
            del self.availableSuppliers[:]
            self.availableSuppliers.append("Select")
            for supplier in response:
                self.availableSuppliers.append(supplier[0])
    except Exception as error:
        messagebox.showerror("Error",f"Error due to : {str(error)}")    

def updateProductList(self):
    connection=sqlite3.connect(database=config.databaseURL)
    cursor=connection.cursor()
    try:
        cursor.execute("select * from product")
        response=cursor.fetchall()
        self.productTable.delete(*self.productTable.get_children())
        for product in response:
            self.productTable.insert('',END,values=product)
    except Exception as error:
        messagebox.showerror("Error",f"Error due to : {str(error)}")

def checkIfInputsValid(self):
    if(self.productCategory == "Select" or self.productCategory == "Empty"):
        messagebox.showerror("Error","All fields are required",parent=self.root)
        return False

    if(self.productSupplier == "Select" or self.productSupplier == "Empty"):
        messagebox.showerror("Error","All fields are required",parent=self.root)
        return False

    if(self.productName == "" or self.productPrice == "" or self.productQuantity == ""):
        messagebox.showerror("Error","All fields are required",parent=self.root)
        return False

    if(self.productPrice.isdigit() == False):
        messagebox.showerror("Error","Price must be a number",parent=self.root)
        return False

    if(self.productQuantity.isdigit == False):
        messagebox.showerror("Error","Quantity must be a number",parent=self.root)
        return False
    
    #All tests pass, return true
    return True

class Product:
    def __init__(self,root):
        # Reused variables 
        self.availableCategories = []
        self.availableSuppliers = []

        # Tkinter StringVar variables
        self.categoryStringVar = StringVar()
        self.idStringVar = StringVar()
        self.supplierStringVar = StringVar()
        self.nameStringVar = StringVar()
        self.priceStringVar = StringVar()
        self.quantityStringVar = StringVar()
        self.statusStringVar = StringVar()
        self.searchTypeStringVar = StringVar()
        self.searchNameStringVar = StringVar()

        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(background="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        
        # Initialize Interface
        fetchCategories(self)
        fetchSuppliers(self)
        createProductFrame(self)
        createSearchFrame(self)
        createProductList(self)

        updateProductList(self)

    def fetchTextFromInputBoxes(self):
        self.productCategory = self.categoryStringVar.get()
        self.productID = self.idStringVar.get()
        self.productSupplier = self.supplierStringVar.get()
        self.productName = self.nameStringVar.get()
        self.productPrice = self.priceStringVar.get()
        self.productQuantity = self.quantityStringVar.get()
        self.productStatus = self.statusStringVar.get()
        self.searchProductType = self.searchTypeStringVar.get()
        self.searchProductName = self.searchNameStringVar.get()

    def getDataFromList(self,ev):
        focus=self.productTable.focus()
        content=(self.productTable.item(focus))
        productListing=content['values']

        # Quit if an empty list is clicked
        if(len(productListing) == 0):
            return

        self.idStringVar.set(productListing[0])
        self.categoryStringVar.set(productListing[1])
        self.supplierStringVar.set(productListing[2])
        self.nameStringVar.set(productListing[3])
        self.priceStringVar.set(productListing[4])
        self.quantityStringVar.set(productListing[5])
        self.statusStringVar.set(productListing[6])

    def addProduct(self):
        self.fetchTextFromInputBoxes()

        if(checkIfInputsValid(self) == False):
            return

        # All checks pass, upload product to database
        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from product where name=?",(self.productName,))
            response=cursor.fetchone()
            if(response != None):
                messagebox.showerror("Error","Product already present",parent=self.root)
                return
            
            cursor.execute(
                "insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                self.productCategory,self.productSupplier,self.productName,self.productPrice,self.productQuantity,self.productStatus
            ))
            connection.commit()
            messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
            self.clearTextFields()
            updateProductList(self)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def updateProduct(self):
        self.fetchTextFromInputBoxes()

        if(checkIfInputsValid(self) == False):
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from product where pid=?",(self.productID))
            response=cursor.fetchone()
            if(response == None):
                messagebox.showerror("Error","Invalid Product",parent=self.root)
                return
           
            cursor.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                self.productCategory,self.productSupplier,self.productName,self.productPrice,self.productQuantity,self.productStatus,self.productID,
            ))
            connection.commit()
            messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
            updateProductList(self)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def deleteProduct(self):
        self.fetchTextFromInputBoxes()

        if(checkIfInputsValid(self) == False):
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from product where pid=?",(self.productID,))
            response=cursor.fetchone()
            if(response == None):
                messagebox.showerror("Error","Invalid Product",parent=self.root)
                return
            
            userConfirmation=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
            if(userConfirmation == True):
                cursor.execute("delete from product where pid=?",(self.productID,))
                connection.commit()
                messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                self.clearTextFields()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def searchProduct(self):
        self.fetchTextFromInputBoxes()

        if(self.searchProductType == "Select"):
            messagebox.showerror("Error","Select Search By option",parent=self.root)
            return
        if(self.searchProductName == ""):
            messagebox.showerror("Error","Search input should be required",parent=self.root)
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("select * from product where "+self.searchProductType+" LIKE '%"+self.searchProductName+"%'")
            response=cursor.fetchall()

            if len(response) == 0:
                messagebox.showerror("Error","No record found!!!",parent=self.root)
                return

            self.productTable.delete(*self.productTable.get_children())
            for product in response:
                self.productTable.insert('',END,values=product)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def clearTextFields(self):
        self.categoryStringVar.set("Select")
        self.supplierStringVar.set("Select")
        self.nameStringVar.set("")
        self.priceStringVar.set("")
        self.quantityStringVar.set("")
        self.statusStringVar.set("Active")
        self.idStringVar.set("")
        self.searchTypeStringVar.set("Select")
        self.searchNameStringVar.set("")
        updateProductList(self)

if __name__=="__main__":
    root=Tk()
    obj=Product(root)
    root.mainloop()