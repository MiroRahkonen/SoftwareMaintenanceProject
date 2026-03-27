from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import config
import components

defaultFont = ("goudy old style",15)

# Function parameters have default values, which are overwritten if they are set in function call
def createFrame(
    self,
    bd=None,
    position=[None,None],
    background="white",
    width=None,
    height=None,
    relwidth=None
):
    frame = Frame(
        self,
        bd=bd,
        background=background,
        relief=RIDGE
    )
    frame.place(
        x=position[0],
        y=position[1], 
        width=width,
        height=height,
        relwidth=relwidth
    )
    return frame


def createImage(path,size=[None,None]):
    image = Image.open(path)
    # If image size is given, resize the image
    if(size[0] != None):
        image = image.resize(size)
    
    image = ImageTk.PhotoImage(image)
    return image


def createLabel(self, text, fg="black", font=defaultFont, background="white", position=[None,None]):
    label = Label(self, text=text, fg=fg, font=font, background=background)
    label.place(x=position[0], y=position[1])
    return label


def createText(self, height, width, position=[]):
    text = Text(self, font=defaultFont, background="lightyellow")
    text.place(
        x=position[0], 
        y=position[1], 
        width=width, 
        height=height
    )
    return text


def createEntry(
    self,
    textvariable=None, 
    font=defaultFont, 
    background="lightyellow", 
    fg=None,
    position=[None,None],
    width=200,
    height=None
):
    entry=Entry(
        self,
        textvariable=textvariable,
        font=font,
        background=background,
        fg=fg
    )
    entry.place(
        x=position[0], 
        y=position[1], 
        width = width,
        height = height
    )
    return entry


def createImageLabel(self,image,position=[None,None]):
    imageLabel = Label(self, bd=2, relief = RAISED, image=image)
    imageLabel.place(x = position[0], y = position[1])
    return imageLabel


def createDashboardLabel(self, text, background, position=[]):
    label = Label(
        self,
        text = text,
        fg = "white",
        bd=5,
        relief=RIDGE,
        background = background,
        font = ("times new roman",20,"bold"),
    )
    label.place(
        x = position[0],
        y = position[1],
        width = 300,
        height = 150
    )
    return label


def createNavigationButton(self,text,command,image):
    button = Button(
        self,
        text=text,
        command=command,
        image=image,
        compound=LEFT,
        padx=5,
        anchor="w",
        font = ("times new roman",20,"bold"),
        background="white",
        bd=3,
        cursor="hand2"
    )
    button.pack(side=TOP, fill=X)
    return button


def createButton(
    self,
    text,
    command,
    background,
    font=("times new roman",15),
    fg="white",
    position=[],
    height=35,
    width=100
):
    button=Button(
        self,
        text=text,
        command=command,
        font=font,
        background=background,
        fg=fg,
        cursor="hand2"
    )
    button.place(
        x=position[0],
        y=position[1],
        height=height,
        width=width
    )
    return button


def createCalculatorButton(self, text, command,row, column, pady=10):
    button = Button(
        self,
        text=text,
        font=('arial',15,'bold'),
        command=command,
        bd=5,
        width=4,
        pady=pady,
        cursor="hand2"
    )
    button.grid(
        row=row,
        column=column
    )
    return button


def createCombobox(self,textvariable,values,position,width=200):
    combobox = ttk.Combobox(
        self,
        textvariable=textvariable,
        values=values,
        state='readonly',
        justify=CENTER,
        font=defaultFont,
    )
    combobox.place(
        x=position[0],
        y=position[1],
        width=width
    )
    combobox.current(0)
    return combobox


def createTreeview(parentFrame, command=None, columns=[], headers=[],columnWidths=[]):
    scrolly=Scrollbar(parentFrame,orient=VERTICAL)
    scrollx=Scrollbar(parentFrame,orient=HORIZONTAL)

    table=ttk.Treeview(
        parentFrame,
        columns=columns,
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set
    )

    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.config(command=table.xview)
    scrolly.config(command=table.yview)

    tablelength = len(columns)

    # Create columns into table
    for index in range(tablelength):
        table.heading(columns[index],text=headers[index])
        table.column(columns[index],width=columnWidths[index])


    table["show"]="headings"
    table.pack(fill=BOTH,expand=1)
    table.bind("<ButtonRelease-1>",command)
    return table


def createListbox(self, listCommand):
    scrollbar = Scrollbar(self,orient=VERTICAL)
    
    listbox = Listbox(
        scrollbar,
        font=defaultFont,
        background="white",
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(side=RIGHT,fill=Y)
    scrollbar.config(command=listbox.yview)
    listbox.pack(fill=BOTH,expand=1)
    listbox.bind("<ButtonRelease-1>", listCommand)
    return listbox