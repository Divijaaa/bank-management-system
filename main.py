import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="da7384",
            database="bank_management"
        )
        self.cursor = self.connection.cursor()

    def fetch_customer_details(self, customer_id):
        query = f"SELECT * FROM customer WHERE cust_id = {customer_id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_account_details(self, customer_id):
        query = f"SELECT * FROM account WHERE cust_id = {customer_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_loan_details(self, customer_id):
        query = f"SELECT * FROM loan WHERE cust_id = {customer_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_transaction_details(self, customer_id):
        query = f"SELECT * FROM transactions WHERE cust_id = {customer_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_all_customer_details(self):
        query = "SELECT * FROM customer"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_bank_details(self):
        query = "SELECT * FROM bank"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_branch_details(self):
        query = "SELECT * FROM branch"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def add_customer(self, name, phone, address, email):
        query = "INSERT INTO customer (name_of_cust, phone_no, customer_address, customer_mail, username, password, bank_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        default_username = "customer"  # Default username for new customers
        default_password = "customer"  # Default password for new customers
        default_bank_name = "Bank A"  # Default bank name for new customers

        try:
            self.cursor.execute(query, (name, phone, address, email, default_username, default_password, default_bank_name))
            self.connection.commit()
            return self.cursor.lastrowid  # Return the ID of the newly added customer
        except mysql.connector.Error as err:
            print("Error:", err)
            return None
        
    def delete_customer(self, customer_id):
        try:
            # Delete customer details
            delete_customer_query = "DELETE FROM customer WHERE cust_id = %s"
            self.cursor.execute(delete_customer_query, (customer_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
 

class ThemedStyle(ttk.Style):
    def __init__(self):
        super().__init__()
        self.theme_use('clam')  # Set the initial theme
        self.configure("TButton", foreground="saddle brown", background="bisque2")
        self.configure("TLabel", foreground="green")
        self.configure("TFrame", foreground="cyan")
        self.configure("TCombobox", fieldbackground="cyan")
        self.configure("TCanvas", background="cyan")

class LoginWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Login")
        self.root.geometry("400x400")  # Set width to 400 pixels and height to 400 pixels

        self.style = ThemedStyle()

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()
        self.frame = tk.Frame(root, bg="bisque2")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Inserting the photo
        self.photo = tk.PhotoImage(file="C:/Users/divij/Downloads/pngimg.com - bank_PNG22.png")
        self.photo_label = tk.Label(self.frame, image=self.photo, bg="bisque2")
        self.photo_label.grid(row=0,column=1, columnspan=1,padx=10,pady=10)

        # Empty row for spacing
        tk.Label(self.frame,bg='bisque2').grid(row=1)

        self.username_label = tk.Label(self.frame, text="Username:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.username_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20, 5))
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=2, column=1, padx=10, pady=(20, 5))

        self.password_label = tk.Label(self.frame, text="Password:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.password_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=5)

        self.user_type_label = tk.Label(self.frame, text="User Type:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.user_type_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        self.user_type_var = tk.StringVar()
        self.user_type_var.set("Customer")

        self.customer_radio = tk.Radiobutton(self.frame, text="CUSTOMER", variable=self.user_type_var, value="Customer",font=("helvetica", 10,"bold"), bg="bisque2",fg="dodgerblue4")
        self.customer_radio.grid(row=5, column=1, sticky="w", padx=10,pady=5)

        self.employee_radio = tk.Radiobutton(self.frame, text="EMPLOYEE", variable=self.user_type_var, value="Employee",font=("helvetica", 10,"bold"),bg="bisque2",fg="dodgerblue4")
        self.employee_radio.grid(row=5, column=2, sticky="w", pady=5)

        # Empty row for spacing
        tk.Label(self.frame, bg='bisque2').grid(row=6)

        self.login_button = tk.Button(self.frame, text="LOGIN", command=self.validate_login, fg='bisque2', bg='dodgerblue4', font=("helvetica", 12, "bold"))
        self.login_button.grid(row=7, column=1, columnspan=2, pady=(3, 20))


    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        if user_type == "Customer":
            # Here you would implement your authentication logic for customers
            # For simplicity, let's assume username and password are both "customer"
            if username == "try" and password == "try":
                messagebox.showinfo("Login Successful", "Welcome, Customer!")
                self.open_customer_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        elif user_type == "Employee":
            # Here you would implement your authentication logic for employees
            # For simplicity, let's assume username and password are both "employee"
            if username == "employee" and password == "employee":
                messagebox.showinfo("Login Successful", "Welcome, Employee!")
                self.open_employee_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

    def open_customer_dashboard(self):
        self.root.destroy()
        root = tk.Tk()
        CustomerDashboard(root, self.db,1)  # Assuming customer ID is 1 for demonstration
        root.mainloop()

    def open_employee_dashboard(self):
        self.root.destroy()
        root = tk.Tk()
        EmployeeDashboard(root, self.db)
        root.mainloop()

class CustomerDashboard:
    def __init__(self, root, db, customer_id):
        self.root = root
        self.db = db
        self.customer_id = customer_id
        self.root.title("Customer Dashboard")

        self.style = ttk.Style()

        self.frame = tk.Frame(root, padx=20, pady=20, bg='bisque2')
        self.frame.pack()

        # Entry for entering customer ID
        self.customer_id_label = tk.Label(self.frame, text="Customer ID:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.customer_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.customer_id_entry = tk.Entry(self.frame, font=("helvetica", 12))
        self.customer_id_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Button to confirm customer ID
        self.confirm_button = tk.Button(self.frame, text="Confirm", command=self.confirm_customer_id, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.confirm_button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        # Button to reset customer ID
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset_customer_id, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.reset_button.grid(row=0, column=3, sticky="w", padx=10, pady=10)

        # Combobox for selecting detail type
        self.detail_type_label = tk.Label(self.frame, text="Select Detail Type:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.detail_type_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.detail_type_var = tk.StringVar()
        self.detail_type_combobox = ttk.Combobox(self.frame, textvariable=self.detail_type_var, state="readonly")
        self.detail_type_combobox.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        self.detail_type_combobox["values"] = ["Account Details", "Loan Details", "Transaction Details"]
        self.detail_type_combobox.current(0)

        # Button to display details
        self.display_button = tk.Button(self.frame, text="Display Details", command=self.display_selected_details, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.display_button.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        # Text widget for displaying details
        self.details_text = tk.Text(self.frame, height=10, width=50, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.details_text.grid(row=2, column=0, columnspan=3, sticky="w", padx=10, pady=10)

        self.back_button = tk.Button(self.frame, text="Back to Login", command=self.go_back_to_login, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.back_button.grid(row=3, column=2, sticky="w", padx=10, pady=10)

        # Button to exit the application
        self.exit_button = tk.Button(self.frame, text="Exit", command=self.exit_application, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.exit_button.grid(row=3, column=3, sticky="w", padx=10, pady=10)

    def confirm_customer_id(self):
        customer_id = self.customer_id_entry.get()
        if customer_id:
            self.customer_id = customer_id
            self.customer_id_entry.config(state="disabled")
            self.confirm_button.config(state="disabled")
        else:
            messagebox.showerror("Error", "Please enter customer ID.")

    def reset_customer_id(self):
        self.customer_id_entry.delete(0, tk.END)
        self.customer_id_entry.config(state="normal")
        self.confirm_button.config(state="normal")

    def display_selected_details(self):
        option = self.detail_type_var.get()
        if option == "Account Details":
            details = self.db.fetch_account_details(self.customer_id)
        elif option == "Loan Details":
            details = self.db.fetch_loan_details(self.customer_id)
        elif option == "Transaction Details":
            details = self.db.fetch_transaction_details(self.customer_id)
        else:
            details = None

        self.display_details(option, details)

    def display_details(self, option, details):
        self.details_text.delete(1.0, tk.END)
        
        if details:
            for detail in details:
                if option == "Account Details":
                    self.details_text.insert(tk.END, f"Account Number: {detail[0]}\n")
                    self.details_text.insert(tk.END, f"Account Type: {detail[1]}\n")
                    self.details_text.insert(tk.END, f"Balance: {detail[2]}\n")
                    self.details_text.insert(tk.END, f"Status: {detail[3]}\n")
                    self.details_text.insert(tk.END, "\n")
                elif option == "Loan Details":
                    self.details_text.insert(tk.END, f"Loan ID: {detail[0]}\n")
                    self.details_text.insert(tk.END, f"Loan Type: {detail[1]}\n")
                    self.details_text.insert(tk.END, f"Amount: {detail[2]}\n")
                    self.details_text.insert(tk.END, f"Interest Rate: {detail[3]}\n")
                    self.details_text.insert(tk.END, "\n")
                elif option == "Transaction Details":
                    self.details_text.insert(tk.END, f"Transaction ID: {detail[0]}\n")
                    self.details_text.insert(tk.END, f"Type: {detail[1]}\n")
                    self.details_text.insert(tk.END, f"Amount: {detail[2]}\n")
                    self.details_text.insert(tk.END, f"Sender ID: {detail[3]}\n")
                    self.details_text.insert(tk.END, f"Receiver ID: {detail[4]}\n")
                    self.details_text.insert(tk.END, "\n")
        else:
            self.details_text.insert(tk.END, "No details found.")

    def go_back_to_login(self):
        self.root.destroy()  # Destroy the customer dashboard window
        # Code to go back to the login window
        root = tk.Tk()  # Create a new root window for the login
        LoginWindow(root, self.db)  # Open the login window
        root.mainloop()
        
    def exit_application(self):
        self.root.destroy()  # Destroy the entire application


class EmployeeDashboard:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Employee Dashboard")

        self.frame = tk.Frame(root, padx=20, pady=20, bg='bisque2')
        self.frame.pack()
        

        # Entry fields for adding a new customer
        self.name_label = tk.Label(self.frame, text="Name:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(self.frame, text="Phone Number:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.phone_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        self.address_label = tk.Label(self.frame, text="Address:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.address_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.address_entry = tk.Entry(self.frame)
        self.address_entry.grid(row=2, column=1, padx=10, pady=5)

        self.email_label = tk.Label(self.frame, text="Email:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.email_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_customer_button = tk.Button(self.frame, text="Add Customer", command=self.add_customer, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.add_customer_button.grid(row=4, columnspan=2, padx=10, pady=5)

        # Entry for deleting a customer
        self.delete_customer_label = tk.Label(self.frame, text="Delete Customer (ID):", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.delete_customer_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.delete_customer_entry = tk.Entry(self.frame, width=20)  # Decrease the width to match the customer ID entry
        self.delete_customer_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button to delete a customer
        self.delete_customer_button = tk.Button(self.frame, text="Delete Customer", command=self.delete_customer, fg='dodgerblue4', bg='bisque2', font=("helvetica", 10, "bold"))
        self.delete_customer_button.grid(row=5, column=2, padx=10, pady=5)

        # Dropdown for selecting detail type
        self.detail_type_label = tk.Label(self.frame, text="Select Detail Type:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.detail_type_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        self.detail_type_var = tk.StringVar()
        self.detail_type_combobox = ttk.Combobox(self.frame, textvariable=self.detail_type_var)
        self.detail_type_combobox.grid(row=6, column=1, padx=10, pady=5)

        # Configure the style for the combobox and its dropdown listbox
        style = ttk.Style()
        style.configure('Custom.TCombobox', foreground='dodgerblue4', background='bisque2', font=("helvetica", 12))

        self.detail_type_combobox['style'] = 'Custom.TCombobox'

        self.detail_type_combobox["values"] = ["Customer Details", "Bank Details", "Branch Details"]
        self.detail_type_combobox.current(0)
        self.detail_type_combobox.bind("<<ComboboxSelected>>", self.on_detail_type_selected)


        # Entry for entering customer ID
        self.customer_id_label = tk.Label(self.frame, text="Customer ID:", fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.customer_id_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.customer_id_entry = tk.Entry(self.frame,state="normal",font=("helvetica", 12, "bold"))  # Initially enabled
        self.customer_id_entry.grid(row=7, column=1, padx=30, pady=5)
        self.customer_id_entry.config(width=20) 

        # Button to initiate search
        self.search_button = tk.Button(self.frame, text="Search", command=self.search_customer, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.search_button.grid(row=6, column=2, rowspan=2, padx=10, pady=5)

        # Text widget for displaying details
        self.details_text = tk.Text(self.frame, height=10, width=50, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.details_text.grid(row=8, column=0, columnspan=3, padx=10, pady=5)

        # Button to go back to login window
        self.back_button = tk.Button(self.frame, text="Back to Login", command=self.go_back_to_login, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.back_button.grid(row=9, columnspan=3, padx=10, pady=5)

        # Button to exit the application
        self.exit_button = tk.Button(self.frame, text="Exit", command=self.exit_application, fg='dodgerblue4', bg='bisque2', font=("helvetica", 12, "bold"))
        self.exit_button.grid(row=9, column=2, padx=10, pady=5)

    def add_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        email = self.email_entry.get()

        # Validate if all fields are filled
        if not (name and phone and address and email):
            messagebox.showerror("Error", "Please enter all customer details.")
            return

        # Add the new customer to the database
        customer_id = self.db.add_customer(name, phone, address, email)

        if customer_id:
            messagebox.showinfo("Success", f"Customer added successfully with ID: {customer_id}")
        else:
            messagebox.showerror("Error", "Failed to add customer")

        # Clear the entry fields after adding customer
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def delete_customer(self):
        customer_id = self.delete_customer_entry.get()
        if customer_id:
            if messagebox.askyesno("Confirmation", f"Do you want to delete customer {customer_id}?"):
                success = self.db.delete_customer(customer_id)
                if success:
                    messagebox.showinfo("Success", f"Customer {customer_id} deleted successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to delete customer {customer_id}.")
        else:
            messagebox.showerror("Error", "Please enter customer ID.")

    def on_detail_type_selected(self, event):
        selected_type = self.detail_type_var.get()
        if selected_type == "Customer Details":
            self.customer_id_entry.config(state="normal")  # Enable customer ID entry
        else:
            self.customer_id_entry.delete(0, tk.END)  # Clear any entered customer ID
            self.customer_id_entry.config(state="disabled")  # Disable customer ID entry

    def search_customer(self):
        detail_type = self.detail_type_var.get()

        if detail_type == "Customer Details":
            customer_id = self.customer_id_entry.get()
            if customer_id:
                customer_details = self.db.fetch_customer_details(customer_id)
                if customer_details:
                    self.display_customer_details(customer_details)
                else:
                    self.details_text.delete("1.0", tk.END)
                    self.details_text.insert(tk.END, "Customer not found.")
            else:
                messagebox.showerror("Error", "Please enter customer ID.")
        elif detail_type == "Bank Details":
            bank_details = self.db.fetch_bank_details()
            self.display_bank_details(bank_details)
        elif detail_type == "Branch Details":
            branch_details = self.db.fetch_branch_details()
            self.display_branch_details(branch_details)

    def display_customer_details(self, customer_details):
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert(tk.END, f"Customer ID: {customer_details[0]}\n")
        self.details_text.insert(tk.END, f"Name: {customer_details[1]}\n")
        self.details_text.insert(tk.END, f"Phone: {customer_details[2]}\n")
        self.details_text.insert(tk.END, f"Address: {customer_details[3]}\n")

    def display_bank_details(self, bank_details):
        self.details_text.delete("1.0", tk.END)
        if bank_details:
            self.details_text.insert(tk.END, "Bank Details:\n")
            for idx, detail in enumerate(bank_details):
                self.details_text.insert(tk.END, f"Bank {idx + 1}:\n")
                self.details_text.insert(tk.END, f"Name: {detail[0]}\n")
                self.details_text.insert(tk.END, f"Code: {detail[1]}\n")
                self.details_text.insert(tk.END, f"Main Address: {detail[2]}\n\n")
        else:
            self.details_text.insert(tk.END, "No bank details found.")

    def display_branch_details(self, branch_details):
        self.details_text.delete("1.0", tk.END)
        if branch_details:
            self.details_text.insert(tk.END, "Branch Details:\n")
            for idx, detail in enumerate(branch_details):
                self.details_text.insert(tk.END, f"Branch {idx + 1}:\n")
                self.details_text.insert(tk.END, f"Name: {detail[2]}\n")
                self.details_text.insert(tk.END, f"Phone: {detail[1]}\n")
                self.details_text.insert(tk.END, f"Address: {detail[3]}\n\n")
        else:
            self.details_text.insert(tk.END, "No branch details found.")

    def go_back_to_login(self):
        self.root.destroy()  # Destroy the dashboard window
        root = tk.Tk()  # Create a new root window for the login
        LoginWindow(root, self.db)  # Open the login window
        root.mainloop()
    
    def exit_application(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    db = Database()
    LoginWindow(root, db)
    root.mainloop()
    db.close_connection()

if __name__ == "__main__":
    main()
