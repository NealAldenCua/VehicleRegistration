from errno import errorcode

import customtkinter
import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


# Connect to MySQL server
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hackermanN0thing"
    )


# Create database if not exists
def create_database():
    db = connect_to_mysql()
    cursor = db.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS vehicleregistration")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print("Database already exists")
        else:
            print(err)
            raise
    finally:
        cursor.close()
        db.close()


# Create table if not exists
def create_table():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hackermanN0thing",
        database="vehicleregistration"
    )
    cursor = db.cursor()
    try:
        # Create a table with id, name, address, vehicle, and plate columns
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS registration (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                vehicle VARCHAR(255),
                plate VARCHAR(255) UNIQUE
            )
            """
        )
    except mysql.connector.Error as err:
        print(err)
        raise
    finally:
        cursor.close()
        db.close()


# Initialize the database and table
create_database()  # Ensure the database exists
create_table()  # Ensure the table exists

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title('Vehicle Registration')
app.geometry("1000x600")

global name
global address
global vehicle
global plate

# label for Vehicle Registration
customtkinter.CTkLabel(app, text="Vehicle Monitoring", font=(None, 40)).place(x=30, y=30)

# label for inputs
name_label = customtkinter.CTkLabel(app, text="Name", font=(None, 20)).place(x=50, y=100)
name_entry = customtkinter.CTkEntry(app, placeholder_text="Enter your name", width=350)
name_entry.place(x=250, y=100)

address_label = customtkinter.CTkLabel(app, text="Address", font=(None, 20)).place(x=50, y=150)
address_entry = customtkinter.CTkEntry(app, placeholder_text="Enter your address", width=350)
address_entry.place(x=250, y=150)

vehicle_label = customtkinter.CTkLabel(app, text="Vehicle", font=(None, 20)).place(x=50, y=200)
vehicle_entry = customtkinter.CTkEntry(app, placeholder_text="Enter your vehicle", width=350)
vehicle_entry.place(x=250, y=200)

plate_number_label = customtkinter.CTkLabel(app, text="Plate Number", font=(None, 20)).place(x=50, y=250)
plate_number_entry = customtkinter.CTkEntry(app, placeholder_text="Enter your plate number", width=350)
plate_number_entry.place(x=250, y=250)


# functions for the buttons
def Add():
    # Check if any of the entries is empty
    if not (name_entry.get() and address_entry.get() and vehicle_entry.get() and plate_number_entry.get()):
        # If any of the entries is empty, show a warning and return without further processing
        messagebox.showwarning("Warning", "All fields must be filled!")
        return

    name_value = name_entry.get()
    address_value = address_entry.get()
    vehicle_value = vehicle_entry.get()
    plate_value = plate_number_entry.get()

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="hackermanN0thing",
                                      database="vehicleregistration")
    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO registration (name, address, vehicle, plate) VALUES (%s, %s, %s, %s)"
        val = (name_value, address_value, vehicle_value, plate_value)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Entry added successfully")

        # Clear the fields
        name_entry.delete(0, END)
        address_entry.delete(0, END)
        vehicle_entry.delete(0, END)
        plate_number_entry.delete(0, END)
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()


def Delete():
    # Check if any item is selected in the Treeview
    if not listbox.selection():
        # If no item is selected, show a warning and return without further processing
        messagebox.showwarning("Warning", "Select a record to delete!")
        return

    # Get the selected item from the Treeview
    selected_item = listbox.selection()[0]
    values = listbox.item(selected_item, 'values')

    # This assumes you have a unique identifier in the Treeview.
    # For simplicity, if your table has a primary key like 'id', use it to find the record to delete.
    plate_value = values[3]  # Assuming the plate number is the unique identifier

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="hackermanN0thing",
                                      database="vehicleregistration")
    mycursor = mysqldb.cursor()
    try:
        sql = "DELETE FROM registration WHERE plate = %s"  # Using plate number as a unique identifier
        val = (plate_value,)
        mycursor.execute(sql, val)
        mysqldb.commit()

        messagebox.showinfo("Information", "Record deleted successfully.")

        # Remove the selected item from the Treeview
        listbox.delete(selected_item)

        # Clear the entry fields
        name_entry.delete(0, END)
        address_entry.delete(0, END)
        vehicle_entry.delete(0, END)
        plate_number_entry.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        mysqldb.rollback()
    finally:
        mysqldb.close()


def Update():
    # Check if any item is selected in the Treeview
    if not listbox.selection():
        messagebox.showwarning("Warning", "Select a record to update!")
        return

    # Get the selected item from the Treeview
    selected_item = listbox.selection()[0]
    values = listbox.item(selected_item, 'values')

    # Assuming you have a unique identifier like 'plate'
    plate_value_to_update = values[3]  # Assuming plate is unique

    name_value = name_entry.get()
    address_value = address_entry.get()
    vehicle_value = vehicle_entry.get()
    plate_value = plate_number_entry.get()

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="hackermanN0thing",
                                      database="vehicleregistration")
    mycursor = mysqldb.cursor()
    try:
        sql = "UPDATE registration SET name = %s, address = %s, vehicle = %s, plate = %s WHERE plate = %s"
        val = (name_value, address_value, vehicle_value, plate_value, plate_value_to_update)  # Five parameters now
        mycursor.execute(sql, val)
        mysqldb.commit()

        messagebox.showinfo("Information", "Record updated successfully.")

        # Update the selected item in the Treeview
        listbox.item(selected_item, values=(name_value, address_value, vehicle_value, plate_value))

        # Clear the entry fields
        name_entry.delete(0, END)
        address_entry.delete(0, END)
        vehicle_entry.delete(0, END)
        plate_number_entry.delete(0, END)

    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"An error occurred: {e}")
        mysqldb.rollback()

    finally:
        mysqldb.close()


def GetValue(event):
    if not listbox.selection():
        return  # No selection, so nothing to do

    name_entry.delete(0, END)
    address_entry.delete(0, END)
    vehicle_entry.delete(0, END)
    plate_number_entry.delete(0, END)

    row_id = listbox.selection()[0]
    select = listbox.item(row_id, 'values')  # Extract the values

    # Use safe retrieval with index-based extraction
    try:
        name_value = select[0]  # Assuming the first column is 'name'
        address_value = select[1]  # Assuming the second column is 'address'
        vehicle_value = select[2]  # Assuming the third column is 'vehicle'
        plate_value = select[3]  # Assuming the fourth column is 'plate number'

        # Insert into entry fields
        name_entry.insert(0, name_value)
        address_entry.insert(0, address_value)
        vehicle_entry.insert(0, vehicle_value)
        plate_number_entry.insert(0, plate_value)

    except IndexError:
        # Handle case where expected index does not exist
        messagebox.showwarning("Warning", "Error retrieving record details.")


def show():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="hackermanN0thing",
                                      database="vehicleregistration")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT name, address, vehicle, plate FROM registration")
    records = mycursor.fetchall()
    print(records)
    for i, (name, address, vehicle, plate) in enumerate(records, start=1):
        listbox.insert("", "end", values=(name, address, vehicle, plate))
        mysqldb.close()


# buttons
button_add = customtkinter.CTkButton(app, command=Add, text="ADD", font=(None, 20), width=100, height=100,
                                     fg_color="#77DD77", text_color="black", hover_color="gray", border_width=1,
                                     border_color="white").place(x=630, y=150)

button_delete = customtkinter.CTkButton(app, command=Delete, text="Delete", font=(None, 20), width=100, height=100,
                                        fg_color="#FAA0A0", text_color="black", hover_color="gray", border_width=1,
                                        border_color="white").place(x=750, y=150)

button_update = customtkinter.CTkButton(app, command=Update, text="update", font=(None, 20), width=100, height=100,
                                        fg_color="#FDFD96", text_color="black", hover_color="gray", border_width=1,
                                        border_color="white").place(x=870, y=150)

# display items
cols = ('name', 'address', 'vehicle', 'plate number')
listbox = ttk.Treeview(app, columns=cols, show='headings', height=18, style="mystyle.Treeview")

# make text bigger
style = ttk.Style()
style.configure("mystyle.Treeview.Heading", font=("None", 15))  # Increase font for Treeview headings
style.configure("mystyle.Treeview", font=("None", 15))

for col in cols:
    listbox.heading(col, text=col)
    listbox.grid(row=1, column=0, columnspan=2)
    listbox.place(x=50, y=500, width=1400)

show()
listbox.bind('<Double-Button-1>', GetValue)

app.mainloop()
