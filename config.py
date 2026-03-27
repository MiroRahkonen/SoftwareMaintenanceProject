import os

#------Reusable Variables-------
databaseURL = "ims.db"

#------- BASE PATH SETUP -------
baseDirectory = os.path.dirname(os.path.abspath(__file__))
imageDirectory = os.path.join(baseDirectory, "images")
billsDirectory = os.path.join(baseDirectory, "bills")

os.makedirs(billsDirectory, exist_ok=True)