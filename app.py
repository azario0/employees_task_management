import customtkinter as ctk
import csv
from datetime import datetime
from tkcalendar import Calendar

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class EmployeeTaskManagementSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Employee Task Management System")
        self.root.geometry("800x600")

        # Create tabs
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_employee = self.tabview.add("Employee Management")
        self.tab_task_assign = self.tabview.add("Task Assignment")
        self.tab_task_status = self.tabview.add("Task Status")
        self.tab_task_filter = self.tabview.add("Task Filtering & Report")

        self.setup_employee_tab()
        self.setup_task_assign_tab()
        self.setup_task_status_tab()
        self.setup_task_filter_tab()

    def setup_employee_tab(self):
        frame = ctk.CTkFrame(self.tab_employee)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Employee Name:").grid(row=0, column=0, padx=5, pady=5)
        self.employee_name = ctk.CTkEntry(frame)
        self.employee_name.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Employee Surname:").grid(row=1, column=0, padx=5, pady=5)
        self.employee_surname = ctk.CTkEntry(frame)
        self.employee_surname.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Add Employee", command=self.add_employee).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.employee_list = ctk.CTkScrollableFrame(frame, height=200)
        self.employee_list.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        ctk.CTkButton(frame, text="Delete Selected", command=self.delete_employee).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.load_employees()

    def setup_task_assign_tab(self):
        frame = ctk.CTkFrame(self.tab_task_assign)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Employee:").grid(row=0, column=0, padx=5, pady=5)
        self.task_employee = ctk.CTkComboBox(frame, values=self.get_employee_list())
        self.task_employee.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Task:").grid(row=1, column=0, padx=5, pady=5)
        self.task_description = ctk.CTkTextbox(frame, width=300, height=100)
        self.task_description.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Assign Task", command=self.assign_task).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.task_list = ctk.CTkTextbox(frame, height=200, state="disabled")
        self.task_list.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.load_tasks()

    def setup_task_status_tab(self):
        frame = ctk.CTkFrame(self.tab_task_status)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Employee:").grid(row=0, column=0, padx=5, pady=5)
        self.status_employee = ctk.CTkComboBox(frame, values=self.get_employee_list(), command=self.load_employee_tasks)
        self.status_employee.grid(row=0, column=1, padx=5, pady=5)

        self.task_status_list = ctk.CTkScrollableFrame(frame, height=300)
        self.task_status_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        ctk.CTkButton(frame, text="Mark Selected as Completed", command=self.mark_tasks_completed).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def setup_task_filter_tab(self):
        frame = ctk.CTkFrame(self.tab_task_filter)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Status:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_status = ctk.CTkComboBox(frame, values=["All", "Pending", "Completed"])
        self.filter_status.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_date = ctk.CTkEntry(frame)
        self.filter_date.grid(row=1, column=1, padx=5, pady=5)

        self.calendar = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ctk.CTkButton(frame, text="Apply Filter", command=self.apply_filter).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.filtered_tasks = ctk.CTkTextbox(frame, height=300, state="disabled")
        self.filtered_tasks.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    def add_employee(self):
        name = self.employee_name.get()
        surname = self.employee_surname.get()
        if name and surname:
            with open('employees.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, surname])
            self.load_employees()
            self.employee_name.delete(0, 'end')
            self.employee_surname.delete(0, 'end')
            self.update_employee_comboboxes()

    def load_employees(self):
        for widget in self.employee_list.winfo_children():
            widget.destroy()
        try:
            with open('employees.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    var = ctk.StringVar()
                    cb = ctk.CTkCheckBox(self.employee_list, text=f"{row[0]} {row[1]}", variable=var)
                    cb.pack(anchor="w")
        except FileNotFoundError:
            pass

    def delete_employee(self):
        employees = []
        to_delete = []
        for widget in self.employee_list.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox) and widget.get() == 1:
                to_delete.append(widget.cget("text"))
        
        with open('employees.csv', 'r') as file:
            reader = csv.reader(file)
            employees = list(reader)
        
        with open('employees.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for employee in employees:
                if f"{employee[0]} {employee[1]}" not in to_delete:
                    writer.writerow(employee)
        
        self.load_employees()
        self.update_employee_comboboxes()

    def get_employee_list(self):
        employees = []
        try:
            with open('employees.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    employees.append(f"{row[0]} {row[1]}")
        except FileNotFoundError:
            pass
        return employees

    def update_employee_comboboxes(self):
        employee_list = self.get_employee_list()
        self.task_employee.configure(values=employee_list)
        self.status_employee.configure(values=employee_list)

    def assign_task(self):
        employee = self.task_employee.get()
        task = self.task_description.get("1.0", "end-1c")
        if employee and task:
            with open('tasks.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([employee, task, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Pending"])
            self.load_tasks()
            self.task_description.delete("1.0", "end")

    def load_tasks(self):
        self.task_list.configure(state="normal")
        self.task_list.delete('1.0', 'end')
        try:
            with open('tasks.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.task_list.insert('end', f"{row[0]}: {row[1]} - {row[2]} ({row[3]})\n")
        except FileNotFoundError:
            pass
        self.task_list.configure(state="disabled")

    def load_employee_tasks(self, event=None):
        employee = self.status_employee.get()
        for widget in self.task_status_list.winfo_children():
            widget.destroy()
        try:
            with open('tasks.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == employee and row[3] == "Pending":
                        var = ctk.StringVar()
                        cb = ctk.CTkCheckBox(self.task_status_list, text=f"{row[1]} - {row[2]}", variable=var)
                        cb.pack(anchor="w")
        except FileNotFoundError:
            pass

    def mark_tasks_completed(self):
        employee = self.status_employee.get()
        tasks_to_complete = []
        for widget in self.task_status_list.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox) and widget.get() == 1:
                tasks_to_complete.append(widget.cget("text").split(' - ')[0])
        
        tasks = []
        with open('tasks.csv', 'r') as file:
            reader = csv.reader(file)
            tasks = list(reader)
        
        with open('tasks.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for task in tasks:
                if task[0] == employee and task[1] in tasks_to_complete:
                    task[3] = "Completed"
                writer.writerow(task)
        
        self.load_employee_tasks()

    def apply_filter(self):
        status = self.filter_status.get()
        date = self.calendar.get_date()
        self.filtered_tasks.configure(state="normal")
        self.filtered_tasks.delete('1.0', 'end')
        try:
            with open('tasks.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    task_date = row[2].split()[0]
                    if (status == "All" or status == row[3]) and (not date or date == task_date):
                        self.filtered_tasks.insert('end', f"{row[0]}: {row[1]} - {row[2]} ({row[3]})\n")
        except FileNotFoundError:
            pass
        self.filtered_tasks.configure(state="disabled")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EmployeeTaskManagementSystem()
    app.run()