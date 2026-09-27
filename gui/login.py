import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk, ImageFilter

from config import *
from database.database import Database
from gui.dashboard import DashboardWindow


class LoginWindow:

    def __init__(self, root):

        self.root = root
        self.db = Database()

        self.setup_window()

        self.load_images()

        self.build_ui()

    def setup_window(self):

        self.root.title(APP_NAME)

        width = WINDOW_WIDTH

        height = WINDOW_HEIGHT

        sw = self.root.winfo_screenwidth()

        sh = self.root.winfo_screenheight()

        x = (sw - width) // 2
        y = (sh - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.resizable(False, False)

    def load_images(self):

        base = os.path.dirname(os.path.dirname(__file__))

        bg_path = os.path.join(base, "assets", "background.jpg")

        logo_path = os.path.join(base, "assets", "logo.jpg")

        self.bg_image = None
        self.logo = None

        if os.path.exists(bg_path):

            img = Image.open(bg_path)

            img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)

            # Blur Effect
            img = img.filter(ImageFilter.GaussianBlur(radius=3))

            self.bg_image = ImageTk.PhotoImage(img)

        if os.path.exists(logo_path):

            img = Image.open(logo_path)

            img = img.resize((50, 50))

            self.logo = ImageTk.PhotoImage(img)

    def build_ui(self):

        self.canvas = Canvas(
            self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        if self.bg_image:

            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

            self.create_left_panel()

            self.create_login_card()

    def create_left_panel(self):

        # Left Panel
        self.left = ttk.Frame(self.root, bootstyle="dark")

        self.left.place(x=0, y=0, width=420, height=WINDOW_HEIGHT)

        # Logo
        if self.logo:

            ttk.Label(self.left, image=self.logo).place(x=10, y=20)

        # Project Name
        ttk.Label(
            self.left,
            text="SkyLink Pro",
            font=("Segoe UI", 28, "bold"),
            bootstyle="inverse-dark",
        ).pack(pady=(40, 0))

        ttk.Label(
            self.left,
            text="Smart Airline Reservation System",
            font=("Segoe UI", 12),
            bootstyle="inverse-dark",
        ).pack(pady=(0, 20))

        ttk.Separator(self.left).pack(fill=X, padx=30, pady=20)

        # ✈ Flight Booking

        # 👤 Passenger Management

        # 💳 Payment System

        # 📄 PDF Ticket

        # 📊 Reports & Analytics

        # 🔒 Secure Login

        info = """
        
        🏠 Dashboard
        
        👤 Passenger
        
        🛫 Flight
        
        🎫 Booking
        
        💳 Payment
        
        📊 Reports
        
        ⚙️ Settings
        """

        ttk.Label(
            self.left,
            text=info,
            justify=LEFT,
            font=("Segoe UI", 13),
            bootstyle="inverse-dark",
        ).pack(padx=30, anchor="w")

    def create_login_card(self):

        # Login Card
        self.card = ttk.Labelframe(self.root, text=" ", bootstyle=" ", padding=40)

        self.card.place(relx=0.6, rely=0.50, anchor=CENTER, width=450, height=470)

        ttk.Label(self.card, text="Welcome Back", font=("Segoe UI", 22, "bold")).pack(
            pady=(10, 5)
        )

        ttk.Label(
            self.card, text="Please login to continue", font=("Segoe UI", 10)
        ).pack(pady=(0, 20))

        # Username
        ttk.Label(self.card, text="Username").pack(anchor=W)

        self.username = ttk.Entry(self.card, width=38)

        self.username.pack(pady=(15, 15))

        # Password
        ttk.Label(self.card, text="Password").pack(anchor=W)

        pass_frame = ttk.Frame(self.card)
        pass_frame.pack()

        self.password = ttk.Entry(pass_frame, width=30, show="*")

        self.password.pack(side=LEFT, padx=(0, 5))

        self.show_password = False

        self.eye_btn = ttk.Button(
            pass_frame, text="👁", width=3, command=self.toggle_password
        )

        self.eye_btn.pack(side=LEFT)

        # Remember Me
        self.remember = ttk.BooleanVar()

        ttk.Checkbutton(self.card, text="Remember Me", variable=self.remember).pack(
            anchor=W, pady=15
        )

        # ==========================
        # Error Label
        # ==========================

        self.error_label = ttk.Label(
            self.card, text="", foreground="red", font=("Segoe UI", 10)
        )

        self.error_label.pack(pady=(8, 0))

        # Login Button
        ttk.Button(
            self.card,
            text="🔐 Login",
            bootstyle="success",
            width=30,
            command=self.login,
        ).pack(pady=10)

        self.username.focus_set()

    def login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter Username and Password.")
            return

        user = self.db.login(username, password)

        if user:

            messagebox.showinfo("Success", "Login Successful.")

            for widget in self.root.winfo_children():
                widget.destroy()

            DashboardWindow(self.root)

        else:

            messagebox.showerror("Login Failed", "Invalid Username or Password.")

    def toggle_password(self):

        if self.show_password:

            self.password.config(show="*")
            self.eye_btn.config(text="👁")
            self.show_password = False

        else:

            self.password.config(show="")
            self.eye_btn.config(text="🙈")
            self.show_password = True
