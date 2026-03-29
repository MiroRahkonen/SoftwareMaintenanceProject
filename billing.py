from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
import config
import components

def createDecoration(self):
    # Create header
    header = Label(
        self.root,
        text="Inventory Management System",
        compound=LEFT,
        font=("times new roman",40,"bold"),
        background="#010c48",
        fg="white",
        anchor="w",
        padx=20
    ).place(x=0,y=0,relwidth=1,height=70)
    
    # Create logout button
    logoutButton = components.createButton(
        self.root,
        text="Logout",
        font=("times new roman", 15, "bold"),
        fg="black",
        background="yellow",
        command=self.root.destroy,
        position=[1150,10],
        height=50,
        width=150
    )

    # Create clock
    self.clockLabel = components.createLabel(
        self.root,
        text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
        fg="white",
        background="#4d636d",
        position=[0,70],
    )
    self.clockLabel.place(relwidth=1, height=30)

def createProductListFrame(self):
    # Create product frame
    productFrame = components.createFrame(
        self.root,
        bd=4,
        position=[6,110],
        width=410,
        height=550
    )

    components.createLabel(
        productFrame,
        text="All Products",
        font=("goudy old style",20,"bold"),
        fg="white",
        background="#262626"
    ).pack(side=TOP,fill=X)
    

    productSearchFrame = components.createFrame(productFrame,bd=2,position=[2,42],width=398,height=90)

    components.createLabel(
        productSearchFrame,
        text="Search Product | By Name",
        font=("times new roman",15,"bold"),
        fg="green",
        position=[2,5]
    )
    
    components.createLabel(
        productSearchFrame,
        text="Product Name",
        font=("times new roman",15,"bold"),
        position=[2,45]
    )

    productSearchInput = components.createEntry(
        productSearchFrame,
        textvariable=self.productSearchStringVar,
        font=("times new roman",15,"bold"),
        position=[128,47],
        width=150,
        height=22
    )

    searchButton = components.createButton(
        productSearchFrame,
        text="Search",
        command=self.searchProduct,
        background="#2196f3",
        position=[285,45],
        width=100,
        height=25
    )

    showAllButton = components.createButton(
        productSearchFrame,
        text="Show All",
        command=self.showCart,
        background="#083531",
        position=[285,10],
        width=100,
        height=25
    )

    productListFrame = components.createFrame(
        productFrame,
        bd=3,
        position=[2,140],
        width=398,
        height=375
    )

    self.productTable = components.createTreeview(
        productListFrame,
        command=self.getProductData,
        columns=("pid","name","price","qty","status"),
        headers=("P ID", "Name","Price","Quantity","Status"),
        columnWidths=(40,100,80,70,70)
    )

    noteLabel = components.createLabel(
        productFrame,
        text="Note: 'Enter 0 Quantity to remove product from the Cart'",
        font=("goudy old style",12),
        background="white",
        fg="red"
    )
    noteLabel.pack(side=BOTTOM,fill=X)
    noteLabel.anchor = "w"

def createCustomerDetailsFrame(self):
    customerDetailsFrame = components.createFrame(
        self.root, 
        bd=4, 
        position=[420,110], 
        width=530, 
        height=70
    )
    
    # Create Header
    components.createLabel(
        customerDetailsFrame,
        text="Customer Details",
        fg="black",
        background="lightgray"
    ).pack(side=TOP,fill=X)

    # Create Customer Name Entry
    components.createLabel(
        customerDetailsFrame,
        text="Name",
        font=("times new roman",15),
        position=[5,35])
    nameEntry = components.createEntry(
        customerDetailsFrame,
        textvariable=self.customerNameStringVar,
        font=("times new roman",13),
        position=[80,35],
        width=180
    )

    # Create Contact No. entry
    components.createLabel(
        customerDetailsFrame,
        text="Contact No.",
        font=("times new roman",15),
        position=[270,35]
    )
    contactNoEntry = components.createEntry(
        customerDetailsFrame,
        textvariable=self.customerContactStringVar,
        font=("times new roman",15),
        position=[380,35],
        width=140
    )

