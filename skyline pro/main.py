import ttkbootstrap as ttk

from config import APP_NAME
from gui.login import LoginWindow


def main():

    app = ttk.Window(title=APP_NAME, themename="flatly")

    app.geometry("1400x800")
    app.minsize(1100, 700)

    LoginWindow(app)

    app.mainloop()


if __name__ == "__main__":
    main()
