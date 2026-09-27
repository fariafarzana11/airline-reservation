import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime

from database.database import Database
from gui.passenger import PassengerWindow
from gui.flight import FlightWindow
from gui.booking import BookingWindow


class DashboardWindow:

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

        # self.create_sidebar()
        # self.create_content()

        self.create_sidebar()

        self.content_frame = ttk.Frame(self.main, padding=25)

        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # self.content_frame = ttk.Frame(self.main)
        # self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.show_dashboard()

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

    # def show_dashboard(self):

    #     self.main.destroy()

    #     try:
    #         self.status_bar.destroy()
    #     except:
    #         pass

    #     from gui.dashboard import DashboardWindow

    #     DashboardWindow(self.root)

    def show_dashboard(self):

        # Clear current content
        self.clear_content()

        # ==========================================
        # DASHBOARD HEADER
        # ==========================================

        header = ttk.Frame(self.content_frame, padding=(25, 20))

        header.pack(fill=X)

        ttk.Label(header, text="Dashboard", font=("Segoe UI", 24, "bold")).pack(
            side=LEFT
        )

        ttk.Label(
            header, text="SkyLink Pro Airline Management System", font=("Segoe UI", 10)
        ).pack(side=LEFT, padx=20)

        # ==========================================
        # WELCOME
        # ==========================================

        welcome = ttk.Label(
            self.content_frame,
            text="Welcome to SkyLink Pro",
            font=("Segoe UI", 20, "bold"),
        )

        welcome.pack(anchor=W, padx=25, pady=(20, 10))

        # ==========================================
        # INFO
        # ==========================================

        info = ttk.Label(
            self.content_frame,
            text="Manage passengers, flights, bookings and payments from the sidebar.",
            font=("Segoe UI", 11),
        )

        info.pack(anchor=W, padx=25)

    def open_passenger(self):

        # Already on Passenger page
        # pass

        self.clear_content()

        PassengerWindow(self.content_frame)

    def open_flight(self):

        self.clear_content()

        FlightWindow(self.content_frame)

    def open_booking(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        BookingWindow(self.content_frame)

    def open_payment(self):

        PaymentWindow(self.content_frame)

    def open_reports(self):

        messagebox.showinfo("Reports", "Reports module is coming soon.")

    def open_settings(self):

        messagebox.showinfo("Settings", "Settings module is coming soon.")

    def logout(self):

        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")

        if not confirm:
            return

        # Dashboard- main UI remove
        if hasattr(self, "main"):
            self.main.destroy()

        # Login screen
        from gui.login import LoginWindow

        LoginWindow(self.root)

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ==========================================
    # CONTENT
    # ==========================================

    def create_content(self):

        self.content = ttk.Frame(self.main)

        self.content.pack(side=RIGHT, fill=BOTH, expand=True)

        self.create_topbar()

        self.content_frame = ttk.Frame(self.content)

        self.content_frame.pack(fill=BOTH, expand=True, padx=25, pady=25)

        self.show_dashboard()

    # ==========================================
    # TOPBAR
    # ==========================================

    def create_topbar(self):

        self.topbar = ttk.Frame(self.content, padding=15, bootstyle="light")

        self.topbar.pack(fill=X)

        ttk.Label(self.topbar, text="Dashboard", font=("Segoe UI", 22, "bold")).pack(
            side=LEFT
        )

        self.clock = ttk.Label(self.topbar, font=("Segoe UI", 10))

        self.clock.pack(side=RIGHT, padx=15)

        ttk.Button(self.topbar, text="🔔", width=3, bootstyle="secondary").pack(
            side=RIGHT, padx=5
        )

        ttk.Label(self.topbar, text="Admin", font=("Segoe UI", 11, "bold")).pack(
            side=RIGHT, padx=10
        )

        self.update_clock()

    # ==========================================
    # Update CLOCK
    # ==========================================

    def update_clock(self):

        try:

            if not self.clock.winfo_exists():
                return

            now = datetime.now().strftime("%d-%m-%Y  %I:%M:%S %p")

            self.clock.config(text=now)

            self.clock_job = self.root.after(1000, self.update_clock)

        except Exception:
            return

    # ==========================================
    # DASHBOARD
    # ==========================================

    def show_dashboard(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ttk.Label(
            self.content_frame,
            text="Welcome to SkyLink Pro",
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor=W, pady=(0, 20))

        cards = ttk.Frame(self.content_frame)

        cards.pack(fill=X)

        cards.grid_columnconfigure(0, weight=1)

        cards.grid_columnconfigure(1, weight=1)

        cards.grid_columnconfigure(2, weight=1)

        cards.grid_columnconfigure(3, weight=1)

        try:

            flights = self.db.get_total_flights()
            passengers = self.db.get_total_passengers()
            bookings = self.db.get_total_bookings()
            revenue = self.db.get_total_revenue()

        except Exception:

            flights = 0
            passengers = 0
            bookings = 0
            revenue = 0

        self.create_card(cards, "✈", "Total Flights", flights, 0)

        self.create_card(cards, "👤", "Passengers", passengers, 1)

        self.create_card(cards, "🎫", "Bookings", bookings, 2)

        self.create_card(cards, "💰", "Revenue", f"৳ {revenue:,.2f}", 3)

        ttk.Label(
            self.content_frame, text="System Overview", font=("Segoe UI", 18, "bold")
        ).pack(anchor=W, pady=(35, 10))

        ttk.Label(
            self.content_frame,
            text="SkyLink Pro Airline Reservation & Management System",
            font=("Segoe UI", 11),
        ).pack(anchor=W)

    # ==========================================
    # CARD
    # ==========================================

    def create_card(self, parent, icon, title, value, column):

        card = ttk.Frame(parent, padding=20, bootstyle="light")

        card.grid(row=0, column=column, padx=8, sticky="nsew")

        ttk.Label(card, text=icon, font=("Segoe UI Emoji", 28)).pack()

        ttk.Label(card, text=str(value), font=("Segoe UI", 22, "bold")).pack(pady=5)

        ttk.Label(card, text=title, font=("Segoe UI", 10)).pack()

    # ==========================================
    # DASHBOARD STATISTICS
    # ==========================================

    def get_statistics(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            # Total flights
            cursor.execute("""
                SELECT COUNT(*)
                FROM flights
            """)

            total_flights = cursor.fetchone()[0]

            # Scheduled flights
            cursor.execute("""
                SELECT COUNT(*)
                FROM flights
                WHERE status = 'Scheduled'
            """)

            scheduled_flights = cursor.fetchone()[0]

            # Total seats
            cursor.execute("""
                SELECT COALESCE(
                    SUM(total_seats), 0
                )
                FROM flights
            """)

            total_seats = cursor.fetchone()[0]

            # Available seats
            cursor.execute("""
                SELECT COALESCE(
                    SUM(available_seats), 0
                )
                FROM flights
            """)

            available_seats = cursor.fetchone()[0]

            return {
                "total_flights": total_flights,
                "scheduled_flights": scheduled_flights,
                "total_seats": total_seats,
                "available_seats": available_seats,
            }

        except Exception as e:

            print("Statistics Error:", e)

            return {
                "total_flights": 0,
                "scheduled_flights": 0,
                "total_seats": 0,
                "available_seats": 0,
            }

        finally:

            conn.close()

    def load_statistics(self):

        try:

            stats = self.db.get_statistics()

            total_flights = stats["total_flights"]

            scheduled_flights = stats["scheduled_flights"]

            total_seats = stats["total_seats"]

            available_seats = stats["available_seats"]

            # Update dashboard cards
            self.total_flights_value.config(text=str(total_flights))

            self.scheduled_flights_value.config(text=str(scheduled_flights))

            self.total_seats_value.config(text=str(total_seats))

            self.available_seats_value.config(text=str(available_seats))

        except Exception as e:

            print("Statistics Error:", e)
