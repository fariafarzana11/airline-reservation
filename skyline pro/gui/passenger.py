import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


from database.database import Database


class PassengerWindow:

    # ==========================================
    # INITIALIZE
    # ==========================================

    def __init__(self, root):

        self.root = root
        self.db = Database()

        # Selected passenger
        self.selected_passenger_id = None

        # Build interface
        self.build_ui()

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        self.main = ttk.Frame(self.root)

        self.main.pack(fill=BOTH, expand=True)

        # IMPORTANT:
        # Table must be created before toolbar
        # because toolbar buttons use self.table

        # self.create_sidebar()

        self.create_header()
        self.create_toolbar()

        self.create_table()

        self.create_statistics()

        self.create_status_bar()

        self.load_passengers()

        # ==========================================
        # SIDEBAR
        # ==========================================

    def create_sidebar(self):

        self.sidebar = ttk.Frame(self.main, width=240, bootstyle="dark")

        self.sidebar.pack(side=LEFT, fill=Y)

        # Logo / Title
        ttk.Label(
            self.sidebar, text="✈", font=("Segoe UI", 40), bootstyle="inverse-dark"
        ).pack(pady=(30, 5))

        ttk.Label(
            self.sidebar,
            text="SkyLink Pro",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-dark",
        ).pack()

        ttk.Label(
            self.sidebar,
            text="Airline Management",
            font=("Segoe UI", 9),
            bootstyle="inverse-dark",
        ).pack(pady=(0, 30))

        # Menu
        self.create_menu("🏠  Dashboard", self.show_dashboard)

        self.create_menu("👤  Passenger", self.open_passenger)

        self.create_menu("✈  Flight", self.open_flight)

        self.create_menu("🎫  Booking", self.open_booking)

        self.create_menu("💳  Payment", self.open_payment)

        self.create_menu("📊  Reports", self.open_reports)

        self.create_menu("⚙  Settings", self.open_settings)

        # Logout
        ttk.Button(
            self.sidebar, text="🚪  Logout", bootstyle="danger", command=self.logout
        ).pack(side=BOTTOM, fill=X, padx=15, pady=20)

        # ==========================================
        # CREATE SIDEBAR MENU
        # ==========================================

    def create_menu(self, text, command):

        ttk.Button(
            self.sidebar,
            text=text,
            bootstyle="dark",
            command=command,
            width=22,
        ).pack(
            fill=X,
            padx=15,
            pady=4,
            ipady=8,
        )

    # ==========================================
    # SIDEBAR NAVIGATION
    # ==========================================

    def show_dashboard(self):

        self.main.destroy()

        try:
            self.status_bar.destroy()
        except:
            pass

        from gui.dashboard import DashboardWindow

        DashboardWindow(self.root)

    def open_passenger(self):

        # Already on Passenger page
        pass

    def open_flight(self):

        messagebox.showinfo(
            "Flight Management", "Flight Management module is coming soon."
        )

    def open_booking(self):

        messagebox.showinfo("Booking", "Booking module is coming soon.")

    def open_payment(self):

        messagebox.showinfo("Payment", "Payment module is coming soon.")

    def open_reports(self):

        messagebox.showinfo("Reports", "Reports module is coming soon.")

    def open_settings(self):

        messagebox.showinfo("Settings", "Settings module is coming soon.")

    def logout(self):

        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")

        if confirm:

            self.main.destroy()

            try:
                self.status_bar.destroy()
            except:
                pass

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        header = ttk.Frame(self.main, padding=(25, 20))

        header.pack(fill=X)

        # Title
        ttk.Label(
            header, text="Passenger Management", font=("Segoe UI", 24, "bold")
        ).pack(side=LEFT)

        # Subtitle
        ttk.Label(
            header, text="Manage passenger information", font=("Segoe UI", 10)
        ).pack(side=LEFT, padx=20)

    # ==========================================
    # TOOLBAR
    # ==========================================

    def create_toolbar(self):

        toolbar = ttk.Frame(self.main, padding=(25, 10))

        toolbar.pack(fill=X)

        # ======================================
        # ADD PASSENGER
        # ======================================

        ttk.Button(
            toolbar,
            text="+ Add Passenger",
            bootstyle="success",
            command=self.add_passenger,
        ).pack(side=LEFT, padx=(0, 8))

        # ======================================
        # EDIT
        # ======================================

        ttk.Button(
            toolbar, text="✎ Edit", bootstyle="warning", command=self.edit_passenger
        ).pack(side=LEFT, padx=5)

        # ======================================
        # DELETE
        # ======================================

        ttk.Button(
            toolbar, text="✕ Delete", bootstyle="danger", command=self.delete_passenger
        ).pack(side=LEFT, padx=5)

        # ======================================
        # REFRESH
        # ======================================

        ttk.Button(
            toolbar, text="⟳ Refresh", bootstyle="info", command=self.refresh_passengers
        ).pack(side=LEFT, padx=5)

        # ======================================
        # SEARCH ENTRY
        # ======================================

        self.search_entry = ttk.Entry(toolbar, width=30)

        self.search_entry.pack(side=RIGHT, padx=5)

        # Press Enter to search
        self.search_entry.bind("<Return>", lambda event: self.search_passenger())

        # ======================================
        # SEARCH BUTTON
        # ======================================

        ttk.Button(
            toolbar,
            text="🔍 Search",
            bootstyle="primary",
            command=self.search_passenger,
        ).pack(side=RIGHT)

        # ======================================
        # CLEAR BUTTON
        # ======================================

        ttk.Button(
            toolbar, text="Clear", bootstyle="secondary", command=self.clear_search
        ).pack(side=RIGHT, padx=5)

    # ==========================================
    # CLEAR SEARCH
    # ==========================================

    def clear_search(self):

        self.search_entry.delete(0, END)

        self.load_passengers()

        self.set_status("Search cleared.")

    # ==========================================
    # REFRESH PASSENGERS
    # ==========================================

    def refresh_passengers(self):

        self.search_entry.delete(0, END)

        self.load_passengers()

        self.set_status("Passenger list refreshed.")

    # ==========================================
    # STATUS BAR
    # ==========================================

    def create_status_bar(self):

        self.status_bar = ttk.Frame(self.root, padding=(15, 6), bootstyle="secondary")

        self.status_bar.pack(side=BOTTOM, fill=X)

        # Left status
        self.status_label = ttk.Label(
            self.status_bar, text="Ready", bootstyle="inverse-secondary"
        )

        self.status_label.pack(side=LEFT)

        # Right status
        self.time_label = ttk.Label(
            self.status_bar, text="Passenger Management", bootstyle="inverse-secondary"
        )

        self.time_label.pack(side=RIGHT)

    # ==========================================
    # SET STATUS
    # ==========================================

    def set_status(self, message):

        if hasattr(self, "status_label"):

            self.status_label.config(text=message)

    # ==========================================
    # CREATE PASSENGER TABLE
    # ==========================================

    def create_table(self):

        # ======================================
        # TABLE HEADER
        # ======================================

        table_header = ttk.Frame(self.main, padding=(25, 10, 25, 5))

        table_header.pack(fill=X)

        ttk.Label(
            table_header, text="Passenger Records", font=("Segoe UI", 14, "bold")
        ).pack(side=LEFT)

        # Record counter
        self.record_label = ttk.Label(
            table_header, text="0 Records", bootstyle="secondary"
        )

        self.record_label.pack(side=RIGHT)

        # ======================================
        # TABLE FRAME
        # ======================================

        table_frame = ttk.Frame(self.main, padding=(25, 5, 25, 20))

        table_frame.pack(fill=BOTH, expand=True)

        # ======================================
        # COLUMNS
        # ======================================

        columns = (
            "serial",
            "name",
            "phone",
            "email",
            "passport",
            "gender",
            "dob",
            "nationality",
        )

        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        # ======================================
        # HEADINGS
        # ======================================

        # headings = {
        #     "serial": "SL",
        #     "name": "Full Name",
        #     "phone": "Phone",
        #     "email": "Email",
        #     "passport": "Passport",
        #     "gender": "Gender",
        #     "dob": "Date of Birth",
        #     "nationality": "Nationality",
        # }

        # for column, title in headings.items():

        #     self.table.heading(
        #         column, text=title, command=lambda c=column: self.sort_column(c, False)
        #     )

        # Headings
        self.table.heading("serial", text="SL")
        self.table.heading("name", text="Full Name")
        self.table.heading("phone", text="Phone")
        self.table.heading("email", text="Email")
        self.table.heading("passport", text="Passport")
        self.table.heading("gender", text="Gender")
        self.table.heading("dob", text="Date of Birth")
        self.table.heading("nationality", text="Nationality")

        # ======================================
        # COLUMN WIDTH
        # ======================================

        self.table.column("serial", width=60, anchor=CENTER)

        self.table.column("name", width=190, minwidth=150, anchor=CENTER)

        self.table.column("phone", width=130, minwidth=110, anchor=CENTER)

        self.table.column("email", width=220, minwidth=150, anchor=CENTER)

        self.table.column("passport", width=140, minwidth=120, anchor=CENTER)

        self.table.column("gender", width=90, minwidth=80, anchor=CENTER)

        self.table.column("dob", width=120, minwidth=100, anchor=CENTER)

        self.table.column("nationality", width=130, minwidth=100, anchor=CENTER)

        # ======================================
        # SCROLLBAR
        # ======================================

        y_scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.table.yview)

        x_scroll = ttk.Scrollbar(
            table_frame, orient=HORIZONTAL, command=self.table.xview
        )

        self.table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # ======================================
        # GRID
        # ======================================

        self.table.grid(row=0, column=0, sticky=NSEW)

        y_scroll.grid(row=0, column=1, sticky=NS)

        x_scroll.grid(row=1, column=0, sticky=EW)

        table_frame.rowconfigure(0, weight=1)

        table_frame.columnconfigure(0, weight=1)

        # ======================================
        # EMPTY TABLE MESSAGE
        # ======================================

        self.empty_label = ttk.Label(
            table_frame,
            text="No passengers found",
            font=("Segoe UI", 16, "bold"),
            bootstyle="secondary",
        )

        # ======================================
        # EVENTS
        # ======================================

        self.table.bind("<<TreeviewSelect>>", self.on_passenger_select)

        self.table.bind("<Double-1>", self.show_passenger_details)

        self.table.bind("<Delete>", lambda event: self.delete_passenger())

    # ==========================================

    # STATISTICS
    # ==========================================

    def create_statistics(self):

        stats_frame = ttk.Frame(self.main, padding=(25, 15, 25, 10))

        stats_frame.pack(fill=X)

        # ======================================
        # TOTAL PASSENGERS
        # ======================================

        total_card = ttk.Labelframe(
            stats_frame, text=" Total Passengers ", padding=15, bootstyle="primary"
        )

        total_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.total_label = ttk.Label(
            total_card, text="0", font=("Segoe UI", 24, "bold"), bootstyle="primary"
        )

        self.total_label.pack()

        ttk.Label(total_card, text="Registered Passengers").pack()

        # ======================================
        # MALE
        # ======================================

        male_card = ttk.Labelframe(
            stats_frame, text=" Male ", padding=15, bootstyle="info"
        )

        male_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.male_label = ttk.Label(
            male_card, text="0", font=("Segoe UI", 24, "bold"), bootstyle="info"
        )

        self.male_label.pack()

        ttk.Label(male_card, text="Male Passengers").pack()

        # ======================================
        # FEMALE
        # ======================================

        female_card = ttk.Labelframe(
            stats_frame, text=" Female ", padding=15, bootstyle="danger"
        )

        female_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.female_label = ttk.Label(
            female_card, text="0", font=("Segoe UI", 24, "bold"), bootstyle="danger"
        )

        self.female_label.pack()

        ttk.Label(female_card, text="Female Passengers").pack()

        # ======================================
        # INTERNATIONAL
        # ======================================

        international_card = ttk.Labelframe(
            stats_frame, text=" International ", padding=15, bootstyle="warning"
        )

        international_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.international_label = ttk.Label(
            international_card,
            text="0",
            font=("Segoe UI", 24, "bold"),
            bootstyle="warning",
        )

        self.international_label.pack()

        ttk.Label(international_card, text="International").pack()

        # Initial statistics
        self.update_statistics()

    # ==========================================
    # UPDATE STATISTICS
    # ==========================================

    def update_statistics(self):

        try:

            total, male, female, international = self.db.get_passenger_statistics()

            self.total_label.config(text=str(total))

            self.male_label.config(text=str(male))

            self.female_label.config(text=str(female))

            self.international_label.config(text=str(international))

        except Exception as e:

            print("Statistics Error:", e)

        if len(self.table.get_children()) == 0:

            self.empty_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        else:

            self.empty_label.place_forget()

    # ==========================================
    # UPDATE RECORD COUNT
    # ==========================================

    def update_record_count(self):

        count = len(self.table.get_children())

        self.record_label.config(text=f"{count} Records")

    # ==========================================
    # SELECT PASSENGER
    # ==========================================

    # def on_passenger_select(self, event=None):

    #     selected = self.table.selection()

    #     if not selected:
    #         self.selected_passenger_id = None
    #         return

    #     item = self.table.item(selected[0])

    #     values = item.get("values", [])

    #     if not values:
    #         self.selected_passenger_id = None
    #         return

    #     database_id = values[1]
    #     self.selected_passenger_id = database_id
    #     self.set_status(f"Passenger selected: {values[2]} " f"(ID: {database_id})")

    #     # First column = DATABASE ID
    #     database_id = str(values[0]).strip()

    #     if not database_id:
    #         self.selected_passenger_id = None
    #         return

    #     # IMPORTANT:
    #     # Database ID can be I007, I008, etc.
    #     # So DON'T convert it to int.
    #     self.selected_passenger_id = database_id

    #     self.set_status(
    #         f"Passenger selected: {values[1]} " f"(ID: {self.selected_passenger_id})"
    #     )

    def on_passenger_select(self, event=None):

        selected = self.table.selection()

        if not selected:
            self.selected_passenger_id = None
            return

        item_id = selected[0]

        values = self.table.item(item_id, "values")

        if not values:
            self.selected_passenger_id = None
            return

        try:

            # Treeview iid = REAL DATABASE ID
            self.selected_passenger_id = int(item_id)

            self.set_status(
                f"Passenger selected: {values[1]} " f"(Serial: {values[0]})"
            )

        except (ValueError, TypeError):

            self.selected_passenger_id = None

            messagebox.showerror("Selection Error", f"Invalid database ID: {item_id}")

    # ==========================================
    # SHOW PASSENGER DETAILS
    # ==========================================

    def show_passenger_details(self, event=None):

        selected = self.table.selection()

        if not selected:

            return

        item = self.table.item(selected[0])

        values = item.get("values", [])

        if not values:

            return

        details = (
            f"Passenger ID: {values[0]}\n\n"
            f"Full Name: {values[1]}\n\n"
            f"Phone: {values[2]}\n\n"
            f"Email: {values[3]}\n\n"
            f"Passport: {values[4]}\n\n"
            f"Gender: {values[5]}\n\n"
            f"Date of Birth: {values[6]}\n\n"
            f"Nationality: {values[7]}"
        )

        messagebox.showinfo("Passenger Details", details)

    # ==========================================
    # SORT COLUMN
    # ==========================================

    def sort_column(self, column, reverse):

        data = [
            (self.table.set(child, column), child)
            for child in self.table.get_children("")
        ]

        data.sort(reverse=reverse)

        for index, (_, child) in enumerate(data):

            self.table.move(child, "", index)

        self.table.heading(
            column, command=lambda: self.sort_column(column, not reverse)
        )
        # ==========================================

    # ==========================================
    # LOAD PASSENGERS
    # ==========================================

    def load_passengers(self):

        # Clear existing rows
        for item in self.table.get_children():

            self.table.delete(item)

        try:

            # Get data from database
            passengers = self.db.get_passengers()

            # Insert passengers into table
            for serial, passenger in enumerate(passengers, start=1):
                database_id = passenger[0]
                self.table.insert(
                    "",
                    END,
                    iid=str(database_id),
                    values=(
                        serial,
                        passenger[1],  # Name
                        passenger[2],  # Phone
                        passenger[3],  # Email
                        passenger[4],  # Passport
                        passenger[5],  # Gender
                        passenger[6],  # DOB
                        passenger[7],  # Nationality
                    ),
                )

            # Update record count
            self.update_record_count()

            # Empty table message
            self.update_empty_state()

            # Update statistics
            self.update_statistics()

            self.set_status(f"{len(passengers)} passenger(s) loaded.")

        except Exception as e:

            messagebox.showerror("Database Error", f"Unable to load passengers.\n\n{e}")

    # ==========================================
    # EMPTY TABLE STATE
    # ==========================================

    def update_empty_state(self):

        if len(self.table.get_children()) == 0:

            self.empty_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        else:

            self.empty_label.place_forget()

    # ==========================================
    # SEARCH PASSENGER
    # ==========================================

    def search_passenger(self):

        keyword = self.search_entry.get().strip()

        # Empty search = show all
        if not keyword:

            self.load_passengers()

            return

        # Clear table
        for item in self.table.get_children():

            self.table.delete(item)

        try:

            passengers = self.db.search_passengers(keyword)

            # Insert search results
            for passenger in passengers:

                self.table.insert(
                    "",
                    END,
                    values=(
                        passenger[0],  # ID
                        passenger[1],  # Name
                        passenger[2],  # Phone
                        passenger[3],  # Email
                        passenger[4],  # Passport
                        passenger[5],  # Gender
                        passenger[6],  # DOB
                        passenger[7],  # Nationality
                    ),
                )

            # Update UI
            self.update_record_count()

            self.update_empty_state()

            count = len(self.table.get_children())

            self.set_status(f"Search completed — {count} passenger(s) found.")

        except Exception as e:

            messagebox.showerror("Search Error", f"Unable to search passengers.\n\n{e}")

    # ==========================================
    # ADD PASSENGER
    # ==========================================

    def add_passenger(self):

        window = ttk.Toplevel(self.root)

        window.title("Add Passenger")

        window.geometry("600x700")

        window.resizable(False, False)

        # ======================================
        # CENTER WINDOW
        # ======================================

        window.update_idletasks()

        width = 600
        height = 700

        x = window.winfo_screenwidth() // 2 - width // 2

        y = window.winfo_screenheight() // 2 - height // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

        # ======================================
        # HEADER
        # ======================================

        header = ttk.Frame(window, padding=20, bootstyle="primary")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="Add New Passenger",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-primary",
        ).pack()

        ttk.Label(
            header, text="Enter passenger information", bootstyle="inverse-primary"
        ).pack(pady=(5, 0))

        # ======================================
        # FORM
        # ======================================

        form = ttk.Frame(window, padding=30)

        form.pack(fill=BOTH, expand=True)

        # ======================================
        # NAME
        # ======================================

        ttk.Label(form, text="Full Name *").grid(row=0, column=0, sticky=W, pady=8)

        name_entry = ttk.Entry(form, width=40)

        name_entry.grid(row=0, column=1, sticky=EW, pady=8)

        # ======================================
        # PHONE
        # ======================================

        ttk.Label(form, text="Phone *").grid(row=1, column=0, sticky=W, pady=8)

        phone_entry = ttk.Entry(form, width=40)

        phone_entry.grid(row=1, column=1, sticky=EW, pady=8)

        # ======================================
        # EMAIL
        # ======================================

        ttk.Label(form, text="Email").grid(row=2, column=0, sticky=W, pady=8)

        email_entry = ttk.Entry(form, width=40)

        email_entry.grid(row=2, column=1, sticky=EW, pady=8)

        # ======================================
        # PASSPORT
        # ======================================

        ttk.Label(form, text="Passport Number *").grid(
            row=3, column=0, sticky=W, pady=8
        )

        passport_entry = ttk.Entry(form, width=40)

        passport_entry.grid(row=3, column=1, sticky=EW, pady=8)

        # ======================================
        # GENDER
        # ======================================

        ttk.Label(form, text="Gender").grid(row=4, column=0, sticky=W, pady=8)

        gender_combo = ttk.Combobox(
            form, values=["Male", "Female", "Other"], state="readonly", width=37
        )

        gender_combo.grid(row=4, column=1, sticky=EW, pady=8)

        gender_combo.current(0)

        # ======================================
        # DATE OF BIRTH
        # ======================================

        ttk.Label(form, text="Date of Birth").grid(row=5, column=0, sticky=W, pady=8)

        dob_entry = ttk.Entry(form, width=40)

        dob_entry.grid(row=5, column=1, sticky=EW, pady=8)

        dob_entry.insert(0, "DD-MM-YYYY")

        # ======================================
        # NATIONALITY
        # ======================================

        ttk.Label(form, text="Nationality").grid(row=6, column=0, sticky=W, pady=8)

        nationality_entry = ttk.Entry(form, width=40)

        nationality_entry.grid(row=6, column=1, sticky=EW, pady=8)

        nationality_entry.insert(0, "Bangladesh")

        # ======================================
        # ADDRESS
        # ======================================

        ttk.Label(form, text="Address").grid(row=7, column=0, sticky=NW, pady=8)

        address_text = ttk.Text(form, width=40, height=4)

        address_text.grid(row=7, column=1, sticky=EW, pady=8)

        form.columnconfigure(1, weight=1)

        # ======================================
        # SAVE FUNCTION
        # ======================================

        def save_passenger():

            name = name_entry.get().strip()

            phone = phone_entry.get().strip()

            email = email_entry.get().strip()

            passport = passport_entry.get().strip()

            gender = gender_combo.get()

            dob = dob_entry.get().strip()

            nationality = nationality_entry.get().strip()

            address = address_text.get("1.0", END).strip()

            # ==================================
            # VALIDATION
            # ==================================

            if not name:

                messagebox.showwarning(
                    "Validation", "Please enter passenger name.", parent=window
                )

                name_entry.focus()

                return

            if not phone:

                messagebox.showwarning(
                    "Validation", "Please enter phone number.", parent=window
                )

                phone_entry.focus()

                return

            if not passport:

                messagebox.showwarning(
                    "Validation", "Please enter passport number.", parent=window
                )

                passport_entry.focus()

                return

            # ==================================
            # SAVE DATABASE
            # ==================================

            try:

                self.db.add_passenger(
                    name, phone, email, passport, gender, dob, nationality, address
                )

                messagebox.showinfo(
                    "Success", "Passenger added successfully.", parent=window
                )

                window.destroy()

                self.load_passengers()

                self.set_status("Passenger added successfully.")

            except Exception as e:

                messagebox.showerror("Database Error", str(e), parent=window)

        # ======================================
        # BUTTONS
        # ======================================

        button_frame = ttk.Frame(form)

        button_frame.grid(row=8, column=0, columnspan=2, pady=25)

        ttk.Button(
            button_frame, text="Cancel", bootstyle="secondary", command=window.destroy
        ).pack(side=LEFT, padx=8)

        ttk.Button(
            button_frame,
            text="Save Passenger",
            bootstyle="success",
            command=save_passenger,
        ).pack(side=LEFT, padx=8)

        name_entry.focus()

    # ==========================================
    # EDIT PASSENGER
    # ==========================================

    def edit_passenger(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please select a passenger first.")
            return

        item_id = selected[0]
        values = self.table.item(item_id, "values")

        if not values:
            return

        passenger_id = int(item_id)

        # selected = self.table.selection()

        # if not selected:

        #     messagebox.showwarning("No Selection", "Please select a passenger first.")

        #     return
        # # ==========================================
        # # GET HIDDEN DATABASE ID
        # # ==========================================
        # passenger_id = selected[0]

        # # Get Treeview row
        # item = self.table.item(selected[0])

        # values = item.get("values", [])

        # if not values:
        #     messagebox.showwarning(
        #         "Selection Error", "Unable to read passenger information."
        #     )
        #     return

        # DATABASE ID is stored in first column
        # passenger_id = str(values[0]).strip()

        # if not passenger_id:
        #     messagebox.showerror("Error", "Invalid passenger ID.")
        #     return

        # ======================================
        # EDIT WINDOW
        # ======================================

        window = ttk.Toplevel(self.root)

        window.title("Edit Passenger")

        window.geometry("600x700")

        window.resizable(False, False)

        # ======================================
        # CENTER WINDOW
        # ======================================

        window.update_idletasks()

        width = 600
        height = 700

        x = window.winfo_screenwidth() // 2 - width // 2

        y = window.winfo_screenheight() // 2 - height // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

        # ======================================
        # HEADER
        # ======================================

        header = ttk.Frame(window, padding=20, bootstyle="warning")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="Edit Passenger",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-warning",
        ).pack()

        ttk.Label(
            header,
            text=f"Passenger ID: {passenger_id}",
            bootstyle="inverse-warning",
        ).pack(pady=(5, 0))

        # ======================================
        # FORM
        # ======================================

        form = ttk.Frame(window, padding=30)

        form.pack(fill=BOTH, expand=True)

        # ======================================
        # NAME
        # ======================================

        ttk.Label(form, text="Full Name *").grid(row=0, column=0, sticky=W, pady=8)

        name_entry = ttk.Entry(form, width=40)

        name_entry.grid(row=0, column=1, sticky=EW, pady=8)

        name_entry.insert(0, values[1])

        # ======================================
        # PHONE
        # ======================================

        ttk.Label(form, text="Phone *").grid(row=1, column=0, sticky=W, pady=8)

        phone_entry = ttk.Entry(form, width=40)

        phone_entry.grid(row=1, column=1, sticky=EW, pady=8)

        phone_entry.insert(0, values[2])

        # ======================================
        # EMAIL
        # ======================================

        ttk.Label(form, text="Email").grid(row=2, column=0, sticky=W, pady=8)

        email_entry = ttk.Entry(form, width=40)

        email_entry.grid(row=2, column=1, sticky=EW, pady=8)

        email_entry.insert(0, values[3])

        # ======================================
        # PASSPORT
        # ======================================

        ttk.Label(form, text="Passport Number *").grid(
            row=3, column=0, sticky=W, pady=8
        )

        passport_entry = ttk.Entry(form, width=40)

        passport_entry.grid(row=3, column=1, sticky=EW, pady=8)

        passport_entry.insert(0, values[4])

        # ======================================
        # GENDER
        # ======================================

        ttk.Label(form, text="Gender").grid(row=4, column=0, sticky=W, pady=8)

        gender_combo = ttk.Combobox(
            form, values=["Male", "Female", "Other"], state="readonly", width=37
        )

        gender_combo.grid(row=4, column=1, sticky=EW, pady=8)

        gender_combo.set(values[5])

        # ======================================
        # DATE OF BIRTH
        # ======================================

        ttk.Label(form, text="Date of Birth").grid(row=5, column=0, sticky=W, pady=8)

        dob_entry = ttk.Entry(form, width=40)

        dob_entry.grid(row=5, column=1, sticky=EW, pady=8)

        dob_entry.insert(0, values[6])

        # ======================================
        # NATIONALITY
        # ======================================

        ttk.Label(form, text="Nationality").grid(row=6, column=0, sticky=W, pady=8)

        nationality_entry = ttk.Entry(form, width=40)

        nationality_entry.grid(row=6, column=1, sticky=EW, pady=8)

        nationality_entry.insert(0, values[7])

        # ======================================
        # ADDRESS
        # ======================================

        ttk.Label(form, text="Address").grid(row=7, column=0, sticky=NW, pady=8)

        address_text = ttk.Text(form, width=40, height=4)

        address_text.grid(row=7, column=1, sticky=EW, pady=8)

        form.columnconfigure(1, weight=1)

        # ======================================
        # UPDATE FUNCTION
        # ======================================

        def update_data():

            name = name_entry.get().strip()

            phone = phone_entry.get().strip()

            email = email_entry.get().strip()

            passport = passport_entry.get().strip()

            gender = gender_combo.get()

            dob = dob_entry.get().strip()

            nationality = nationality_entry.get().strip()

            address = address_text.get("1.0", END).strip()

            # ==================================
            # VALIDATION
            # ==================================

            if not name:

                messagebox.showwarning(
                    "Validation", "Please enter passenger name.", parent=window
                )

                name_entry.focus()

                return

            if not phone:

                messagebox.showwarning(
                    "Validation", "Please enter phone number.", parent=window
                )

                phone_entry.focus()

                return

            if not passport:

                messagebox.showwarning(
                    "Validation", "Please enter passport number.", parent=window
                )

                passport_entry.focus()

                return

            # ==================================
            # CONFIRM UPDATE
            # ==================================

            confirm = messagebox.askyesno(
                "Confirm Update",
                "Are you sure you want to update this passenger?",
                parent=window,
            )

            if not confirm:

                return

            # ==================================
            # DATABASE UPDATE
            # ==================================

            try:

                result = self.db.update_passenger(
                    passenger_id,
                    name,
                    phone,
                    email,
                    passport,
                    gender,
                    dob,
                    nationality,
                    address,
                )

                if result > 0:

                    messagebox.showinfo(
                        "Success", "Passenger updated successfully.", parent=window
                    )

                    window.destroy()

                    self.load_passengers()

                    self.set_status("Passenger updated successfully.")

                else:

                    messagebox.showwarning(
                        "Update", "No changes were made.", parent=window
                    )

            except Exception as e:

                messagebox.showerror("Database Error", str(e), parent=window)

        # ======================================
        # BUTTONS
        # ======================================

        button_frame = ttk.Frame(form)

        button_frame.grid(row=8, column=0, columnspan=2, pady=25)

        ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            command=window.destroy,
        ).pack(side=LEFT, padx=8)

        ttk.Button(
            button_frame,
            text="Update Passenger",
            bootstyle="warning",
            command=update_data,
        ).pack(side=LEFT, padx=8)

        name_entry.focus()

    # ==========================================
    # DELETE PASSENGER
    # ==========================================

    # def delete_passenger(self):

    #     selected = self.table.selection()

    #     # ======================================
    #     # CHECK SELECTION
    #     # ======================================

    #     if not selected:

    #         messagebox.showwarning("No Selection", "Please select a passenger first.")

    #         return

    #     # ======================================
    #     # GET DATA
    #     # ======================================

    #     item = self.table.item(selected[0])

    #     values = item.get("values", [])

    #     if not values:
    #         messagebox.showwarning(
    #             "Selection Error", "Unable to read passenger information."
    #         )
    #         return
    #     # First column = DATABASE passenger ID
    #     passenger_id = str(values[0]).strip()

    #     if not passenger_id:
    #         messagebox.showerror("Delete Error", "Invalid passenger ID.")
    #         return
    #     passenger_name = values[1]

    #     # ======================================
    #     # CONFIRM DELETE
    #     # ======================================

    #     confirm = messagebox.askyesno(
    #         "Confirm Delete",
    #         (
    #             f"Are you sure you want to delete\n\n"
    #             f"Passenger: {passenger_name}\n"
    #             f"Database ID: {passenger_id}\n\n"
    #             f"This action cannot be undone."
    #         ),
    #     )

    #     if not confirm:

    #         return

    #     # ======================================
    #     # DELETE DATABASE
    #     # ======================================

    #     try:

    #         result = self.db.delete_passenger(passenger_id)

    #         if result > 0:

    #             messagebox.showinfo(
    #                 "Success", f"Passenger '{passenger_name}' " f"deleted successfully."
    #             )

    #             self.load_passengers()

    #             self.selected_passenger_id = None

    #             self.set_status("Passenger deleted successfully.")

    #         else:

    #             messagebox.showwarning("Delete", "Passenger could not be deleted.")

    #     except Exception as e:

    #         messagebox.showerror("Database Error", str(e))

    def delete_passenger(self):

        selected = self.table.selection()

        # No selection
        if not selected:
            messagebox.showwarning("No Selection", "Please select a passenger first.")
            return

        # Selected Treeview item
        item_id = selected[0]

        # Get displayed values
        values = self.table.item(item_id, "values")

        if not values:
            messagebox.showwarning(
                "Selection Error", "Unable to read passenger information."
            )
            return

        # ------------------------------------------
        # REAL DATABASE ID
        # ------------------------------------------
        try:
            passenger_id = int(item_id)

        except (ValueError, TypeError):

            messagebox.showerror("Delete Error", f"Invalid database ID: {item_id}")
            return

        # ------------------------------------------
        # DISPLAY DATA
        # ------------------------------------------
        serial = values[0]
        passenger_name = values[1]

        # ------------------------------------------
        # CONFIRM DELETE
        # ------------------------------------------
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this passenger?\n\n"
            f"Serial: {serial}\n"
            f"Name: {passenger_name}\n"
            f"Database ID: {passenger_id}\n\n"
            f"This action cannot be undone.",
        )

        if not confirm:
            return

        # ------------------------------------------
        # DELETE FROM DATABASE
        # ------------------------------------------
        try:

            result = self.db.delete_passenger(passenger_id)

            if result:

                messagebox.showinfo(
                    "Success", f"Passenger '{passenger_name}' deleted successfully."
                )

                # Reload table
                self.load_passengers()

                self.selected_passenger_id = None

                self.set_status(f"Passenger '{passenger_name}' deleted successfully.")

            else:

                messagebox.showwarning(
                    "Delete Failed", "Passenger could not be deleted."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error", f"Unable to delete passenger.\n\n{e}"
            )