def createCalculatorFrame(self):
    self.calculatorContainer = components.createFrame(
        self.root,
        bd=2,
        position=[420,190],
        width=530,
        height=360
    )

    calculatorFrame = components.createFrame(
        self.calculatorContainer,
        bd=9,
        position=[5,10],
        width=268,
        height=340
    )

    self.calculatorEntry = Entry(
        calculatorFrame,
        textvariable=self.calculatorStringVar,
        font=('arial',15,'bold'),
        width=21,
        bd=10,
        relief=GROOVE,
        state='readonly',
        justify=RIGHT
    )
    self.calculatorEntry.grid(row=0,columnspan=4)

    components.createCalculatorButton(calculatorFrame,text=7,command=lambda:self.getCalculatorInput(7),row=1,column=0)
    components.createCalculatorButton(calculatorFrame,text=8,command=lambda:self.getCalculatorInput(8),row=1,column=1)
    components.createCalculatorButton(calculatorFrame,text=9,command=lambda:self.getCalculatorInput(9),row=1,column=2)
    components.createCalculatorButton(calculatorFrame,text="+",command=lambda:self.getCalculatorInput('+'),row=1,column=3)

    components.createCalculatorButton(calculatorFrame,text=4,command=lambda:self.getCalculatorInput(4),row=2,column=0)
    components.createCalculatorButton(calculatorFrame,text=5,command=lambda:self.getCalculatorInput(5),row=2,column=1)
    components.createCalculatorButton(calculatorFrame,text=6,command=lambda:self.getCalculatorInput(6),row=2,column=2)
    components.createCalculatorButton(calculatorFrame,text="-",command=lambda:self.getCalculatorInput('-'),row=2,column=3)

    components.createCalculatorButton(calculatorFrame,text=1,command=lambda:self.getCalculatorInput(1),row=3,column=0)
    components.createCalculatorButton(calculatorFrame,text=2,command=lambda:self.getCalculatorInput(2),row=3,column=1)
    components.createCalculatorButton(calculatorFrame,text=3,command=lambda:self.getCalculatorInput(3),row=3,column=2)
    components.createCalculatorButton(calculatorFrame,text="*",command=lambda:self.getCalculatorInput('*'),row=3,column=3)

    components.createCalculatorButton(calculatorFrame,text=0,command=lambda:self.getCalculatorInput(0),pady=15,row=4,column=0)
    components.createCalculatorButton(calculatorFrame,text="C",command=self.clearCalculator,pady=15,row=4,column=1)
    components.createCalculatorButton(calculatorFrame,text="=",command=self.performCalculation,pady=15,row=4,column=2)
    components.createCalculatorButton(calculatorFrame,text="/",command=lambda:self.getCalculatorInput('/'),pady=15,row=4,column=3)

def createShoppingCartFrame(self):
    #------------------ cart frame --------------------
    self.cartFrame = components.createFrame(
        self.calculatorContainer,
        bd=3,
        position=[280,8],
        width=245,
        height=342
    )

    shoppingCart = components.createFrame(
        self.calculatorContainer,
        position=[280,8],
        width=245,
        height=342
    )

    self.productCountLabel = components.createLabel(
        self.cartFrame,
        text="Cart \t Total Products: [0]",
        background="lightgray"
    )
    self.productCountLabel.pack(side=TOP,fill=X)

    self.cartTable = components.createTreeview(
        shoppingCart,
        command=self.getCartData,
        columns=("pid","name","price","qty"),
        headers=("P ID","Name","Price","Quantity"),
        columnWidths=[40,100,90,30]
    )

def createProductInfoFrame(self):
    cartWidgetFrame = components.createFrame(
        self.root,
        bd=2,
        position=[420,550],
        width=530,
        height=110
    )

    components.createLabel(cartWidgetFrame,text="Product Name",position=[5,5])
    productNameEntry = components.createEntry(
        cartWidgetFrame,
        textvariable=self.productNameStringVar,
        font=("times new roman",15),
        position=[5,35],
        width=190,
        height=22
    )
    productNameEntry.state = "readonly"

    components.createLabel(cartWidgetFrame,text="Price Per Qty",position=[230,5])
    productPriceEntry = components.createEntry(
        cartWidgetFrame,
        textvariable=self.productPriceStringVar,
        font=("times new roman",15),
        position=[230,35],
        width=150,
        height=22
    )
    productPriceEntry.state = "readonly"

    components.createLabel(cartWidgetFrame,text="Quantity",position=[390,5])
    productQuantityEntry=Entry(cartWidgetFrame,textvariable=self.productQuantityStringVar,font=("times new roman",15),background="lightyellow").place(x=390,y=35,width=120,height=22)

    self.inStockLabel = components.createLabel(cartWidgetFrame,text="In Stock",position=[5,70])

    clearNewProductButton = components.createButton(
        cartWidgetFrame,
        command=self.clearNewProduct,
        text="Clear",
        background="lightgray",
        position=[180,70],
        width=150,
        height=30
    )
    
    addToCartButton = components.createButton(
        cartWidgetFrame,
        command=self.addToCart,
        text="Add | Update",
        font=("times new roman",15,"bold"),
        background="orange",
        position=[340,70],
        width=180,
        height=30
    )
        
