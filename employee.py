from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
import config
import components

def createSearchFrame(self):
    #---------- Search Frame -------------
    searchFrame = LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
    searchFrame.place(x=250,y=20,width=600,height=70)

    # Search Options
    searchCombobox = components.createCombobox(
        searchFrame,
        textvariable=self.searchTypeStringVar,
        values=("Select","Email","Name","Contact"),
        position=[10,10]
    )

    searchEntry = components.createEntry(searchFrame,textvariable=self.searchTextStringVar,width=180,position=[220,10])
    
    searchButton = components.createButton(
        searchFrame,
        command=self.searchEmployee,
        text="Search",
        background="#4caf50",
        position=[410,9],
        width=150,
        height=30
    )

def createDecorations(self):
    headerLabel = components.createLabel(
        self.root,
        text="Employee Details",
        background="#0f4d7d",
        fg="white",
        position=[50,100]
    )
    headerLabel.place(
        width = 1000
    )

def createEmployeeFrame(self):
    # Top input boxes
    components.createLabel(self.root,text="Emp ID",position=[60,150])
    components.createLabel(self.root,text="Gender",position=[420,150])
    components.createLabel(self.root,text="Contact",position=[775,150])

    employeeIDEntry = components.createEntry(self.root,textvariable=self.idStringVar,position=[150,150])

    genderCombobox = components.createCombobox(
        self.root,
        textvariable=self.genderStringVar,
        values=("Select","Male","Female","Other"),
        position=[500,150]
    )
    
    contactEntry = components.createEntry(self.root,textvariable=self.contactStringVar,position=[850,150])

    # Second row input boxes
    components.createLabel(self.root,text="Name",position=[60,190])
    components.createLabel(self.root,text="D.O.B.",position=[420,190])
    components.createLabel(self.root,text="D.O.J.",position=[775,190])

    nameEntry = components.createEntry(self.root,textvariable=self.nameStringVar,position=[150,190])
    dobEntry = components.createEntry(self.root,textvariable=self.dobStringVar,position=[500,190])
    doJEntry = components.createEntry(self.root,textvariable=self.dojStringVar,position=[850,190])

    # Third row input boxes
    components.createLabel(self.root,text="Email",position=[60,230])
    components.createLabel(self.root,text="Password",position=[420,230])
    components.createLabel(self.root,text="User Type",position=[760,230])

    emailEntry = components.createEntry(self.root,textvariable=self.emailStringVar,position=[150,230])
    passwordEntry = components.createEntry(self.root,textvariable=self.passwordStringVar,position=[500,230])

    userTypeCombobox = components.createCombobox(
        self.root,
        textvariable=self.usertypeStringVar,
        values=("Admin","Employee"),
        position=[850,230]
    )
    
    # Bottom input boxes
    components.createLabel(self.root,text="Address",position=[60,270])
    self.addressStringVar = components.createText(self.root, position=[150,270], width=300, height=60)

    components.createLabel(self.root,text="Salary",position=[500,270])
    salaryEntry = components.createEntry(self.root,textvariable=self.salaryStringVar,position=[560,270],width=200)

    # Create employee management buttons
    components.createButton(self.root,text="Save",command=self.addEmployee,background="#2196f3",position=[500,305],height=30)
    components.createButton(self.root,text="Update",command=self.updateEmployee,background="#4caf50",position=[620,305],height=30)
    components.createButton(self.root,text="Delete",command=self.deleteEmployee,background="#f44336",position=[740,305],height=30)
    components.createButton(self.root,text="Clear",command=self.clearTextFields,background="#607d8b",position=[860,305],height=30)

def createEmployeeList(self):
    employeeTableFrame = components.createFrame(self.root,bd=3,position=[0,350],height=150,relwidth=1)

    self.employeeTable = components.createTreeview(
        employeeTableFrame,
        self.getDataFromList,
        columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),
        headers=("EMP ID","Name","Email","Gender","Contact","D.O.B","D.O.J","Password","User Type","Address","Salary"),
        columnWidths=(90,100,100,100,100,100,100,100,100,100,100)
    )

