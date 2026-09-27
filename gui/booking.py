import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime

from database.database import Database


class BookingWindow:

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

        self.load_bookings()

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        header = ttk.Frame(self.main, padding=(25, 20), bootstyle="primary")

        header.pack(fill=X)

        ttk.Label(
            header,
            text="Booking Management",
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-primary",
        ).pack(side=LEFT)

        ttk.Label(
            header,
            text="Manage passenger flight bookings",
            font=("Segoe UI", 10),
            bootstyle="inverse-primary",
        ).pack(side=LEFT, padx=20)

    # ==========================================
    # TOOLBAR
    # ==========================================

    def create_toolbar(self):

        toolbar = ttk.Frame(self.main, padding=(25, 15))

        toolbar.pack(fill=X)

        ttk.Button(
            toolbar, text="+ New Booking", bootstyle="success", command=self.add_booking
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            toolbar,
            text="✕ Cancel Booking",
            bootstyle="danger",
            command=self.cancel_booking,
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            toolbar, text="⟳ Refresh", bootstyle="info", command=self.load_bookings
        ).pack(side=LEFT, padx=5)

        self.search_entry = ttk.Entry(toolbar, width=35)

        self.search_entry.pack(side=RIGHT, padx=5)

        ttk.Button(
            toolbar, text="🔍 Search", bootstyle="primary", command=self.search_bookings
        ).pack(side=RIGHT, padx=5)

        self.search_entry.bind("<Return>", lambda event: self.search_bookings())

    # ==========================================
    # STATISTICS
    # ==========================================

    def create_statistics(self):

        stats = ttk.Frame(self.main, padding=(25, 5))

        stats.pack(fill=X)

        self.total_card = self.create_stat_card(stats, "Total Bookings", "0", "primary")

        self.total_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.confirmed_card = self.create_stat_card(stats, "Confirmed", "0", "success")

        self.confirmed_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.pending_card = self.create_stat_card(stats, "Pending", "0", "warning")

        self.pending_card.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.cancelled_card = self.create_stat_card(stats, "Cancelled", "0", "danger")

        self.cancelled_card.pack(side=LEFT, fill=X, expand=True, padx=5)

    def create_stat_card(self, parent, title, value, style):

        card = ttk.Labelframe(parent, text=f" {title} ", padding=15, bootstyle=style)

        label = ttk.Label(
            card, text=value, font=("Segoe UI", 22, "bold"), bootstyle=style
        )

        label.pack()

        return card

    # ==========================================
    # TABLE
    # ==========================================

    def create_table(self):

        table_frame = ttk.Frame(self.main, padding=(25, 10, 25, 20))

        table_frame.pack(fill=BOTH, expand=True)

        columns = ("id", "passenger", "flight", "seat", "date", "amount", "status")

        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        headings = {
            "id": "Booking ID",
            "passenger": "Passenger",
            "flight": "Flight",
            "seat": "Seat",
            "date": "Booking Date",
            "amount": "Amount",
            "status": "Status",
        }

        for column, title in headings.items():

            self.table.heading(column, text=title)

        self.table.column("id", width=100, anchor=CENTER)

        self.table.column("passenger", width=220)

        self.table.column("flight", width=130, anchor=CENTER)

        self.table.column("seat", width=100, anchor=CENTER)

        self.table.column("date", width=130, anchor=CENTER)

        self.table.column("amount", width=130, anchor=CENTER)

        self.table.column("status", width=120, anchor=CENTER)

        y_scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.table.yview)

        self.table.configure(yscrollcommand=y_scroll.set)

        self.table.grid(row=0, column=0, sticky=NSEW)

        y_scroll.grid(row=0, column=1, sticky=NS)

        table_frame.rowconfigure(0, weight=1)

        table_frame.columnconfigure(0, weight=1)

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
            text="SkyLink Pro • Booking Management",
            bootstyle="inverse-secondary",
        ).pack(side=RIGHT)

    # ==========================================
    # ADD BOOKING
    # ==========================================

    def add_booking(self):

        window = ttk.Toplevel(self.root)

        window.title("New Booking")

        window.geometry("650x650")

        window.resizable(False, False)

        window.transient(self.root)

        window.grab_set()

        # ======================================
        # CENTER
        # ======================================

        window.update_idletasks()

        width = 650
        height = 650

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
            text="✈  New Flight Booking",
            font=("Segoe UI", 22, "bold"),
            bootstyle="inverse-primary",
        ).pack()

        ttk.Label(
            header, text="Create a new passenger booking", bootstyle="inverse-primary"
        ).pack(pady=(5, 0))

        # ======================================
        # FORM
        # ======================================

        form = ttk.Frame(window, padding=30)

        form.pack(fill=BOTH, expand=True)

        form.columnconfigure(1, weight=1)

        # ======================================
        # PASSENGER
        # ======================================

        ttk.Label(form, text="Passenger *").grid(row=0, column=0, sticky=W, pady=10)

        passengers = self.db.get_passengers()

        passenger_map = {}

        passenger_values = []

        for passenger in passengers:

            passenger_id = passenger[0]
            passenger_name = passenger[1]

            display = f"{passenger_id} - {passenger_name}"

            passenger_map[display] = passenger_id

            passenger_values.append(display)

        passenger_combo = ttk.Combobox(
            form, values=passenger_values, state="readonly", width=40
        )

        passenger_combo.grid(row=0, column=1, sticky=EW, pady=10)

        # ======================================
        # FLIGHT
        # ======================================

        ttk.Label(form, text="Flight *").grid(row=1, column=0, sticky=W, pady=10)

        flights = self.db.get_all_flights()

        flight_map = {}

        flight_values = []

        for flight in flights:

            flight_id = flight[0]
            flight_number = flight[1]
            airline = flight[2]
            departure = flight[3]
            arrival = flight[4]
            available = flight[10]
            price = flight[11]
            status = flight[12]

            if available > 0 and status not in ("Cancelled", "Completed", "Departed"):

                display = (
                    f"{flight_number} | "
                    f"{departure} → {arrival} | "
                    f"৳ {price:,.2f}"
                )

                flight_map[display] = flight

                flight_values.append(display)

        flight_combo = ttk.Combobox(
            form, values=flight_values, state="readonly", width=40
        )

        flight_combo.grid(row=1, column=1, sticky=EW, pady=10)

        ttk.Label(form, text="Flight *").grid(row=1, column=0, sticky=W, pady=10)

        flight_combo = ttk.Combobox(form, state="readonly", width=40)

        flight_combo.grid(row=1, column=1, sticky=EW, pady=10)

        flight_map = {}

        flights = self.db.get_all_flights()

        for flight in flights:

            flight_id = flight[0]
            flight_number = flight[1]
            departure = flight[3]
            arrival = flight[4]
            available = flight[10]
            price = flight[11]
            status = flight[12]

            if available > 0 and status not in ("Cancelled", "Completed", "Departed"):

                display = (
                    f"{flight_number} | "
                    f"{departure} → {arrival} | "
                    f"{available} seats"
                )

                flight_map[display] = flight

        flight_combo["values"] = list(flight_map.keys())

        # ======================================
        # SEAT
        # ======================================

        # ttk.Label(form, text="Seat Number *").grid(row=2, column=0, sticky=W, pady=10)

        # seat_entry = ttk.Entry(form, state="readonly", width=40)

        # seat_entry.grid(row=2, column=1, sticky=EW, pady=10)
        # ==========================================
        # SEAT MAP
        # ==========================================

        ttk.Label(form, text="Select Seat", font=("Segoe UI", 11, "bold")).grid(
            row=2, column=0, sticky=NW, pady=10
        )

        seat_frame = ttk.Frame(form)

        seat_frame.grid(row=2, column=1, sticky=W, pady=10)

        selected_seat = ttk.StringVar()

        seat_buttons = {}

        ttk.Label(
            form, text="Example: 12A", font=("Segoe UI", 8), bootstyle="secondary"
        ).grid(row=3, column=1, sticky=W)

        # ======================================
        # BOOKING DATE
        # ======================================

        ttk.Label(form, text="Booking Date").grid(row=4, column=0, sticky=W, pady=10)

        date_entry = ttk.Entry(form, width=40)

        date_entry.grid(row=4, column=1, sticky=EW, pady=10)

        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # ======================================
        # AMOUNT
        # ======================================

        ttk.Label(form, text="Total Amount").grid(row=5, column=0, sticky=W, pady=10)

        amount_entry = ttk.Entry(form, width=40)

        amount_entry.grid(row=5, column=1, sticky=EW, pady=10)

        # ======================================
        # UPDATE PRICE
        # ======================================

        def update_price(event=None):

            selected = flight_combo.get()

            if selected in flight_map:

                flight = flight_map[selected]

                price = flight[11]

                amount_entry.delete(0, END)

                amount_entry.insert(0, str(price))

        flight_combo.bind("<<ComboboxSelected>>", update_price)

        # ======================================
        # STATUS
        # ======================================

        ttk.Label(form, text="Status").grid(row=6, column=0, sticky=W, pady=10)

        status_combo = ttk.Combobox(
            form,
            values=["Confirmed", "Pending", "Cancelled"],
            state="readonly",
            width=40,
        )

        status_combo.grid(row=6, column=1, sticky=EW, pady=10)

        status_combo.set("Confirmed")

        # ======================================
        # SAVE
        # ======================================

        def save_booking():

            passenger_display = passenger_combo.get().strip()

            flight_display = flight_combo.get().strip()

            seat_no = seat_entry.get().strip()

            booking_date = date_entry.get().strip()

            amount = amount_entry.get().strip()

            status = status_combo.get().strip()

            seat = selected_seat.get().strip()

            # -------------------------------
            # VALIDATION
            # -------------------------------

            if not passenger_display:

                messagebox.showwarning(
                    "Validation", "Please select a passenger.", parent=window
                )

                passenger_combo.focus()

                return

            if not flight_display:

                messagebox.showwarning(
                    "Validation", "Please select a flight.", parent=window
                )

                flight_combo.focus()

                return

            if not seat_no:

                messagebox.showwarning(
                    "Validation", "Please enter Seat Number.", parent=window
                )

                seat_entry.focus()

                return

            if not booking_date:

                messagebox.showwarning(
                    "Validation", "Please enter Booking Date.", parent=window
                )

                date_entry.focus()

                return

            if not seat:

                messagebox.showwarning(
                    "Validation", "Please select a seat.", parent=window
                )

                return

            try:

                datetime.strptime(booking_date, "%Y-%m-%d")

            except ValueError:

                messagebox.showwarning(
                    "Validation", "Invalid date. Use YYYY-MM-DD.", parent=window
                )

                date_entry.focus()

                return

            try:

                amount_value = float(amount)

                if amount_value <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validation", "Amount must be a positive number.", parent=window
                )

                amount_entry.focus()

                return

            # -------------------------------
            # IDs
            # -------------------------------

            passenger_id = passenger_map[passenger_display]

            flight = flight_map[flight_display]

            flight_id = flight[0]

            # -------------------------------
            # CONFIRM
            # -------------------------------

            confirm = messagebox.askyesno(
                "Confirm Booking",
                f"Create booking?\n\n"
                f"Passenger: {passenger_display}\n"
                f"Flight: {flight_display}\n"
                f"Seat: {seat_no}\n"
                f"Amount: ৳ {amount_value:,.2f}",
                parent=window,
            )

            if not confirm:
                return

            # -------------------------------
            # DATABASE
            # -------------------------------

            try:

                result = self.db.add_booking(
                    passenger_id=passenger_id,
                    flight_id=flight_id,
                    seat_no=seat_no,
                    booking_date=booking_date,
                    total_amount=amount_value,
                    status=status,
                )

                if result:

                    messagebox.showinfo(
                        "Success", "Booking created successfully!", parent=window
                    )

                    window.destroy()

                    self.load_bookings()

                else:

                    messagebox.showerror(
                        "Booking Failed",
                        "This seat is already booked or unavailable.",
                        parent=window,
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error", f"Unable to create booking.\n\n{e}", parent=window
                )

        # ======================================
        # BUTTONS
        # ======================================

        button_frame = ttk.Frame(form)

        button_frame.grid(row=7, column=0, columnspan=2, pady=25)

        ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            width=15,
            command=window.destroy,
        ).pack(side=LEFT, padx=8)

        ttk.Button(
            button_frame,
            text="✓ Confirm Booking",
            bootstyle="success",
            width=20,
            command=save_booking,
        ).pack(side=LEFT, padx=8)

        passenger_combo.focus()

        # ===========================
        # Update seats
        # ============================
        def update_seats(event=None):

            selected = flight_combo.get()

            if not selected:
                return

            flight = flight_map.get(selected)

            if not flight:
                return

            flight_id = flight[0]

            total_seats = flight[9]

            booked_seats = self.db.get_booked_seats(flight_id)

            seat_list = []

            for seat_number in range(1, total_seats + 1):

                seat = str(seat_number)

                if seat not in booked_seats:

                    seat_list.append(seat)

            seat_combo["values"] = seat_list

            if seat_list:

                seat_combo.current(0)

            else:

                seat_combo.set("No seats available")

            # old seat buttons remove

            for widget in seat_frame.winfo_children():
                widget.destroy()

            seat_buttons.clear()

            selected = flight_combo.get()

            if not selected:
                return

            flight = flight_map.get(selected)

            if not flight:
                return

            flight_id = flight[0]

            total_seats = flight[9]

            booked_seats = self.db.get_booked_seats(flight_id)

            # 4-column aircraft
            columns = ["A", "B", "C", "D"]

            for seat_number in range(1, total_seats + 1):

                row = (seat_number - 1) // 4
                column = (seat_number - 1) % 4

                seat_no = f"{seat_number}{columns[column]}"

                if seat_no in booked_seats:

                    button = ttk.Button(
                        seat_frame,
                        text=seat_no,
                        width=6,
                        bootstyle="danger",
                        state="disabled",
                    )

                else:

                    button = ttk.Button(
                        seat_frame,
                        text=seat_no,
                        width=6,
                        bootstyle="success-outline",
                        command=lambda s=seat_no: select_seat(s),
                    )

                button.grid(row=row, column=column, padx=4, pady=4)

                seat_buttons[seat_no] = button

        flight_combo.bind("<<ComboboxSelected>>", update_seats)

        def select_seat(seat_no):

            selected_seat.set(seat_no)

            # সব available seat reset
            for seat, button in seat_buttons.items():

                if button["state"] != "disabled":

                    button.configure(bootstyle="success-outline")

            # Selected seat
            if seat_no in seat_buttons:

                seat_buttons[seat_no].configure(bootstyle="primary")

        flight_combo.bind("<<ComboboxSelected>>", update_seats)

    # ==========================================
    # LOAD BOOKINGS
    # ==========================================

    def load_bookings(self):

        for item in self.table.get_children():

            self.table.delete(item)

        bookings = self.db.get_all_bookings()

        for booking in bookings:

            booking_id, passenger, flight, seat, booking_date, amount, status = booking

            self.table.insert(
                "",
                END,
                values=(
                    booking_id,
                    passenger,
                    flight,
                    seat,
                    booking_date,
                    f"৳ {amount:,.2f}",
                    status,
                ),
            )

        self.update_statistics()

        self.status_label.config(text=f"{len(bookings)} booking(s) loaded")

    # ==========================================
    # STATISTICS
    # ==========================================

    def update_statistics(self):

        bookings = self.db.get_all_bookings()

        total = len(bookings)
        confirmed = 0
        pending = 0
        cancelled = 0

        for booking in bookings:

            status = str(booking[6]).strip().title()

            if status == "Confirmed":

                confirmed += 1

            elif status == "Pending":

                pending += 1

            elif status == "Cancelled":

                cancelled += 1

        self.update_stat_card(self.total_card, total)

        self.update_stat_card(self.confirmed_card, confirmed)

        self.update_stat_card(self.pending_card, pending)

        self.update_stat_card(self.cancelled_card, cancelled)

    def update_stat_card(self, card, value):

        for widget in card.winfo_children():

            if isinstance(widget, ttk.Label):

                widget.config(text=str(value))

    # ==========================================
    # CANCEL BOOKING
    # ==========================================

    def cancel_booking(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning("Selection", "Please select a booking first.")

            return

        values = self.table.item(selected[0], "values")

        booking_id = values[0]

        messagebox.showinfo(
            "Cancel Booking",
            f"Booking #{booking_id} cancellation "
            f"will be implemented in the next step.",
        )

    # ==========================================
    # SEARCH
    # ==========================================

    def search_bookings(self):

        keyword = self.search_entry.get().strip().lower()

        if not keyword:

            self.load_bookings()

            return

        for item in self.table.get_children():

            self.table.delete(item)

        bookings = self.db.get_all_bookings()

        count = 0

        for booking in bookings:

            booking_id, passenger, flight, seat, booking_date, amount, status = booking

            searchable = (
                f"{booking_id} "
                f"{passenger} "
                f"{flight} "
                f"{seat} "
                f"{booking_date} "
                f"{status}"
            ).lower()

            if keyword in searchable:

                self.table.insert(
                    "",
                    END,
                    values=(
                        booking_id,
                        passenger,
                        flight,
                        seat,
                        booking_date,
                        f"৳ {amount:,.2f}",
                        status,
                    ),
                )

                count += 1

        self.status_label.config(text=f"{count} booking(s) found")
