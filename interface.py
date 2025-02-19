import tkinter as tk
import tkinter.messagebox as messagebox
from datetime import datetime
from tkinter import ttk

import pyperclip

from database import insert_record, update_record, get_all_records, search_record, delete_record

# Tkinter GUI
root = tk.Tk()
root.title("Job Application Tracker")
root.geometry("1200x700")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Entry fields
label_company = tk.Label(frame_inputs, text="Company")
label_company.grid(row=0, column=0, padx=5, pady=5)
entry_company = tk.Entry(frame_inputs)
entry_company.grid(row=1, column=0, padx=5, pady=5)

label_job_title = tk.Label(frame_inputs, text="Job Title")
label_job_title.grid(row=0, column=1, padx=5, pady=5)
entry_job_title = tk.Entry(frame_inputs)
entry_job_title.grid(row=1, column=1, padx=5, pady=5)

label_application_date = tk.Label(frame_inputs, text="Application Date")
label_application_date.grid(row=0, column=2, padx=5, pady=5)
entry_application_date = tk.Entry(frame_inputs)
entry_application_date.grid(row=1, column=2, padx=5, pady=5)
entry_application_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

label_had_interview = tk.Label(frame_inputs, text="Had Interview")
label_had_interview.grid(row=2, column=0, padx=5, pady=5)
had_interview_options = ['True', 'False']
combo_had_interview = ttk.Combobox(frame_inputs, values=had_interview_options)
combo_had_interview.grid(row=3, column=0, padx=5, pady=5)

label_is_there_feedback = tk.Label(frame_inputs, text="Is There Feedback?")
label_is_there_feedback.grid(row=2, column=1, padx=5, pady=5)
is_there_feedback_options = ['True', 'False']
combo_is_there_feedback = ttk.Combobox(
    frame_inputs, values=is_there_feedback_options)
combo_is_there_feedback.grid(row=3, column=1, padx=5, pady=5)

label_feedback_date = tk.Label(frame_inputs, text="Feedback Date")
label_feedback_date.grid(row=2, column=2, padx=5, pady=5)
entry_feedback_date = tk.Entry(frame_inputs)
entry_feedback_date.grid(row=3, column=2, padx=5, pady=5)

label_application_website = tk.Label(frame_inputs, text="Application Website")
label_application_website.grid(row=4, column=0, padx=5, pady=5)
application_website_options = [
    'Gupy', 'Company website', 'LinkedIn', 'Vagas.com.br', 'Glassdoor']
combo_application_website = ttk.Combobox(
    frame_inputs, values=application_website_options)
combo_application_website.grid(row=5, column=0, padx=5, pady=5)

label_is_remote = tk.Label(frame_inputs, text="Is it Remote?")
label_is_remote.grid(row=4, column=1, padx=5, pady=5)
is_remote_options = ['hybrid', 'in-place', 'remote']
combo_is_remote = ttk.Combobox(frame_inputs, values=is_remote_options)
combo_is_remote.grid(row=5, column=1, padx=5, pady=5)

label_linkedin_access = tk.Label(frame_inputs, text="LinkedIn Access")
label_linkedin_access.grid(row=4, column=2, padx=5, pady=5)
linkedin_access_options = ['True', 'False']
combo_linkedin_access = ttk.Combobox(
    frame_inputs, values=linkedin_access_options)