class Employee:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")

        self.root.config(background="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        # Tkinter StringVar variables
        self.idStringVar = StringVar()
        self.genderStringVar = StringVar()
        self.contactStringVar = StringVar()
        self.nameStringVar = StringVar()
        self.dobStringVar = StringVar()
        self.dojStringVar = StringVar()
        self.emailStringVar = StringVar()
        self.passwordStringVar = StringVar()
        self.usertypeStringVar = StringVar()
        self.addressStringVar = ""
        self.salaryStringVar = StringVar()

        self.searchTypeStringVar = StringVar()
        self.searchTextStringVar = StringVar()

        # Initialize Interface
        createSearchFrame(self)
        createDecorations(self)
        createEmployeeFrame(self)
        createEmployeeList(self)
        
        self.updateEmployeeList()
        self.fetchTextFromInputBoxes()

    # Functions
    def fetchTextFromInputBoxes(self):
        self.employeeID = self.idStringVar.get()
        self.employeeGender = self.genderStringVar.get()
        self.employeeContact = self.contactStringVar.get()
        self.employeeName = self.nameStringVar.get()
        self.employeeDateOfBirth = self.dobStringVar.get()
        self.employeeDOJ = self.dojStringVar.get()
        self.employeeEmail = self.emailStringVar.get()
        self.employeePassword = self.passwordStringVar.get()
        self.employeeAddress = self.addressStringVar.get('1.0',END)
        self.employeeUserType = self.usertypeStringVar.get()
        self.employeeSalary = self.salaryStringVar.get()

        self.searchType = self.searchTypeStringVar.get()
        self.searchName = self.searchTextStringVar.get()

    def addEmployee(self):
        self.fetchTextFromInputBoxes()

        if self.employeeID=="":
            messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            return

        connection = sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from employee where eid=?",(self.employeeID,))
            response = cursor.fetchone()
            if response!=None:
                messagebox.showerror("Error","This Employee ID is already assigned",parent=self.root)
                return

            cursor.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                self.employeeID,
                self.employeeName,
                self.employeeEmail,
                self.employeeGender,
                self.employeeContact,
                self.employeeDateOfBirth,
                self.employeeDOJ,
                self.employeePassword,
                self.employeeUserType,
                self.employeeAddress,
                self.employeeSalary,
            ))
            connection.commit()
            messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
            
            self.clearTextFields()
            self.updateEmployeeList()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def updateEmployeeList(self):
        self.fetchTextFromInputBoxes()

        connection = sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("select * from employee")
            response=cursor.fetchall()
            self.employeeTable.delete(*self.employeeTable.get_children())
            for employee in response:
                self.employeeTable.insert('',END,values=employee)
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def updateEmployee(self):
        self.fetchTextFromInputBoxes()

        if self.employeeID=="":
            messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            return

        connection = sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from employee where eid=?",(self.employeeID,))
            response = cursor.fetchone()
            if response == None:
                messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                return
                
            cursor.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                self.employeeName,
                self.employeeEmail,
                self.employeeGender,
                self.employeeContact,
                self.employeeDateOfBirth,
                self.employeeDOJ,
                self.employeePassword,
                self.employeeUserType,
                self.employeeAddress,
                self.employeeSalary,
                self.employeeID,
            ))
            connection.commit()
            messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
            self.updateEmployeeList()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def deleteEmployee(self):
        self.fetchTextFromInputBoxes

        if self.employeeID=="":
            messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            return

        connection = sqlite3.connect(database=config.databaseURL)
        cursor=connection.cursor()
        try:
            cursor.execute("Select * from employee where eid=?",(self.employeeID,))
            response=cursor.fetchone()
            if response==None:
                messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                return

            userConfirmation = messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
            if userConfirmation == False:
                return

            cursor.execute("delete from employee where eid=?",(self.employeeID,))
            connection.commit()
            messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
            self.clearTextFields()
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def searchEmployee(self):
        self.fetchTextFromInputBoxes()

        if self.searchType == "Select":
            messagebox.showerror("Error","Select Search By option",parent=self.root)
            return
        elif self.searchName == "":
            messagebox.showerror("Error","Search input should be required",parent=self.root)
            return

        connection = sqlite3.connect(database=config.databaseURL)
        cursor = connection.cursor()
        try:
            cursor.execute("select * from employee where "+self.searchType+" LIKE '%"+self.searchName+"%'")
            response = cursor.fetchall()

            if(len(response) == 0):
                messagebox.showerror("Error","No record found!!!",parent=self.root)
                return

            self.employeeTable.delete(*self.employeeTable.get_children())
            for employee in response:
                self.employeeTable.insert('',END,values=row)   
        except Exception as error:
            messagebox.showerror("Error",f"Error due to : {str(error)}")

    def getDataFromList(self,ev):
        focus=self.employeeTable.focus()
        content=(self.employeeTable.item(focus))
        productListing=content['values']
        
        # Quit if no items are in list and it is clicked
        if(len(productListing) == 0):
            return

        self.idStringVar.set(productListing[0])
        self.nameStringVar.set(productListing[1])
        self.emailStringVar.set(productListing[2])
        self.genderStringVar.set(productListing[3])
        self.contactStringVar.set(productListing[4])
        self.dobStringVar.set(productListing[5])
        self.dojStringVar.set(productListing[6])
        self.passwordStringVar.set(productListing[7])
        self.usertypeStringVar.set(productListing[8])
        self.addressStringVar.delete('1.0',END)
        self.addressStringVar.insert(END,productListing[9])
        self.salaryStringVar.set(productListing[10])

    def clearTextFields(self):
        self.idStringVar.set("")
        self.nameStringVar.set("")
        self.emailStringVar.set("")
        self.genderStringVar.set("Select")
        self.contactStringVar.set("")
        self.dobStringVar.set("")
        self.dojStringVar.set("")
        self.passwordStringVar.set("")
        self.usertypeStringVar.set("Admin")
        self.addressStringVar.delete('1.0',END)
        self.salaryStringVar.set("")
        self.searchTypeStringVar.set("Select")
        self.searchTextStringVar.set("")
        self.updateEmployeeList()

if __name__=="__main__":
    root=Tk()
    obj=Employee(root)
    root.mainloop()