def createCustomerBillFrame(self):
    billingFrame = components.createFrame(
        self.root,
        bd=2,
        position=[953,110],
        width=400,
        height=410
    )

    components.createLabel(
        billingFrame,
        text="Customer Bill Area",
        font=("goudy old style",20,"bold"),
        background="#262626",
        fg="white"
    ).pack(side=TOP,fill=X)

    scrolly=Scrollbar(billingFrame,orient=VERTICAL)
    scrolly.pack(side=RIGHT,fill=Y)

    self.billingListStringVar = Text(billingFrame,yscrollcommand=scrolly.set)
    self.billingListStringVar.pack(fill=BOTH,expand=1)
    scrolly.config(command=self.billingListStringVar.yview)

    billMenuFrame = components.createFrame(self.root,bd=2,position=[953,520],width=400,height=140)

    self.billAmountLabel= components.createLabel(
        billMenuFrame,
        text="Bill Amount\n[0]",
        font=("goudy old style",15,"bold"),
        background="#3f51b5",
        fg="white",
        position=[2,5],
    )
    self.billAmountLabel.place(width = 120, height = 70)
    
    discountLabel = components.createLabel(
        billMenuFrame,
        text="Discount\n[5%]",
        font=("goudy old style",15,"bold"),
        background="#8bc34a",
        fg="white",
        position=[124,5]
    )
    discountLabel.place(width = 120,height = 70) 

    self.netPayLabel=components.createLabel(
        billMenuFrame,
        text="Net Pay\n[0]",
        fg="white",
        font=("goudy old style",15,"bold"),
        background="#607d8b",
        position=[246,5]
    )
    self.netPayLabel.place(
        width = 160,
        height = 70
    )

    printButton = components.createButton(
        billMenuFrame,
        text="Print",
        command=self.printBill,
        font=("goudy old style",15,"bold"),
        background="lightgreen",
        fg="white",
        position=[2,80],
        width=120,
        height=50
    )

    clearNewProductButton = components.createButton(
        billMenuFrame,
        text="Clear All",
        command=self.clearTextInputs,
        font=("goudy old style",15,"bold"),
        background="gray",
        fg="white",
        position=[124,80],
        width=120,
        height=50
    )

    generateBillButton = components.createButton(
        billMenuFrame,
        text="Generate Bill",
        command=self.generateBill,
        font=("goudy old style",15,"bold"),
        background="#009688",
        fg="white",
        position=[246,80],
        width=160,
        height=50
    )

def checkIfInputsValid(self):
    if(self.productID == ""):
        messagebox.showerror("Error","Please select product from the list",parent=self.root)
        return False

    if(self.productQuantity == ""):
        messagebox.showerror("Error","Quantity is required",parent=self.root)
        return False
    if(int(self.productQuantity) > int(self.productStock)):
        messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        return False

    # All tests pass, return true
    return True


