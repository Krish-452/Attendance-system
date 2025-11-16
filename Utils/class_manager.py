import csv
from tkinter import messagebox

def retrieve_classes(user:str, acc_type: str) -> list:
    classes = []
    with open("../Data/classes.csv", "r") as class_data:
        reader = csv.DictReader(class_data)
        for row in reader:
            if row[acc_type] == user:
                classes.append(row)
    return classes
