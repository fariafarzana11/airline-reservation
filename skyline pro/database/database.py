import sqlite3
import os


class Database:

    def __init__(self):

        os.makedirs("database", exist_ok=True)

        self.db_path = os.path.join("database", "skyline.db")

        self.create_tables()

    # ==================================================
    # CONNECTION
    # ==================================================

    def connect(self):

        return sqlite3.connect(self.db_path)

    # ==================================================
    # CREATE TABLES
    # ==================================================

    def create_tables(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            # ============================================
            # ADMIN
            # ===========================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    username TEXT NOT NULL UNIQUE,

                    password TEXT NOT NULL

                )
            """)

            cursor.execute(
                """
                SELECT id
                FROM admins
                WHERE username = ?
            """,
                ("admin",),
            )

            if cursor.fetchone() is None:

                cursor.execute(
                    """
                    INSERT INTO admins (
                        username,
                        password
                    )
                    VALUES (?, ?)
                """,
                    ("admin", "admin123"),
                )

            # ==================================================
            # PASSENGERS
            # ==================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passengers (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    name TEXT NOT NULL,

                    phone TEXT,

                    email TEXT,

                    passport TEXT,

                    gender TEXT,

                    date_of_birth TEXT,

                    nationality TEXT,

                    address TEXT

                )
            """)

            # ============================================
            # FLIGHTS
            # ============================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flights (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    flight_number TEXT NOT NULL UNIQUE,

                    airline TEXT NOT NULL,

                    departure TEXT NOT NULL,

                    arrival TEXT NOT NULL,

                    departure_date TEXT NOT NULL,

                    departure_time TEXT NOT NULL,

                    arrival_time TEXT NOT NULL,

                    aircraft TEXT NOT NULL,

                    total_seats INTEGER NOT NULL,

                    available_seats INTEGER NOT NULL,

                    price REAL NOT NULL,

                    status TEXT NOT NULL
                        DEFAULT 'Scheduled',

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP

                )
            """)

            # ============================================
            # BOOKING TABLE
            # ==========================================
            cursor.execute("""
                
                
                CREATE TABLE IF NOT EXISTS bookings (
            
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
            
                    passenger_id INTEGER NOT NULL,
            
                    flight_id INTEGER NOT NULL,
            
                    seat_no TEXT NOT NULL,
            
                    booking_date TEXT NOT NULL,
            
                    total_amount REAL NOT NULL,
            
                    status TEXT NOT NULL DEFAULT 'Confirmed',
            
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        
                    
                    FOREIGN KEY (passenger_id)
                          REFERENCES passengers(id),        
                          
                    FOREIGN KEY (flight_id)
                        REFERENCES flights(id),
                        
                    UNIQUE (flight_id, seat_no)
                
                 )
                
            """)

            conn.commit()

        finally:
            conn.close()

    # ==================================================
    # LOGIN
    # ==================================================

    def login(self, username, password):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM admins
                WHERE username = ?
                AND password = ?
            """,
                (username, password),
            )

            return cursor.fetchone()

        finally:

            conn.close()

    # ==================================================
    # PASSENGER
    # ==================================================

    def add_passenger(
        self, name, phone, email, passport, gender, date_of_birth, nationality, address
    ):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO passengers (
                    name,
                    phone,
                    email,
                    passport,
                    gender,
                    date_of_birth,
                    nationality,
                    address
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """,
                (
                    name,
                    phone,
                    email,
                    passport,
                    gender,
                    date_of_birth,
                    nationality,
                    address,
                ),
            )

            conn.commit()

            return cursor.lastrowid

        finally:

            conn.close()

    # ==================================================
    # GET PASSENGERS
    # ==================================================

    def get_passengers(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    name,
                    phone,
                    email,
                    passport,
                    gender,
                    date_of_birth,
                    nationality,
                    address
                FROM passengers
                ORDER BY id ASC
            """)

            return cursor.fetchall()

        finally:

            conn.close()

    # ==================================================
    # SEARCH PASSENGERS
    # ==================================================

    def search_passengers(self, keyword):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            keyword = f"%{keyword}%"

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    phone,
                    email,
                    passport,
                    gender,
                    date_of_birth,
                    nationality,
                    address

                FROM passengers

                WHERE name LIKE ?
                   OR phone LIKE ?
                   OR email LIKE ?
                   OR passport LIKE ?
                   OR nationality LIKE ?

                ORDER BY id ASC

            """,
                (keyword, keyword, keyword, keyword, keyword),
            )

            return cursor.fetchall()

        finally:

            conn.close()

    # ==================================================
    # UPDATE PASSENGER
    # ==================================================

    def update_passenger(
        self,
        passenger_id,
        name,
        phone,
        email,
        passport,
        gender,
        date_of_birth,
        nationality,
        address,
    ):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE passengers

                SET
                    name = ?,
                    phone = ?,
                    email = ?,
                    passport = ?,
                    gender = ?,
                    date_of_birth = ?,
                    nationality = ?,
                    address = ?

                WHERE id = ?

            """,
                (
                    name,
                    phone,
                    email,
                    passport,
                    gender,
                    date_of_birth,
                    nationality,
                    address,
                    passenger_id,
                ),
            )

            conn.commit()

            return cursor.rowcount

        finally:

            conn.close()

    # ==================================================
    # DELETE PASSENGER
    # ==================================================

    def delete_passenger(self, passenger_id):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM passengers
                WHERE id = ?
            """,
                (passenger_id,),
            )

            conn.commit()

            return cursor.rowcount

        finally:

            conn.close()

    # ==================================================
    # PASSENGER STATISTICS
    # ==================================================

    def get_passenger_statistics(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM passengers
            """)

            total = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM passengers
                WHERE gender = 'Male'
            """)

            male = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM passengers
                WHERE gender = 'Female'
            """)

            female = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM passengers

                WHERE nationality IS NOT NULL
                AND nationality != ''
                AND LOWER(nationality) != 'bangladesh'
            """)

            international = cursor.fetchone()[0]

            return (total, male, female, international)

        finally:

            conn.close()

    # ==================================================
    # FLIGHT
    # ==================================================

    def add_flight(
        self,
        flight_number,
        airline,
        departure,
        arrival,
        departure_date,
        departure_time,
        arrival_time,
        aircraft,
        total_seats,
        price,
        status,
    ):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO flights (

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
                    status

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,
                (
                    flight_number,
                    airline,
                    departure,
                    arrival,
                    departure_date,
                    departure_time,
                    arrival_time,
                    aircraft,
                    total_seats,
                    total_seats,
                    price,
                    status,
                ),
            )

            conn.commit()

            return True

        except sqlite3.IntegrityError:

            return False

        finally:

            conn.close()

    # ==================================================
    # GET FLIGHTS
    # ==================================================

    def get_all_flights(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
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
                    status

                FROM flights

                ORDER BY id ASC
            """)

            return cursor.fetchall()

        finally:

            conn.close()

    # update flight
    def update_flight(
        self,
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
        price,
        status,
    ):
        conn = None

        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Check duplicate flight number
            cursor.execute(
                """
            SELECT id
            FROM flights
            WHERE flight_number = ?
            AND id != ?
            """,
                (flight_number, flight_id),
            )

            if cursor.fetchone():
                return False

            cursor.execute(
                """
            UPDATE flights
            SET
                flight_number = ?,
                airline = ?,
                departure = ?,
                arrival = ?,
                departure_date = ?,
                departure_time = ?,
                arrival_time = ?,
                aircraft = ?,
                total_seats = ?,
                available_seats = ?,
                price = ?,
                status = ?
            WHERE id = ?
            """,
                (
                    flight_number,
                    airline,
                    departure,
                    arrival,
                    departure_date,
                    departure_time,
                    arrival_time,
                    aircraft,
                    total_seats,
                    total_seats,
                    price,
                    status,
                    flight_id,
                ),
            )

            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:

            print("Update Flight Error:", e)

            return False

        finally:

            if conn:
                conn.close()

    def delete_flight(self, flight_id):

        conn = None

        try:
            conn = self.connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM flights
                WHERE id = ?
                """,
                (flight_id,),
            )

            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:

            print("Delete Flight Error:", e)

            return False

        finally:

            if conn:
                conn.close()

    # ==================================================
    # SEARCH FLIGHTS
    # ==================================================

    def search_flights(self, keyword="", status="All"):

        conn = None

        try:
            conn = self.connect()
            cursor = conn.cursor()

            keyword = keyword.strip()

            search = f"%{keyword}%"

            if status == "All":

                cursor.execute(
                    """
                SELECT
                    id,
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
                    status
                FROM flights
                WHERE
                    flight_number LIKE ?
                    OR airline LIKE ?
                    OR departure LIKE ?
                    OR arrival LIKE ?
                    OR aircraft LIKE ?
                ORDER BY id ASC
                """,
                    (
                        search,
                        search,
                        search,
                        search,
                        search,
                    ),
                )

            else:

                cursor.execute(
                    """
                   SELECT
                       id,
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
                       status
                    FROM flights
                    WHERE
                        (
                           flight_number LIKE ?
                           OR airline LIKE ?
                           OR departure LIKE ?
                           OR arrival LIKE ?
                           OR aircraft LIKE ?
                        )
                        AND status = ?
                    ORDER BY id ASC
                    """,
                    (
                        search,
                        search,
                        search,
                        search,
                        search,
                        status,
                    ),
                )

            flights = cursor.fetchall()

            return flights

        except Exception as e:

            print("Search Flight Error:", e)

            return []

        finally:

            if conn:
                conn.close()

    # ==================================================
    # FLIGHT COUNT
    # ==================================================

    def get_total_flights(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM flights
            """)

            return cursor.fetchone()[0]

        finally:

            conn.close()

    # ==================================================
    # BOOKING COUNT
    # ==================================================

    def get_total_bookings(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM bookings
            """)

            return cursor.fetchone()[0]

        finally:

            conn.close()

    # ==================================================
    # TOTAL REVENUE
    # ==================================================

    def get_total_revenue(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(total_amount),
                        0
                    )

                FROM bookings
            """)

            return cursor.fetchone()[0]

        finally:

            conn.close()

    # ==================================================
    # ACTIVE FLIGHTS
    # ==================================================

    def get_active_flights(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM flights
                WHERE status = 'Active'
            """)

            return cursor.fetchone()[0]

        finally:

            conn.close()

    # ==================================================
    # PENDING BOOKINGS
    # ==================================================

    def get_pending_bookings(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE status = 'Pending'
            """)

            return cursor.fetchone()[0]

        finally:

            conn.close()

    # ==================================================
    # DASHBOARD STATISTICS
    # ==================================================

    def get_statistics(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM flights
            """)

            total_flights = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM flights
                WHERE status = 'Scheduled'
            """)

            scheduled_flights = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COALESCE(
                    SUM(total_seats),
                    0
                )

                FROM flights
            """)

            total_seats = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COALESCE(
                    SUM(available_seats),
                    0
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

        finally:

            conn.close()

    # ==================================================
    # RECENT BOOKINGS
    # ==================================================

    def get_recent_bookings(self):

        conn = self.connect()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    b.id,
                    p.name,
                    f.flight_number,
                    b.seat_no,
                    b.booking_date,
                    b.status

                FROM bookings b

                LEFT JOIN passengers p
                    ON b.passenger_id = p.id

                LEFT JOIN flights f
                    ON b.flight_id = f.id

                ORDER BY b.id ASC

                LIMIT 10
            """)

            return cursor.fetchall()

        finally:

            conn.close()

    # ==========================================
    # ADD BOOKING
    # ==========================================

    def add_booking(
        self, passenger_id, flight_id, seat_no, booking_date, total_amount, status
    ):

        conn = self.connect()
        cursor = conn.cursor()

        try:

            # --------------------------------------
            # CHECK FLIGHT
            # --------------------------------------

            cursor.execute(
                """
                SELECT available_seats
                FROM flights
                WHERE id = ?
                """,
                (flight_id,),
            )

            flight = cursor.fetchone()

            if not flight:
                return False

            available_seats = flight[0]

            if available_seats <= 0:
                return False

            # --------------------------------------
            # CHECK DUPLICATE SEAT
            # --------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM bookings
                WHERE flight_id = ?
                AND seat_no = ?
                AND status != 'Cancelled'
                """,
                (flight_id, seat_no),
            )

            existing_booking = cursor.fetchone()

            if existing_booking:
                return False

            # --------------------------------------
            # INSERT BOOKING
            # --------------------------------------

            cursor.execute(
                """
                INSERT INTO bookings
                (
                    passenger_id,
                    flight_id,
                    seat_no,
                    booking_date,
                    total_amount,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (passenger_id, flight_id, seat_no, booking_date, total_amount, status),
            )

            # --------------------------------------
            # REDUCE AVAILABLE SEATS
            # --------------------------------------

            cursor.execute(
                """
                UPDATE flights
                SET available_seats = available_seats - 1
                WHERE id = ?
                AND available_seats > 0
                """,
                (flight_id,),
            )

            conn.commit()

            return True

        except Exception as e:

            conn.rollback()

            print("Add Booking Error:", e)

            return False

        finally:

            conn.close()

    # ==========================================
    # GET ALL BOOKINGS
    # ==========================================

    def get_all_bookings(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                b.id,
                p.name,
                f.flight_number,
                b.seat_no,
                b.booking_date,
                b.total_amount,
                b.status
            FROM bookings b
    
            LEFT JOIN passengers p
                ON b.passenger_id = p.id
    
            LEFT JOIN flights f
                ON b.flight_id = f.id
    
            ORDER BY b.id DESC
        """)

        bookings = cursor.fetchall()

        conn.close()

        return bookings

    # ==========================================
    # TOTAL BOOKINGS
    # ==========================================

    def get_total_bookings(self):
        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM bookings
            WHERE status != 'Cancelled'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    # ==========================================
    # GET FLIGHT SEAT INFO
    # ==========================================

    def get_flight_seat_info(self, flight_id):

        conn = self.connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    total_seats,
                    available_seats
                FROM flights
                WHERE id = ?
                """,
                (flight_id,),
            )

            return cursor.fetchone()

        finally:

            conn.close()

    # ==========================================

    # GET BOOKED SEATS
    # ==========================================

    def get_booked_seats(self, flight_id):

        conn = self.connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT seat_no
                FROM bookings
                WHERE flight_id = ?
                AND status != 'Cancelled'
                """,
                (flight_id,),
            )

            rows = cursor.fetchall()

            return [row[0] for row in rows]

        finally:

            conn.close()

    # ==========================================
    # TOTAL BOOKING REVENUE
    # ==========================================

    def get_total_revenue(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0)
            FROM bookings
            WHERE status != 'Cancelled'
        """)

        revenue = cursor.fetchone()[0]

        conn.close()

        return revenue

    # CLOSE
    # ==================================================

    def close(self):
        pass