class Billing:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False,False)
        self.root.config(background="white")
        self.productsInCart = []
        self.isBillGenerated = False

        # Tkinter StringVar variables
        self.customerNameStringVar = StringVar()
        self.customerContactStringVar = StringVar()
        self.calculatorStringVar = StringVar()
        self.productSearchStringVar = StringVar()
        self.productIDStringVar = StringVar()
        self.productNameStringVar = StringVar()
        self.productPriceStringVar = StringVar()
        self.productQuantityStringVar = StringVar()
        self.productStockStringVar = StringVar()

        # Initialize Interface
        createDecoration(self)
        createProductListFrame(self)
        createCustomerDetailsFrame(self)
        createCalculatorFrame(self)
        createShoppingCartFrame(self)
        createProductInfoFrame(self)
        createCustomerBillFrame(self)

        self.displayProduct()
        self.generateBillTop()
        self.updateClock()
        self.fetchTextFromInputBoxes()
    
    # Functions
    def fetchTextFromInputBoxes(self):
        self.customerName = self.customerNameStringVar.get()
        self.customerContact = self.customerContactStringVar.get()
        
        self.billingListText = self.billingListStringVar.get('1.0',END)
        self.calculatorInput = self.calculatorStringVar.get()
        
        self.productSearch = self.productSearchStringVar.get()
        self.productID = self.productIDStringVar.get()
        self.productName = self.productNameStringVar.get()
        self.productPrice = self.productPriceStringVar.get()
        self.productQuantity = self.productQuantityStringVar.get()
        self.productStock = self.productStockStringVar.get()

    def getCalculatorInput(self,num):
        self.fetchTextFromInputBoxes()

        xnum = self.calculatorInput+str(num)
        self.calculatorStringVar.set(xnum)

    def clearCalculator(self):
        self.calculatorStringVar.set('')

    def performCalculation(self):
        self.fetchTextFromInputBoxes()
        
        result=self.calculatorInput
        self.calculatorStringVar.set(eval(result))

    def displayProduct(self):
        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("select pid,name,price,qty,status from product where status='Active'")
            productData = cursor.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for product in productData:
                self.productTable.insert('',END,values=product)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def searchProduct(self):
        self.fetchTextFromInputBoxes()

        if(self.productSearch == ""):
            messagebox.showerror("Error","Search input should be required",parent=self.root)
            return

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.productSearch+"%'")
            productData = cursor.fetchall()

            if(len(productData) == 0):
                messagebox.showerror("Error","No record found!!!",parent=self.root)
                return

            self.productTable.delete(*self.productTable.get_children())
            for product in productData:
                self.productTable.insert('',END,values=product)                
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def getProductData(self,ev):
        focus = self.productTable.focus()
        productData = (self.productTable.item(focus))
        productInfo = productData['values']
        
        # Stop if product is not found
        if not productInfo:
            return

        self.productIDStringVar.set(productInfo[0])
        self.productNameStringVar.set(productInfo[1])
        self.productPriceStringVar.set(productInfo[2])
        self.inStockLabel.config(text=f"In Stock [{str(productInfo[3])}]")
        self.productStockStringVar.set(productInfo[3])
        self.productQuantityStringVar.set('1')
    
    def getCartData(self,ev):
        focus = self.cartTable.focus()
        cartData = (self.cartTable.item(focus))

        productInfo = cartData['values']
        
        # Stop if product is not found
        if not productInfo:
            return

        self.productIDStringVar.set(productInfo[0])
        self.productNameStringVar.set(productInfo[1])
        self.productPriceStringVar.set(productInfo[2])
        self.productQuantityStringVar.set(productInfo[3])
        self.inStockLabel.config(text=f"In Stock [{str(pproductInfo[4])}]")
        self.productStockStringVar.set(productInfo[4])
        
    def addToCart(self):
        self.fetchTextFromInputBoxes()

        if(checkIfInputsValid(self) == False):
            return
        
        cartData=[self.productID,self.productName,self.productPrice,self.productQuantity,self.productStock]

        present = "no"
        index = 0
        for product in self.productsInCart:
            if(self.productID == product[0]):
                present="yes"
                break
            index+=1
        if(present == "yes"):
            self.productsInCart.append(cartData)
            confirmation=messagebox.askyesno("Confirm","Product already present\nDo you want to Update|Remove from the Cart List",parent=self.root)
            if(confirmation == False):
                return

            if(self.productQuantity == "0"):
                self.productsInCart.pop(inderror)
            else:
                self.productsInCart[index][3]=self.productQuantity
        else:
            self.productsInCar.append(cartData)
        self.showCart()
        self.updateBill()

    def updateBill(self):
        self.billAmount=0
        self.netPay=0
        self.discount=0
        for product in self.productsInCart:
            self.billAmount=self.billAmount+(float(product[2])*int(product[3]))
        self.discount=(self.billAmount*5)/100
        self.netPay=self.billAmount-self.discount
        self.billAmountLabel.config(text=f"Bill Amount\n{str(self.billAmount)}")
        self.netPayLabel.config(text=f"Net Pay\n{str(self.netPay)}")
        self.productCountLabel.config(text=f"Cart \t Total Products: [{str(len(self.productsInCart))}]")

    def showCart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for product in self.productsInCart:
                self.cartTable.insert('',END,values=product)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def generateBill(self):
        self.fetchTextFromInputBoxes()

        if(self.customerName == "" or self.customerContact == ""):
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
            return

        if(self.customerContact.isdigit() == False):
            messagebox.showerror("Error",f"Contact number must be a number",parent=self.root)
            return

        if(len(self.productsInCart)==0):
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
            return
        
        # Create bill into interface
        self.generateBillTop()
        self.generateBillMiddle()
        self.generateBillBottom()

        fp=open(f'bills/{str(self.invoice)}.txt','w')
        fp.write(self.billingListText)
        fp.close()
        messagebox.showinfo("Saved","Bill has been generated",parent=self.root)
        self.isBillGenerated = True

    def generateBillTop(self):
        self.fetchTextFromInputBoxes()

        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        generateBillTopTemporary=f'''
        \t\tXYZ-Inventory
        \t Phone No. 9899459288 , Delhi-110053
        {str("="*46)}
         Customer Name: {self.customerName}
         Ph. no. : {self.customerContact}
         Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
        {str("="*46)}
         Product Name\t\t\tQTY\tPrice
        {str("="*46)}
        '''
        self.billingListStringVar.delete('1.0',END)
        self.billingListStringVar.insert('1.0',generateBillTopTemporary)
    
    def generateBillBottom(self):
        self.fetchTextFromInputBoxes()

        generateBillBottomTemporary=f'''
        {str("="*46)}
         Bill Amount\t\t\t\tRs.{self.billAmount}
         Discount\t\t\t\tRs.{self.discount}
         Net Pay\t\t\t\tRs.{self.netPay}
        {str("="*46)}\n
        '''
        self.billingListStringVar.insert(END,generateBillBottomTemporary)

    def generateBillMiddle(self):
        self.fetchTextFromInputBoxes()

        connection=sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            for product in self.productsInCart:
                pid = product[0]
                name = product[1]
                qty = int(product[4])-int(product[3])
                if(int(product[3]) == int(product[4])):
                    status="Inactive"
                if(int(product[3]) != int(product[4])):
                    status="Active"
                price=float(product[2])*int(product[3])
                price=str(price)
                self.billingListStringVar.insert(END,"\n "+name+"\t\t\t"+product[3]+"\tRs."+price)
                #------------- update qty in product table --------------
                cursor.execute("update product set qty=?,status=? where pid=?",(
                    qty,
                    status,
                    pid
                ))
                connection.commit()
            connection.close()
            self.displayProduct()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}",parent=self.root)

    def clearNewProduct(self):
        self.productIDStringVar.set("")
        self.productNameStringVar.set("")
        self.productPriceStringVar.set("")
        self.productQuantityStringVar.set("")
        self.inStockLabel.config(text=f"In Stock")
        self.productStockStringVar.set("")
    
    def printBill(self):
        if(self.isBillGenerated == False):
            messagebox.showinfo("Print","Please generate bill to print the receipt",parent=self.root)
            return

        messagebox.showinfo("Print","Please wait while printing",parent=self.root)
        newFile=tempfile.mktemp('.txt')
        open(newFile,'w').write(self.billingListText)
        os.startfile(newFile,'print')

    def clearTextInputs(self):
        del self.productsInCart[:]

        self.clearNewProduct()
        self.displayProduct()
        self.showCart()
        self.customerNameStringVar.set("")
        self.customerContactStringVar.set("")
        self.isBillGenerated = False
        self.billingListStringVar.delete('1.0',END)
        self.productCountLabel.config(text=f"Cart \t Total Products: [0]")
        self.productSearchStringVar.set("")
    
    def updateClock(self):
        currentTime=time.strftime("%I:%M:%S")
        currentDate=time.strftime("%d-%m-%Y")
        self.clockLabel.config(text=f"Welcome to Inventory Management System\t\t Date: {str(currentDate)}\t\t Time: {str(currentTime)}")
        self.clockLabel.after(200,self.updateClock)


if __name__=="__main__":
    root=Tk()
    obj=Billing(root)
    root.mainloop()