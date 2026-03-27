from tkinter import *
from tkinter import messagebox
import time
import sqlite3
import os
import config
import components

from employee import Employee
from supplier import Supplier
from category import Category
from product import Product
from sales import Sales
from billing import Billing

def createNavigationMenu(self):
    # List of interface names and the commands that buttons will execute
    menuButtons = ["Employee", "Supplier", "Category", "Products", "Sales", "Billing", "Exit"]
    buttonCommands = [
        self.openEmployeeWindow,
        self.openSupplierWindow,
        self.openCategoryWindow,
        self.openProductWindow,
        self.openSalesWindow,
        self.openBillingWindow,
        self.root.destroy
    ]

    self.navigationImage = components.createImage(path="images/menu_im.png",size=[200,200])
    self.navigationArrow = components.createImage(path="images/side.png")

    navigationMenu = components.createFrame(
        self.root,
        bd=2,
        position=[0,102],
        width=200,
        height=620
    )
    navigationImage = components.createImageLabel(navigationMenu,image=self.navigationImage)
    navigationImage.pack(side=TOP, fill=X)
    
    components.createLabel(
        navigationMenu,
        text="Menu",
        font=("times new roman",20),
        background="#009688"
    ).pack(side=TOP, fill=X)
    
    # Create all buttons in navigation menu
    for index in range(len(menuButtons)):
        newButton = components.createNavigationButton(
            navigationMenu,
            text=menuButtons[index],
            command=buttonCommands[index],
            image=self.navigationArrow
        )

def createCategoryLabels(self):    
    self.employeeLabel = components.createDashboardLabel(
        self.root,
        text="Total Employee\n{ 0 }",
        background="#33bbf9",
        position=[300,120]
    )
    self.supplierLabel = components.createDashboardLabel(
        self.root,
        text="Total Supplier\n{ 0 }",
        background="#ff5722",
        position=[650,120]
    )
    self.categoryLabel = components.createDashboardLabel(
        self.root,
        text="Total Category\n{ 0 }",
        background="#009688",
        position=[1000,120]
    )
    self.productLabel = components.createDashboardLabel(
        self.root,
        text="Total Product\n{ 0 }",
        background="#607d8b",
        position=[300,300]
    )
    self.salesLabel = components.createDashboardLabel(
        self.root, 
        text="Total Sales\n{ 0 }",
        background="#ffc107",
        position=[650,300]
    )
    
    self.cashRegisterButton = components.createButton(
        self.root,
        text="Open Cash Register",
        font=("times new roman",20,"bold"),
        command=self.openBillingWindow,
        fg="white",
        background="#5e53ff",
        position=[650,520],
        width=300,
        height=150
    )

def createDecorations(self):
    self.titleImage = components.createImage(path="images/logo1.png")
    
    # Create window header
    header = Label(
        self.root,
        text="Inventory Management System",
        compound=LEFT,
        font=("times new roman",40,"bold"),
        fg="white",
        image= self.titleImage,
        background="#010c48",
        anchor="w",
        padx=20,
        height= 70,
    ).place(x=0,y=0,relwidth=1)

    # Create logout button
    logoutButton = components.createButton(
        self.root,
        text="Logout",
        command=self.root.destroy,
        font=("times new roman", 15, "bold"),
        background="yellow",
        fg="black",
        position=[1150,10],
        height=50,
        width=150
    )

    # Create footer label
    components.createLabel(
        self.root,
        font=("times new roman",12),
        text="IMS-Inventory Management System",
        background="#4d636d",
        fg="white"
    ).pack(side=BOTTOM, fill=X)

def createClockFrame(self):
    self.clockLabel = Label(
        self.root,
        background="#4d636d",
        fg="white",
        text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
        font=("times new roman", 15, "bold")
    )
    self.clockLabel.place(
        x=0,
        y=70,
        height= 30,
        relwidth=1
    )


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x750+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # Initialize Interface
        createDecorations(self) 
        createNavigationMenu(self)
        createClockFrame(self)
        createCategoryLabels(self)
        
        self.updateInventoryQuantities()
        self.updateClock()

    # -------------- functions ----------------
    def updateInventoryQuantities(self):
        connection = sqlite3.connect(database=os.path.join(config.baseDirectory, config.databaseURL))
        cursor = connection.cursor()
        try:
            cursor.execute("select * from product")
            product = cursor.fetchall()
            self.productLabel.config(text=f"Total Product\n[ {len(product)} ]")     
            cursor.execute("select * from category")
            category = cursor.fetchall()
            self.categoryLabel.config(text=f"Total Category\n[ {len(category)} ]")      
            cursor.execute("select * from employee")
            employee = cursor.fetchall()
            self.employeeLabel.config(text=f"Total Employee\n[ {len(employee)} ]")      
            cursor.execute("select * from supplier")
            supplier = cursor.fetchall()
            self.supplierLabel.config(text=f"Total Supplier\n[ {len(supplier)} ]")      
            sale = len(os.listdir(config.billsDirectory))
            self.salesLabel.config(text=f"Total Sales\n[ {sale} ]")     
        except Exception as error:
            messagebox.showerror("Error", f"Error due to : {str(error)}", parent=self.root)

    def openEmployeeWindow(self):
        self.employeeWindow = Toplevel(self.root)
        self.windowObject = Employee(self.employeeWindow)

    def openSupplierWindow(self):
        self.supplierWindow = Toplevel(self.root)
        self.windowObject = Supplier(self.supplierWindow)

    def openCategoryWindow(self):
        self.categoryWindow = Toplevel(self.root)
        self.windowObject = Category(self.categoryWindow)

    def openProductWindow(self):
        self.productWindow = Toplevel(self.root)
        self.windowObject = Product(self.productWindow)

    def openSalesWindow(self):
        self.salesWindow = Toplevel(self.root)
        self.windowObject = Sales(self.salesWindow)

    def openBillingWindow(self):
        self.billingWindow = Toplevel(self.root)
        self.windowObject = Billing(self.billingWindow)

    def updateClock(self):
        systemTime = time.strftime("%I:%M:%S")
        systemDate = time.strftime("%d-%m-%Y")

        # Updating clock timer
        self.clockLabel.config(
            text=f"Welcome to Inventory Management System\t\t Date: {systemDate}\t\t Time: {systemTime}"
        )
        self.clockLabel.after(200, self.updateClock)


if __name__ == "__main__":
    root = Tk()
    obj = Dashboard(root)
    root.mainloop()