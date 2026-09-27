import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.database import Database


class FlightWindow:

    def __init__(self, root):

        self.root = root

        self.db = Database()

        self.build_ui()

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        self.main = ttk.Frame(self.root)
        self.main.pack(fill=BOTH, expand=True)

        self.create_header()
        self.create_toolbar()
        self.create_statistics()
        self.create_table()
        self.create_status_bar()

        self.load_flights()

    # ==========================================
    # LOAD FLIGHTS
    # ==========================================

    def load_flights(self):

        try:

            for item in self.table.get_children():
                self.table.delete(item)

            flights = self.db.get_all_flights()

            serial = 1

            for flight in flights:

                (
                    flight_id,
                    flight_number,
                    airline,
                    departure,
                    arrival,
                    departure_date,
                    departure_time,
                    arrival_time,
                    aircraft,
                    total_seats,
                    available_seats,
                    price,
                    status,
                ) = flight

                self.table.insert(
                    "",
                    END,
                    values=(
                        serial,
                        flight_number,
                        airline,
                        departure,
                        arrival,
                        departure_date,
                        aircraft,
                        total_seats,
                        available_seats,
                        f"৳ {price:,.2f}",
                        status,
                    ),
                )

                serial += 1

            # ======================================
            # IMPORTANT
            # ======================================

            self.update_statistics()

            self.status_label.config(text=f"{len(flights)} flight(s) loaded")

        except Exception as e:

            print("Load Flights Error:", e)

    # ==========================================
    # UPDATE STATISTICS
    # ==========================================

    def update_statistics(self):

        try:

            flights = self.db.get_all_flights()

            # Counters
            total = 0
            scheduled = 0
            boarding = 0
            departed = 0
            delayed = 0
            completed = 0
            cancelled = 0

            # ======================================
            # COUNT EVERY FLIGHT
            # ======================================

            for flight in flights:

                total += 1

                status = str(flight[12]).strip().lower()

                if status == "scheduled":
                    scheduled += 1

                elif status == "boarding":
                    boarding += 1

                elif status == "departed":
                    departed += 1

                elif status == "delayed":
                    delayed += 1

                elif status == "completed":
                    completed += 1

                elif status == "cancelled":
                    cancelled += 1

            # ======================================
            # UPDATE ALL CARDS
            # ======================================

            self.update_stat_card(self.total_card, total)

            self.update_stat_card(self.scheduled_card, scheduled)

            self.update_stat_card(self.boarding_card, boarding)

            self.update_stat_card(self.departed_card, departed)

            self.update_stat_card(self.delayed_card, delayed)

            self.update_stat_card(self.completed_card, completed)

            self.update_stat_card(self.cancelled_card, cancelled)

        except Exception as e:

            print("Flight Statistics Error:", e)

    # ==========================================
    # UPDATE SINGLE CARD
    # ==========================================

    def update_stat_card(self, card, value):

        for widget in card.winfo_children():

            if isinstance(widget, ttk.Label):
                widget.config(text=str(value))

        # ==========================================
        # HEADER

    # ==========================================

    def create_header(self):

        header = ttk.Frame(self.main, padding=(25, 20), bootstyle="primary")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="Flight Management",
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-primary",
        ).pack(side=LEFT)

        ttk.Label(
            header,
            text="Manage airline flights",
            font=("Segoe UI", 10),
            bootstyle="inverse-primary",
        ).pack(side=LEFT, padx=20)

    # ==========================================
    # TOOLBAR
    # ==========================================
    def create_toolbar(self):

        toolbar = ttk.Frame(self.main, padding=(25, 15))

        toolbar.pack(fill=X)

        # ==========================================
        # ADD
        # ==========================================

        ttk.Button(
            toolbar, text="+ Add Flight", bootstyle="success", command=self.add_flight
        ).pack(side=LEFT, padx=5)

        # ==========================================
        # EDIT
        # ==========================================

        ttk.Button(
            toolbar, text="✎ Edit", bootstyle="warning", command=self.edit_flight
        ).pack(side=LEFT, padx=5)

        # ==========================================
        # DELETE
        # ==========================================

        ttk.Button(
            toolbar, text="✕ Delete", bootstyle="danger", command=self.delete_flight
        ).pack(side=LEFT, padx=5)

        # ==========================================
        # REFRESH
        # ==========================================

        ttk.Button(
            toolbar, text="⟳ Refresh", bootstyle="info", command=self.load_flights
        ).pack(side=LEFT, padx=5)

        # ==========================================
        # STATUS FILTER
        # ==========================================

        # ttk.Label(toolbar, text="Status:").pack(side=RIGHT, padx=(15, 5))

        self.status_filter = ttk.Combobox(
            toolbar,
            values=[
                "All",
                "Scheduled",
                "Boarding",
                "Departed",
                "Completed",
                "Delayed",
                "Cancelled",
            ],
            state="readonly",
            width=15,
        )

        self.status_filter.pack(side=RIGHT, padx=5)

        self.status_filter.set("Status")

        self.status_filter.bind(
            "<<ComboboxSelected>>", lambda event: self.search_flights()
        )

        # ==========================================
        # SEARCH
        # ==========================================

        self.search_entry = ttk.Entry(toolbar, width=30)

        self.search_entry.pack(side=RIGHT, padx=5)

        ttk.Button(
            toolbar, text="🔍 Search", bootstyle="primary", command=self.search_flights
        ).pack(side=RIGHT, padx=5)

        self.search_entry.bind("<Return>", lambda event: self.search_flights())

    # ==========================================
    # STATISTICS
    # ==========================================

    def create_statistics(self):
        stats = ttk.Frame(self.main, padding=(25, 5))
        stats.pack(fill=X)

        row1 = ttk.Frame(stats)
        row1.pack(fill=X, pady=5)

        self.total_card = self.create_stat_card(row1, "Total Flights", "0", "primary")
        self.total_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.scheduled_card = self.create_stat_card(row1, "Scheduled", "0", "success")

        self.scheduled_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.boarding_card = self.create_stat_card(row1, "Boarding", "0", "info")

        self.boarding_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.departed_card = self.create_stat_card(row1, "Departed", "0", "secondary")

        self.departed_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        # Row 2
        row2 = ttk.Frame(stats)
        row2.pack(fill=X, pady=5)
        self.delayed_card = self.create_stat_card(row2, "Delayed", "0", "warning")
        self.delayed_card.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.completed_card = self.create_stat_card(row2, "Completed", "0", "success")
        self.completed_card.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.cancelled_card = self.create_stat_card(row2, "Cancelled", "0", "danger")
        self.cancelled_card.pack(side=LEFT, fill=X, expand=True, padx=5)

    def create_stat_card(self, parent, title, value, style):

        card = ttk.Labelframe(parent, text=f" {title} ", padding=15, bootstyle=style)

        label = ttk.Label(
            card, text=value, font=("Segoe UI", 22, "bold"), bootstyle=style
        )

        label.pack()

        return card

    # ==========================================
    # FLIGHT TABLE
    # ==========================================

    def create_table(self):

        table_frame = ttk.Frame(self.main, padding=(25, 10, 25, 20))

        table_frame.pack(fill=BOTH, expand=True)

        columns = (
            "id",
            "flight_no",
            "airline",
            "departure",
            "arrival",
            "date",
            "aircraft",
            "seats",
            "available",
            "price",
            "status",
        )

        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        # ==========================================
        # STATUS TAG COLORS
        # ==========================================

        self.table.tag_configure("Scheduled", foreground="#198754")

        self.table.tag_configure("Boarding", foreground="#fd7e14")

        self.table.tag_configure("Departed", foreground="#0dcaf0")

        self.table.tag_configure("Completed", foreground="#198754")

        self.table.tag_configure("Delayed", foreground="#ffc107")

        self.table.tag_configure("Cancelled", foreground="#dc3545")

        headings = {
            "id": "ID",
            "flight_no": "Flight No.",
            "airline": "Airline",
            "departure": "Departure",
            "arrival": "Arrival",
            "date": "Date",
            "aircraft": "Aircraft",
            "seats": "Seats",
            "available": "Available",
            "price": "Price",
            "status": "Status",
        }

        for column, title in headings.items():

            self.table.heading(column, text=title)

        self.table.column("id", width=60, anchor=CENTER)

        self.table.column("flight_no", width=110, anchor=CENTER)

        self.table.column("airline", width=180, anchor=CENTER)

        self.table.column("departure", width=130, anchor=CENTER)

        self.table.column("arrival", width=130, anchor=CENTER)

        self.table.column("date", width=110, anchor=CENTER)

        self.table.column("aircraft", width=120, anchor=CENTER)

        self.table.column("seats", width=80, anchor=CENTER)

        self.table.column("available", width=90, anchor=CENTER)

        self.table.column("price", width=110, anchor=CENTER)

        self.table.column("status", width=110, anchor=CENTER)

        y_scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.table.yview)

        x_scroll = ttk.Scrollbar(
            table_frame, orient=HORIZONTAL, command=self.table.xview
        )

        self.table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.table.grid(row=0, column=0, sticky=NSEW)

        y_scroll.grid(row=0, column=1, sticky=NS)

        x_scroll.grid(row=1, column=0, sticky=EW)

        table_frame.rowconfigure(0, weight=1)

        table_frame.columnconfigure(0, weight=1)

        self.table.bind("<Double-1>", lambda event: self.edit_flight())

    # ==========================================
    # STATUS BAR
    # ==========================================

    def create_status_bar(self):

        self.status_bar = ttk.Frame(self.main, padding=(15, 6), bootstyle="secondary")

        self.status_bar.pack(fill=X, side=BOTTOM)

        self.status_label = ttk.Label(
            self.status_bar, text="Ready", bootstyle="inverse-secondary"
        )

        self.status_label.pack(side=LEFT)

        ttk.Label(
            self.status_bar,
            text="SkyLink Pro • Flight Management",
            bootstyle="inverse-secondary",
        ).pack(side=RIGHT)

    # ==========================================
    # METHODS
    # ==========================================

    def add_flight(self):

        # ==========================================
        # WINDOW
        # ==========================================

        window = ttk.Toplevel(self.root)

        window.title("Add New Flight")
        window.geometry("700x750")

        window.resizable(False, False)

        window.transient(self.root)
        window.grab_set()

        # Center
        window.update_idletasks()

        width = 700
        height = 750

        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

        # ==========================================
        # HEADER
        # ==========================================

        header = ttk.Frame(window, padding=20, bootstyle="primary")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="✈  Add New Flight",
            font=("Segoe UI", 22, "bold"),
            bootstyle="inverse-primary",
        ).pack()

        ttk.Label(
            header,
            text="Enter flight information",
            font=("Segoe UI", 10),
            bootstyle="inverse-primary",
        ).pack(pady=(5, 0))

        # ==========================================
        # FORM
        # ==========================================

        form = ttk.Frame(window, padding=30)

        form.pack(fill=BOTH, expand=True)

        form.columnconfigure(1, weight=1)

        # ==========================================
        # FLIGHT NUMBER
        # ==========================================

        ttk.Label(form, text="Flight Number *").grid(row=0, column=0, sticky=W, pady=8)

        flight_no_entry = ttk.Entry(form, width=40)

        flight_no_entry.grid(row=0, column=1, sticky=EW, pady=8)

        # ==========================================
        # AIRLINE
        # ==========================================

        ttk.Label(form, text="Airline *").grid(row=1, column=0, sticky=W, pady=8)

        airline_combo = ttk.Combobox(
            form,
            values=[
                "Biman Bangladesh Airlines",
                "US-Bangla Airlines",
                "Air Astra",
                "Emirates",
                "Qatar Airways",
                "Turkish Airlines",
                "Singapore Airlines",
                "Malaysia Airlines",
                "Thai Airways",
                "Other",
            ],
            width=37,
        )

        airline_combo.grid(row=1, column=1, sticky=EW, pady=8)

        # ==========================================
        # DEPARTURE
        # ==========================================

        ttk.Label(form, text="Departure *").grid(row=2, column=0, sticky=W, pady=8)

        departure_entry = ttk.Entry(form, width=40)

        departure_entry.grid(row=2, column=1, sticky=EW, pady=8)

        # ==========================================
        # ARRIVAL
        # ==========================================

        ttk.Label(form, text="Arrival *").grid(row=3, column=0, sticky=W, pady=8)

        arrival_entry = ttk.Entry(form, width=40)

        arrival_entry.grid(row=3, column=1, sticky=EW, pady=8)

        # ==========================================
        # DATE
        # ==========================================

        ttk.Label(form, text="Departure Date *").grid(row=4, column=0, sticky=W, pady=8)

        date_entry = ttk.Entry(form, width=40)

        date_entry.grid(row=4, column=1, sticky=EW, pady=8)

        ttk.Label(
            form, text="Format: YYYY-MM-DD", font=("Segoe UI", 8), bootstyle="secondary"
        ).grid(row=5, column=1, sticky=W)

        # ==========================================
        # DEPARTURE TIME
        # ==========================================

        ttk.Label(form, text="Departure Time *").grid(row=6, column=0, sticky=W, pady=8)

        departure_time_entry = ttk.Entry(form, width=40)

        departure_time_entry.grid(row=6, column=1, sticky=EW, pady=8)

        # ==========================================
        # ARRIVAL TIME
        # ==========================================

        ttk.Label(form, text="Arrival Time *").grid(row=7, column=0, sticky=W, pady=8)

        arrival_time_entry = ttk.Entry(form, width=40)

        arrival_time_entry.grid(row=7, column=1, sticky=EW, pady=8)

        # ==========================================
        # AIRCRAFT
        # ==========================================

        ttk.Label(form, text="Aircraft *").grid(row=8, column=0, sticky=W, pady=8)

        aircraft_combo = ttk.Combobox(
            form,
            values=[
                "Boeing 737",
                "Boeing 777",
                "Boeing 787",
                "Airbus A320",
                "Airbus A330",
                "Airbus A350",
                "Airbus A380",
                "ATR 72",
            ],
            state="readonly",
            width=37,
        )

        aircraft_combo.grid(row=8, column=1, sticky=EW, pady=8)

        # ==========================================
        # TOTAL SEATS
        # ==========================================

        ttk.Label(form, text="Total Seats *").grid(row=9, column=0, sticky=W, pady=8)

        seats_entry = ttk.Entry(form, width=40)

        seats_entry.grid(row=9, column=1, sticky=EW, pady=8)

        # ==========================================
        # PRICE
        # ==========================================

        ttk.Label(form, text="Ticket Price *").grid(row=10, column=0, sticky=W, pady=8)

        price_entry = ttk.Entry(form, width=40)

        price_entry.grid(row=10, column=1, sticky=EW, pady=8)

        # ==========================================
        # STATUS
        # ==========================================

        ttk.Label(form, text="Flight Status").grid(row=11, column=0, sticky=W, pady=8)

        status_combo = ttk.Combobox(
            form,
            values=[
                "Scheduled",
                "Boarding",
                "Departed",
                "Completed",
                "Delayed",
                "Cancelled",
            ],
            state="readonly",
            width=37,
        )

        status_combo.grid(row=11, column=1, sticky=EW, pady=8)

        status_combo.set("Scheduled")

        # ==========================================
        # BUTTON FRAME
        # ==========================================

        button_frame = ttk.Frame(form)

        button_frame.grid(row=12, column=0, columnspan=2, pady=25)

        # ==========================================
        # SAVE FUNCTION
        # ==========================================

        def save_flight():

            # GET VALUES
            flight_no = flight_no_entry.get().strip()

            airline = airline_combo.get().strip()
            departure = departure_entry.get().strip()
            arrival = arrival_entry.get().strip()
            flight_date = date_entry.get().strip()
            departure_time = departure_time_entry.get().strip()
            arrival_time = arrival_time_entry.get().strip()
            aircraft = aircraft_combo.get().strip()
            total_seats = seats_entry.get().strip()
            price = price_entry.get().strip()
            status = status_combo.get().strip()

            # ======================================
            # REQUIRED FIELDS
            # ======================================

            required_fields = [
                (flight_no, flight_no_entry, "Flight Number"),
                (airline, airline_combo, "Airline"),
                (departure, departure_entry, "Departure"),
                (arrival, arrival_entry, "Arrival"),
                (flight_date, date_entry, "Departure Date"),
                (departure_time, departure_time_entry, "Departure Time"),
                (arrival_time, arrival_time_entry, "Arrival Time"),
                (aircraft, aircraft_combo, "Aircraft"),
                (total_seats, seats_entry, "Total Seats"),
                (price, price_entry, "Ticket Price"),
            ]

            for value, widget, field_name in required_fields:

                if not value:

                    messagebox.showwarning(
                        "Validation",
                        f"Please enter/select {field_name}.",
                        parent=window,
                    )

                    widget.focus()

                    return

            # ======================================
            # SEATS
            # ======================================

            try:

                total_seats_value = int(total_seats)

                if total_seats_value <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation",
                    "Total Seats must be a positive number.",
                    parent=window,
                )

                seats_entry.focus()

                return

            # ======================================
            # PRICE
            # ======================================

            try:

                price_value = float(price)

                if price_value <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation",
                    "Ticket Price must be a positive number.",
                    parent=window,
                )

                price_entry.focus()

                return

            # ======================================
            # DATE
            # ======================================

            import datetime

            try:

                datetime.datetime.strptime(flight_date, "%Y-%m-%d")

            except ValueError:

                messagebox.showwarning(
                    "Validation", "Invalid date.\nUse YYYY-MM-DD.", parent=window
                )

                date_entry.focus()

                return

            # ======================================
            # CONFIRM
            # ======================================

            confirm = messagebox.askyesno(
                "Confirm Flight",
                f"Add flight {flight_no}?\n\n"
                f"{departure} → {arrival}\n"
                f"Date: {flight_date}\n"
                f"Seats: {total_seats_value}\n"
                f"Price: ৳ {price_value:,.2f}",
                parent=window,
            )

            if not confirm:
                return

            # ======================================
            # DATABASE
            # ======================================

            try:

                result = self.db.add_flight(
                    flight_number=flight_no,
                    airline=airline,
                    departure=departure,
                    arrival=arrival,
                    departure_date=flight_date,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    aircraft=aircraft,
                    total_seats=total_seats_value,
                    price=price_value,
                    status=status,
                )

                if result:

                    messagebox.showinfo(
                        "Success",
                        f"Flight {flight_no} added successfully!",
                        parent=window,
                    )

                    window.destroy()

                    self.load_flights()

                else:

                    messagebox.showerror(
                        "Error", "Flight Number already exists.", parent=window
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error", f"Unable to save flight.\n\n{e}", parent=window
                )

        # ==========================================
        # CANCEL BUTTON
        # ==========================================

        ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            width=15,
            command=window.destroy,
        ).pack(side=LEFT, padx=8)

        # ==========================================
        # SAVE BUTTON
        # ==========================================

        ttk.Button(
            button_frame,
            text="✓ Save Flight",
            bootstyle="success",
            width=20,
            command=save_flight,
        ).pack(side=LEFT, padx=8)

        # ==========================================
        # FOCUS
        # ==========================================

        flight_no_entry.focus()

    def edit_flight(self):

        # ==========================================
        # CHECK SELECTION
        # ==========================================

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection", "Please select a flight to edit.", parent=self.root
            )

            return

        # ==========================================
        # GET SELECTED FLIGHT
        # ==========================================

        item = self.table.item(selected[0])

        values = item["values"]

        flight_id = values[0]

        # ==========================================
        # GET FULL DATA FROM DATABASE
        # ==========================================

        flights = self.db.get_all_flights()

        selected_flight = None

        for flight in flights:

            if flight[0] == flight_id:

                selected_flight = flight

                break

        if selected_flight is None:

            messagebox.showerror(
                "Error", "Selected flight could not be found.", parent=self.root
            )

            return

        (
            flight_id,
            flight_number,
            airline,
            departure,
            arrival,
            departure_date,
            departure_time,
            arrival_time,
            aircraft,
            total_seats,
            available_seats,
            price,
            status,
        ) = selected_flight

        # ==========================================
        # EDIT WINDOW
        # ==========================================

        window = ttk.Toplevel(self.root)

        window.title("Edit Flight")

        window.geometry("700x750")

        window.resizable(False, False)

        window.transient(self.root)

        window.grab_set()

        # ==========================================
        # CENTER WINDOW
        # ==========================================

        window.update_idletasks()

        width = 700
        height = 750

        x = window.winfo_screenwidth() // 2 - width // 2

        y = window.winfo_screenheight() // 2 - height // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

        # ==========================================
        # HEADER
        # ==========================================

        header = ttk.Frame(window, padding=20, bootstyle="warning")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="✎  Edit Flight",
            font=("Segoe UI", 22, "bold"),
            bootstyle="inverse-warning",
        ).pack()

        ttk.Label(
            header,
            text=f"Update flight {flight_number}",
            font=("Segoe UI", 10),
            bootstyle="inverse-warning",
        ).pack(pady=(5, 0))

        # ==========================================
        # FORM
        # ==========================================

        form = ttk.Frame(window, padding=30)

        form.pack(fill=BOTH, expand=True)

        form.columnconfigure(1, weight=1)

        # ==========================================
        # FLIGHT NUMBER
        # ==========================================

        ttk.Label(form, text="Flight Number *").grid(row=0, column=0, sticky=W, pady=8)

        flight_no_entry = ttk.Entry(form, width=40)

        flight_no_entry.grid(row=0, column=1, sticky=EW, pady=8)

        flight_no_entry.insert(0, flight_number)

        # ==========================================
        # AIRLINE
        # ==========================================

        ttk.Label(form, text="Airline *").grid(row=1, column=0, sticky=W, pady=8)

        airline_combo = ttk.Combobox(
            form,
            values=[
                "Biman Bangladesh Airlines",
                "US-Bangla Airlines",
                "Air Astra",
                "Emirates",
                "Qatar Airways",
                "Turkish Airlines",
                "Singapore Airlines",
                "Malaysia Airlines",
                "Thai Airways",
                "Other",
            ],
            width=37,
        )

        airline_combo.grid(row=1, column=1, sticky=EW, pady=8)

        airline_combo.set(airline)

        # ==========================================
        # DEPARTURE
        # ==========================================

        ttk.Label(form, text="Departure *").grid(row=2, column=0, sticky=W, pady=8)

        departure_entry = ttk.Entry(form, width=40)

        departure_entry.grid(row=2, column=1, sticky=EW, pady=8)

        departure_entry.insert(0, departure)

        # ==========================================
        # ARRIVAL
        # ==========================================

        ttk.Label(form, text="Arrival *").grid(row=3, column=0, sticky=W, pady=8)

        arrival_entry = ttk.Entry(form, width=40)

        arrival_entry.grid(row=3, column=1, sticky=EW, pady=8)

        arrival_entry.insert(0, arrival)

        # ==========================================
        # DATE
        # ==========================================

        ttk.Label(form, text="Departure Date *").grid(row=4, column=0, sticky=W, pady=8)

        date_entry = ttk.Entry(form, width=40)

        date_entry.grid(row=4, column=1, sticky=EW, pady=8)

        date_entry.insert(0, departure_date)

        ttk.Label(
            form, text="Format: YYYY-MM-DD", font=("Segoe UI", 8), bootstyle="secondary"
        ).grid(row=5, column=1, sticky=W)

        # ==========================================
        # DEPARTURE TIME
        # ==========================================

        ttk.Label(form, text="Departure Time *").grid(row=6, column=0, sticky=W, pady=8)

        departure_time_entry = ttk.Entry(form, width=40)

        departure_time_entry.grid(row=6, column=1, sticky=EW, pady=8)

        departure_time_entry.insert(0, departure_time)

        # ==========================================
        # ARRIVAL TIME
        # ==========================================

        ttk.Label(form, text="Arrival Time *").grid(row=7, column=0, sticky=W, pady=8)

        arrival_time_entry = ttk.Entry(form, width=40)

        arrival_time_entry.grid(row=7, column=1, sticky=EW, pady=8)

        arrival_time_entry.insert(0, arrival_time)

        # ==========================================
        # AIRCRAFT
        # ==========================================

        ttk.Label(form, text="Aircraft *").grid(row=8, column=0, sticky=W, pady=8)

        aircraft_combo = ttk.Combobox(
            form,
            values=[
                "Boeing 737",
                "Boeing 777",
                "Boeing 787",
                "Airbus A320",
                "Airbus A330",
                "Airbus A350",
                "Airbus A380",
                "ATR 72",
            ],
            state="readonly",
            width=37,
        )

        aircraft_combo.grid(row=8, column=1, sticky=EW, pady=8)

        aircraft_combo.set(aircraft)

        # ==========================================
        # TOTAL SEATS
        # ==========================================

        ttk.Label(form, text="Total Seats *").grid(row=9, column=0, sticky=W, pady=8)

        seats_entry = ttk.Entry(form, width=40)

        seats_entry.grid(row=9, column=1, sticky=EW, pady=8)

        seats_entry.insert(0, str(total_seats))

        # ==========================================
        # PRICE
        # ==========================================

        ttk.Label(form, text="Ticket Price *").grid(row=10, column=0, sticky=W, pady=8)

        price_entry = ttk.Entry(form, width=40)

        price_entry.grid(row=10, column=1, sticky=EW, pady=8)

        price_entry.insert(0, str(price))

        # ==========================================
        # STATUS
        # ==========================================

        ttk.Label(form, text="Flight Status").grid(row=11, column=0, sticky=W, pady=8)

        status_combo = ttk.Combobox(
            form,
            values=[
                "Scheduled",
                "Boarding",
                "Departed",
                "Completed",
                "Delayed",
                "Cancelled",
            ],
            state="readonly",
            width=37,
        )

        status_combo.grid(row=11, column=1, sticky=EW, pady=8)

        status_combo.set(status)

        # ==========================================
        # BUTTON FRAME
        # ==========================================

        button_frame = ttk.Frame(form)

        button_frame.grid(row=12, column=0, columnspan=2, pady=25)

        # ==========================================
        # UPDATE FUNCTION
        # ==========================================

        def update_flight():

            new_flight_no = flight_no_entry.get().strip()
            new_airline = airline_combo.get().strip()
            new_departure = departure_entry.get().strip()
            new_arrival = arrival_entry.get().strip()
            new_date = date_entry.get().strip()
            new_departure_time = departure_time_entry.get().strip()
            new_arrival_time = arrival_time_entry.get().strip()
            new_aircraft = aircraft_combo.get().strip()
            new_seats = seats_entry.get().strip()
            new_price = price_entry.get().strip()
            new_status = status_combo.get().strip()

            # ======================================
            # REQUIRED FIELDS
            # ======================================

            required = [
                (new_flight_no, flight_no_entry, "Flight Number"),
                (new_airline, airline_combo, "Airline"),
                (new_departure, departure_entry, "Departure"),
                (new_arrival, arrival_entry, "Arrival"),
                (new_date, date_entry, "Departure Date"),
                (new_departure_time, departure_time_entry, "Departure Time"),
                (new_arrival_time, arrival_time_entry, "Arrival Time"),
                (new_aircraft, aircraft_combo, "Aircraft"),
            ]

            for value, widget, field_name in required:

                if not value:

                    messagebox.showwarning(
                        "Validation",
                        f"Please enter/select {field_name}.",
                        parent=window,
                    )

                    widget.focus()

                    return

            # ======================================
            # SEATS
            # ======================================

            try:

                seats_value = int(new_seats)

                if seats_value <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation",
                    "Total Seats must be a positive number.",
                    parent=window,
                )

                seats_entry.focus()

                return

            # ======================================
            # PRICE
            # ======================================

            try:

                price_value = float(new_price)

                if price_value <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation",
                    "Ticket Price must be a positive number.",
                    parent=window,
                )

                price_entry.focus()

                return

            # ======================================
            # DATE
            # ======================================

            import datetime

            try:

                datetime.datetime.strptime(new_date, "%Y-%m-%d")

            except ValueError:

                messagebox.showwarning(
                    "Validation", "Invalid date.\nUse YYYY-MM-DD.", parent=window
                )

                date_entry.focus()

                return

            # ======================================
            # CONFIRM
            # ======================================

            confirm = messagebox.askyesno(
                "Update Flight",
                f"Update flight {new_flight_no}?\n\n"
                f"{new_departure} → {new_arrival}\n"
                f"Date: {new_date}\n"
                f"Seats: {seats_value}\n"
                f"Price: ৳ {price_value:,.2f}\n"
                f"Status: {new_status}",
                parent=window,
            )

            if not confirm:
                return

            # ======================================
            # DATABASE UPDATE
            # ======================================

            try:

                result = self.db.update_flight(
                    flight_id=flight_id,
                    flight_number=new_flight_no,
                    airline=new_airline,
                    departure=new_departure,
                    arrival=new_arrival,
                    departure_date=new_date,
                    departure_time=new_departure_time,
                    arrival_time=new_arrival_time,
                    aircraft=new_aircraft,
                    total_seats=seats_value,
                    price=price_value,
                    status=new_status,
                )

                if result:

                    messagebox.showinfo(
                        "Success",
                        f"Flight {new_flight_no} updated successfully!",
                        parent=window,
                    )

                    window.destroy()

                    self.load_flights()

                else:

                    messagebox.showerror(
                        "Update Error",
                        "Flight could not be updated.\n"
                        "Flight Number may already exist.",
                        parent=window,
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error", f"Unable to update flight.\n\n{e}", parent=window
                )

        # ==========================================
        # CANCEL
        # ==========================================

        ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            width=15,
            command=window.destroy,
        ).pack(side=LEFT, padx=8)

        # ==========================================
        # UPDATE
        # ==========================================

        ttk.Button(
            button_frame,
            text="✓ Update Flight",
            bootstyle="warning",
            width=20,
            command=update_flight,
        ).pack(side=LEFT, padx=8)

        # ==========================================
        # FOCUS
        # ==========================================

        flight_no_entry.focus()

        # ==========================================
        # GET FLIGHT DATA
        # ==========================================

        item = self.table.item(selected[0])

        values = item["values"]

        flight_id = values[0]

        # Find complete record from database
        flights = self.db.get_all_flights()

        flight = None

        for row in flights:

            if row[0] == flight_id:

                flight = row

                break

        if not flight:

            messagebox.showerror(
                "Error", "Flight information not found.", parent=self.root
            )

            return

        (
            flight_id,
            flight_number,
            airline,
            departure,
            arrival,
            departure_date,
            departure_time,
            arrival_time,
            aircraft,
            total_seats,
            available_seats,
            price,
            status,
        ) = flight

        # ==========================================
        # EDIT WINDOW
        # ==========================================

        window = ttk.Toplevel(self.root)

        window.title("Edit Flight")

        window.geometry("700x750")

        window.resizable(False, False)

        window.transient(self.root)

        window.grab_set()

        # ==========================================
        # CENTER WINDOW
        # ==========================================

        window.update_idletasks()

        width = 700
        height = 750

        x = (window.winfo_screenwidth() // 2) - (width // 2)

        y = (window.winfo_screenheight() // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

        # ==========================================
        # HEADER
        # ==========================================

        header = ttk.Frame(window, padding=20, bootstyle="warning")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="✎  Edit Flight",
            font=("Segoe UI", 22, "bold"),
            bootstyle="inverse-warning",
        ).pack()

        ttk.Label(
            header,
            text=f"Update flight {flight_number}",
            font=("Segoe UI", 10),
            bootstyle="inverse-warning",
        ).pack(pady=(5, 0))

        # ==========================================
        # FORM
        # ==========================================

        form = ttk.Frame(window, padding=30)

        form.pack(fill=BOTH, expand=True)

        form.columnconfigure(1, weight=1)

        # ==========================================
        # FLIGHT NUMBER
        # ==========================================

        ttk.Label(form, text="Flight Number *").grid(row=0, column=0, sticky=W, pady=8)

        flight_no_entry = ttk.Entry(form, width=40)

        flight_no_entry.grid(row=0, column=1, sticky=EW, pady=8)

        flight_no_entry.insert(0, flight_number)

        # ==========================================
        # AIRLINE
        # ==========================================

        ttk.Label(form, text="Airline *").grid(row=1, column=0, sticky=W, pady=8)

        airline_combo = ttk.Combobox(
            form,
            values=[
                "Biman Bangladesh Airlines",
                "US-Bangla Airlines",
                "Air Astra",
                "Emirates",
                "Qatar Airways",
                "Turkish Airlines",
                "Singapore Airlines",
                "Malaysia Airlines",
                "Thai Airways",
                "Other",
            ],
            width=37,
        )

        airline_combo.grid(row=1, column=1, sticky=EW, pady=8)

        airline_combo.set(airline)

        # ==========================================
        # DEPARTURE
        # ==========================================

        ttk.Label(form, text="Departure *").grid(row=2, column=0, sticky=W, pady=8)

        departure_entry = ttk.Entry(form, width=40)

        departure_entry.grid(row=2, column=1, sticky=EW, pady=8)

        departure_entry.insert(0, departure)

        # ==========================================
        # ARRIVAL
        # ==========================================

        ttk.Label(form, text="Arrival *").grid(row=3, column=0, sticky=W, pady=8)

        arrival_entry = ttk.Entry(form, width=40)

        arrival_entry.grid(row=3, column=1, sticky=EW, pady=8)

        arrival_entry.insert(0, arrival)

        # ==========================================
        # DATE
        # ==========================================

        ttk.Label(form, text="Departure Date *").grid(row=4, column=0, sticky=W, pady=8)

        date_entry = ttk.Entry(form, width=40)

        date_entry.grid(row=4, column=1, sticky=EW, pady=8)

        date_entry.insert(0, departure_date)

        ttk.Label(
            form, text="Format: YYYY-MM-DD", font=("Segoe UI", 8), bootstyle="secondary"
        ).grid(row=5, column=1, sticky=W)

        # ==========================================
        # DEPARTURE TIME
        # ==========================================

        ttk.Label(form, text="Departure Time *").grid(row=6, column=0, sticky=W, pady=8)

        departure_time_entry = ttk.Entry(form, width=40)

        departure_time_entry.grid(row=6, column=1, sticky=EW, pady=8)

        departure_time_entry.insert(0, departure_time)

        # ==========================================
        # ARRIVAL TIME
        # ==========================================

        ttk.Label(form, text="Arrival Time *").grid(row=7, column=0, sticky=W, pady=8)

        arrival_time_entry = ttk.Entry(form, width=40)

        arrival_time_entry.grid(row=7, column=1, sticky=EW, pady=8)

        arrival_time_entry.insert(0, arrival_time)

        # ==========================================
        # AIRCRAFT
        # ==========================================

        ttk.Label(form, text="Aircraft *").grid(row=8, column=0, sticky=W, pady=8)

        aircraft_combo = ttk.Combobox(
            form,
            values=[
                "Boeing 737",
                "Boeing 777",
                "Boeing 787",
                "Airbus A320",
                "Airbus A330",
                "Airbus A350",
                "Airbus A380",
                "ATR 72",
            ],
            state="readonly",
            width=37,
        )

        aircraft_combo.grid(row=8, column=1, sticky=EW, pady=8)

        aircraft_combo.set(aircraft)

        # ==========================================
        # TOTAL SEATS
        # ==========================================

        ttk.Label(form, text="Total Seats *").grid(row=9, column=0, sticky=W, pady=8)

        seats_entry = ttk.Entry(form, width=40)

        seats_entry.grid(row=9, column=1, sticky=EW, pady=8)

        seats_entry.insert(0, str(total_seats))

        # ==========================================
        # PRICE
        # ==========================================

        ttk.Label(form, text="Ticket Price *").grid(row=10, column=0, sticky=W, pady=8)

        price_entry = ttk.Entry(form, width=40)

        price_entry.grid(row=10, column=1, sticky=EW, pady=8)

        price_entry.insert(0, str(price))

        # ==========================================
        # STATUS
        # ==========================================

        ttk.Label(form, text="Flight Status").grid(row=11, column=0, sticky=W, pady=8)

        status_combo = ttk.Combobox(
            form,
            values=[
                "Scheduled",
                "Boarding",
                "Departed",
                "Completed",
                "Delayed",
                "Cancelled",
            ],
            state="readonly",
            width=37,
        )

        status_combo.grid(row=11, column=1, sticky=EW, pady=8)

        status_combo.set(status)

        # ==========================================
        # BUTTON FRAME
        # ==========================================

        button_frame = ttk.Frame(form)

        button_frame.grid(row=12, column=0, columnspan=2, pady=25)

        # ==========================================
        # UPDATE FUNCTION
        # ==========================================

        def update_flight():

            flight_no = flight_no_entry.get().strip()

            airline_value = airline_combo.get().strip()

            departure_value = departure_entry.get().strip()

            arrival_value = arrival_entry.get().strip()

            date_value = date_entry.get().strip()

            departure_time_value = departure_time_entry.get().strip()

            arrival_time_value = arrival_time_entry.get().strip()

            aircraft_value = aircraft_combo.get().strip()

            seats_value = seats_entry.get().strip()

            price_value = price_entry.get().strip()

            status_value = status_combo.get().strip()

            # ======================================
            # REQUIRED VALIDATION
            # ======================================

            fields = [
                (flight_no, flight_no_entry, "Flight Number"),
                (airline_value, airline_combo, "Airline"),
                (departure_value, departure_entry, "Departure"),
                (arrival_value, arrival_entry, "Arrival"),
                (date_value, date_entry, "Departure Date"),
                (departure_time_value, departure_time_entry, "Departure Time"),
                (arrival_time_value, arrival_time_entry, "Arrival Time"),
                (aircraft_value, aircraft_combo, "Aircraft"),
            ]

            for value, widget, name in fields:

                if not value:

                    messagebox.showwarning(
                        "Validation", f"Please enter/select {name}.", parent=window
                    )

                    widget.focus()

                    return

            # ======================================
            # SEATS
            # ======================================

            try:

                seats = int(seats_value)

                if seats <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation",
                    "Total Seats must be a positive number.",
                    parent=window,
                )

                seats_entry.focus()

                return

            # ======================================
            # PRICE
            # ======================================

            try:

                price_number = float(price_value)

                if price_number <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation",
                    "Ticket Price must be a positive number.",
                    parent=window,
                )

                price_entry.focus()

                return

            # ======================================
            # DATE
            # ======================================

            import datetime

            try:

                datetime.datetime.strptime(date_value, "%Y-%m-%d")

            except ValueError:

                messagebox.showwarning(
                    "Validation", "Invalid date.\nUse YYYY-MM-DD.", parent=window
                )

                date_entry.focus()

                return

            # ======================================
            # CONFIRM
            # ======================================

            confirm = messagebox.askyesno(
                "Update Flight",
                f"Update flight {flight_no}?\n\n"
                f"{departure_value} → {arrival_value}\n"
                f"Date: {date_value}\n"
                f"Seats: {seats}\n"
                f"Price: ৳ {price_number:,.2f}",
                parent=window,
            )

            if not confirm:
                return

            # ======================================
            # DATABASE UPDATE
            # ======================================

            try:

                result = self.db.update_flight(
                    flight_id=flight_id,
                    flight_number=flight_no,
                    airline=airline_value,
                    departure=departure_value,
                    arrival=arrival_value,
                    departure_date=date_value,
                    departure_time=departure_time_value,
                    arrival_time=arrival_time_value,
                    aircraft=aircraft_value,
                    total_seats=seats,
                    price=price_number,
                    status=status_value,
                )

                if result:

                    messagebox.showinfo(
                        "Success",
                        f"Flight {flight_no} updated successfully!",
                        parent=window,
                    )

                    window.destroy()

                    self.load_flights()

                else:

                    messagebox.showerror(
                        "Error",
                        "Flight number already exists or update failed.",
                        parent=window,
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error", f"Unable to update flight.\n\n{e}", parent=window
                )

        # ==========================================
        # CANCEL
        # ==========================================

        ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            width=15,
            command=window.destroy,
        ).pack(side=LEFT, padx=8)

        # ==========================================
        # UPDATE BUTTON
        # ==========================================

        ttk.Button(
            button_frame,
            text="✓ Update Flight",
            bootstyle="warning",
            width=20,
            command=update_flight,
        ).pack(side=LEFT, padx=8)

        flight_no_entry.focus()

    def delete_flight(self):

        # ==========================================
        # CHECK SELECTION
        # ==========================================

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection", "Please select a flight to delete.", parent=self.root
            )

            return

        # ==========================================
        # GET SELECTED DATA
        # ==========================================

        item = self.table.item(selected[0])

        values = item["values"]

        flight_id = values[0]
        flight_number = values[1]
        airline = values[2]
        departure = values[3]
        arrival = values[4]
        flight_date = values[5]

        # ==========================================
        # CONFIRM DELETE
        # ==========================================

        confirm = messagebox.askyesno(
            "Delete Flight",
            f"Are you sure you want to delete this flight?\n\n"
            f"Flight: {flight_number}\n"
            f"Airline: {airline}\n"
            f"Route: {departure} → {arrival}\n"
            f"Date: {flight_date}\n\n"
            f"This action cannot be undone.",
            parent=self.root,
        )

        if not confirm:
            return

        # ==========================================
        # DELETE FROM DATABASE
        # ==========================================

        try:

            result = self.db.delete_flight(flight_id)

            if result:

                messagebox.showinfo(
                    "Success",
                    f"Flight {flight_number} deleted successfully.",
                    parent=self.root,
                )

                # Refresh table
                self.load_flights()

                self.status_label.config(text=f"Flight {flight_number} deleted")

            else:

                messagebox.showerror(
                    "Delete Error", "Flight could not be deleted.", parent=self.root
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error", f"Unable to delete flight.\n\n{e}", parent=self.root
            )

        try:

            selected_status = self.status_filter.get().strip()

            # ======================================
            # ALL STATUS
            # ======================================

            if selected_status == "All Status":

                self.load_flights()

                return

            # ======================================
            # CLEAR TABLE
            # ======================================

            for item in self.table.get_children():

                self.table.delete(item)

            # ======================================
            # GET ALL FLIGHTS
            # ======================================

            flights = self.db.get_all_flights()

            filtered_flights = []

            # ======================================
            # FILTER
            # ======================================

            for flight in flights:

                status = str(flight[12]).strip()

                if status.lower() == selected_status.lower():
                    filtered_flights.append(flight)

            # ======================================
            # INSERT RESULTS
            # ======================================

            for flight in filtered_flights:

                (
                    flight_id,
                    flight_number,
                    airline,
                    departure,
                    arrival,
                    departure_date,
                    departure_time,
                    arrival_time,
                    aircraft,
                    total_seats,
                    available_seats,
                    price,
                    status,
                ) = flight

                self.table.insert(
                    "",
                    END,
                    values=(
                        flight_id,
                        flight_number,
                        airline,
                        departure,
                        arrival,
                        departure_date,
                        aircraft,
                        total_seats,
                        available_seats,
                        f"৳ {price:,.2f}",
                        status,
                    ),
                )

            # ======================================
            # STATUS BAR
            # ======================================

            self.status_label.config(
                text=f"{len(filtered_flights)} {selected_status} flight(s) found"
            )

        except Exception as e:

            print("Status Filter Error:", e)

    # ==========================================
    # SEARCH + STATUS FILTER
    # ==========================================

    def search_flights(self):

        try:

            keyword = self.search_entry.get().strip().lower()
            selected_status = self.status_filter.get().strip()

            # Clear table
            for item in self.table.get_children():
                self.table.delete(item)

            # Get all flights
            flights = self.db.get_all_flights()

            filtered_flights = []

            for flight in flights:

                flight_number = str(flight[1]).lower()
                airline = str(flight[2]).lower()
                departure = str(flight[3]).lower()
                arrival = str(flight[4]).lower()
                status = str(flight[12]).strip()

                # -------------------------------
                # Keyword Search
                # -------------------------------

                keyword_match = (
                    not keyword
                    or keyword in flight_number
                    or keyword in airline
                    or keyword in departure
                    or keyword in arrival
                )

                # -------------------------------
                # Status Filter
                # -------------------------------

                status_match = (
                    selected_status == "Status"
                    or status.lower() == selected_status.lower()
                )

                # -------------------------------
                # Final Filter
                # -------------------------------

                if keyword_match and status_match:

                    filtered_flights.append(flight)

            # -------------------------------
            # Display Results
            # -------------------------------

            for flight in filtered_flights:

                (
                    flight_id,
                    flight_number,
                    airline,
                    departure,
                    arrival,
                    departure_date,
                    departure_time,
                    arrival_time,
                    aircraft,
                    total_seats,
                    available_seats,
                    price,
                    status,
                ) = flight

                self.table.insert(
                    "",
                    END,
                    values=(
                        flight_id,
                        flight_number,
                        airline,
                        departure,
                        arrival,
                        departure_date,
                        aircraft,
                        total_seats,
                        available_seats,
                        f"৳ {price:,.2f}",
                        status,
                    ),
                )

            # -------------------------------
            # Status Bar
            # -------------------------------

            self.status_label.config(text=f"{len(filtered_flights)} flight(s) found")

        except Exception as e:

            print("Search Flights Error:", e)

    # ==========================================
    # CLEAR SEARCH
    # ==========================================

    def clear_search(self):

        self.search_entry.delete(0, END)

        self.status_filter.set("All")

        self.load_flights()

    # =========================================================
    # DISPLAY FLIGHTS
    # =========================================================

    def display_flights(self, flights):

        # Clear table

        for item in self.table.get_children():

            self.table.delete(item)

        # Insert

        for flight in flights:

            (
                flight_id,
                flight_number,
                airline,
                departure,
                arrival,
                departure_date,
                departure_time,
                arrival_time,
                aircraft,
                total_seats,
                available_seats,
                price,
                status,
            ) = flight

            self.table.insert(
                "",
                END,
                values=(
                    flight_id,
                    flight_number,
                    airline,
                    departure,
                    arrival,
                    departure_date,
                    aircraft,
                    total_seats,
                    available_seats,
                    f"৳ {price:,.2f}",
                    status,
                ),
            )

        self.update_statistics()

    def clear_search(self):

        self.search_entry.delete(0, END)

        self.status_filter.set("All")

        self.load_flights()