combo_linkedin_access.grid(row=5, column=2, padx=5, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

def handle_insert() -> None:
    """
    Function to insert records into the database.

    This function is responsible for handling the insertion of data
    into the database by calling the insert_record function.

    Returns:
        None: This function does not return any value.
    """
    company = entry_company.get()
    job_title = entry_job_title.get()
    application_date = entry_application_date.get()
    had_interview = combo_had_interview.get()
    is_there_feedback = combo_is_there_feedback.get()
    feedback_date = entry_feedback_date.get()
    application_website = combo_application_website.get()
    is_remote = combo_is_remote.get()
    linkedin_access = combo_linkedin_access.get()

    try:
        application_date = datetime.strptime(
            application_date, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error", "Invalid Application Date! Use YYYY-MM-DD format.")
        return

    if feedback_date.strip():
        try:
            feedback_date = datetime.strptime(feedback_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid Feedback Date! Use YYYY-MM-DD format.")
            return
    else:
        feedback_date = None

    insert_record(company, job_title, application_date, had_interview, is_there_feedback,
                  feedback_date, application_website, is_remote, linkedin_access)
    messagebox.showinfo("Success", "Record inserted successfully!")

def handle_search() -> None:
    """
    Function to search for records in the database.

    This function is responsible for handling the search operation
    by calling the search_record function and displaying or processing
    the results accordingly.

    Returns:
        None: This function does not return any value.
    """
    company = entry_company.get()

    if not company:
        result = get_all_records()
    else:
        result = search_record(company)
    for row in tree.get_children():
        tree.delete(row)

    if result:
        for row in result:
            tree.insert("", "end", values=row)
    else:
        print("Data not found!")

def handle_update() -> None:
    """
    Function to update records in the database.

    This function is responsible for handling the update operation
    by calling the update_record function and processing the results accordingly.

    Returns:
        None: This function does not return any value.
    """
    company = entry_company.get()
    job_title = entry_job_title.get()
    had_interview = combo_had_interview.get()
    is_there_feedback = combo_is_there_feedback.get()
    application_website = combo_application_website.get()
    is_remote = combo_is_remote.get()
    linkedin_access = combo_linkedin_access.get()
    feedback_date = entry_feedback_date.get()

    update_record(company, job_title, had_interview, is_there_feedback,
                  feedback_date, application_website, is_remote, linkedin_access)

    messagebox.showinfo("Success", "Record updated successfully!")

def handle_delete() -> None:
    """
    Function to handle the deletion of records from the database.

    This function checks if a record is selected in the treeview, 
    calls the delete_record function to delete it from the database, 
    and removes the record from the treeview.

    Returns:
        None: This function does not return any value.
    """
    selected_item = tree.selection()

    if selected_item:
        values = tree.item(selected_item, 'values')
        job_title = values[1]
        delete_record(job_title)
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Record deleted successfully")
    else:
        print("Nothing selected to delete")

def copy_company() -> None:
    """
    Function to copy company from the treeview to the entry fields.

    This function copies the selected company name from the treeview
    and populates the corresponding entry fields in the user interface.

    Returns:
        None: This function does not return any value.
    """
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        company = values[0]
        pyperclip.copy(company)
        entry_company.delete(0, tk.END)
        entry_company.insert(0, company)

def copy_job_title() -> None:
    """
    Function to copy job title from the treeview to the entry fields.

    This function copies the selected job title from the treeview
    and populates the corresponding entry fields in the user interface.

    Returns:
        None: This function does not return any value.
    """
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        job_title = values[1]
        pyperclip.copy(job_title)
        entry_job_title.delete(0, tk.END)
        entry_job_title.insert(0, job_title)


def copy_application_date() -> None:
    """
    Function to copy application date from the treeview to the entry fields.

    This function retrieves the application date from the selected item in the
    treeview, copies it to the clipboard using pyperclip, and populates the
    corresponding entry field in the user interface.

    Returns:
        None: This function does not return any value.
    """
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        application_date = values[2]
        pyperclip.copy(application_date)
        entry_application_date.delete(0, tk.END)
        entry_application_date.insert(0, application_date)

def clear_fields() -> None:
    """
    Function to clear all entry fields.

    This function clears all the fields in the user interface, including
    text entry fields and combo boxes.

    Returns:
        None: This function does not return any value.
    """
    entry_company.delete(0, tk.END)
    entry_job_title.delete(0, tk.END)
    entry_application_date.delete(0, tk.END)
    combo_had_interview.set("")
    combo_is_there_feedback.set("")
    entry_feedback_date.delete(0, tk.END)
    combo_application_website.set("")
    combo_is_remote.set("")
    combo_linkedin_access.set("")


def load_data() -> None:
    """
    Function to load data from the database into the treeview.

    This function retrieves all records from the database using the get_all_records
    function, clears the existing items in the treeview, and inserts the new records.

    Returns:
        None: This function does not return any value.
    """
    for row in tree.get_children():
        tree.delete(row)

    rows = get_all_records()

    for row in rows:
        tree.insert("", "end", values=row)

# Buttons section
button_insert = tk.Button(root, text="Insert", command=handle_insert, bg="green", fg="white")
button_insert.pack()

button_search = tk.Button(root, text="Search", command=handle_search)
button_search.pack()

button_update = tk.Button(root, text="Update", command=handle_update, bg="blue", fg="white")
button_update.pack()

button_delete = tk.Button(root, text="Delete", command=handle_delete, bg="red", fg="white")
button_delete.pack()

button_copy_company = tk.Button(
    root, text="Copy Company", command=copy_company)
button_copy_company.pack()

button_copy_job_title = tk.Button(
    root, text="Copy Job Title", command=copy_job_title)
button_copy_job_title.pack()

button_copy_application_date = tk.Button(
    root, text="Copy Application Date", command=copy_application_date)
button_copy_application_date.pack()

button_clear_fields = tk.Button(
    root, text="Clear Fields", command=clear_fields, bg="gray", fg="white")
button_clear_fields.pack(pady=10)

# Treeview section
tree = ttk.Treeview(root, columns=("Company", "Job Title", "Application Date", "Feedback",
                    "Feedback Date", "Website", "Remote", "LinkedIn", "Interview"), show="headings")

# Creating the headers  
tree.heading("Company", text="Company")
tree.heading("Job Title", text="Job Title")
tree.heading("Application Date", text="Application Date")
tree.heading("Feedback", text="Feedback")
tree.heading("Feedback Date", text="Feedback Date")
tree.heading("Website", text="Website")
tree.heading("Remote", text="Remote")
tree.heading("LinkedIn", text="LinkedIn")
tree.heading("Interview", text="Interview")

# Adjusting the columns
tree.column("Company", width=150)
tree.column("Job Title", width=200)
tree.column("Application Date", width=100)
tree.column("Feedback", width=100)
tree.column("Feedback Date", width=100)
tree.column("Website", width=150)
tree.column("Remote", width=100)
tree.column("LinkedIn", width=100)
tree.column("Interview", width=100)

tree.pack()

# Load data into the treeview
load_data()
root.mainloop()
