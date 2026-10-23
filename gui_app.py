import tkinter as tk
from tkinter import messagebox
from system_logic import login_user, register_user, check_booking_rules
import sqlite3

BG_MAIN = "linen"
BG_CARD = "white"
NAVY_DARK = "midnightblue"
NAVY_LIGHT = "navy"
BRASS = "darkgoldenrod"
TEXT_DARK = "black"
TEXT_MUTED = "dimgrey"
BORDER = "royalblue"

def get_db_connection():
    conn = sqlite3.connect("campus_booking.db")
    conn.row_factory = sqlite3.Row
    return conn


class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Campus Resource Booking")
        self.root.geometry("550x800")
        self.root.configure(bg=BG_MAIN)
        self.current_user = None
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="S M A R T   C A M P U S", font=("Times New Roman", 22, "bold"), bg=BG_MAIN,
                 fg=NAVY_DARK).pack(pady=(80, 5))
        tk.Label(self.root, text="Resource Booking System", font=("Times New Roman", 11, "italic"), bg=BG_MAIN,
                 fg=TEXT_MUTED).pack(pady=(0, 40))

        card = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=40, pady=40)
        card.pack(pady=20, padx=60)

        tk.Label(card, text="Username", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.username_entry = tk.Entry(card, width=30, font=("Times New Roman", 12), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                       highlightthickness=1, highlightbackground=BORDER)
        self.username_entry.pack(pady=(5, 20), ipady=6)

        tk.Label(card, text="Password", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.password_entry = tk.Entry(card, width=30, font=("Times New Roman", 12), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                       highlightthickness=1, highlightbackground=BORDER, show="*")
        self.password_entry.pack(pady=(5, 25), ipady=6)

        tk.Button(self.root, text="SIGN IN", command=self.handle_login, bg=NAVY_DARK, fg="white", width=25,
                  font=("Times New Roman", 11, "bold"), relief="flat", pady=10, cursor="hand2",
                  activebackground=NAVY_LIGHT).pack(pady=(10, 15))
        tk.Button(self.root, text="Create an Account", command=self.show_register_screen, bg=BG_MAIN, fg=NAVY_DARK,
                  width=25, font=("Times New Roman", 10, "underline"), relief="flat", cursor="hand2",
                  activebackground=BG_MAIN).pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        user = login_user(username, password)
        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_register_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Create Account", font=("Times New Roman", 18, "bold"), bg=BG_MAIN, fg=NAVY_DARK).pack(
            pady=(40, 20))

        card = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=30, pady=30)
        card.pack(pady=10)

        tk.Label(card, text="Username", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        reg_user = tk.Entry(card, width=30, font=("Times New Roman", 12), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                            highlightthickness=1, highlightbackground=BORDER)
        reg_user.pack(pady=(5, 15), ipady=6)

        tk.Label(card, text="Password", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        reg_pass = tk.Entry(card, width=30, font=("Times New Roman", 12), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                            highlightthickness=1, highlightbackground=BORDER, show="*")
        reg_pass.pack(pady=(5, 15), ipady=6)

        tk.Label(card, text="Role (Lecturer/CampusAdmin/SystemOperator)", font=("Times New Roman", 9), bg=BG_CARD,
                 fg=TEXT_DARK).pack(anchor="w")
        reg_role = tk.Entry(card, width=30, font=("Times New Roman", 12), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                            highlightthickness=1, highlightbackground=BORDER)
        reg_role.pack(pady=(5, 15), ipady=6)

        tk.Label(card, text="Campus ID (1, 2, 3)", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        reg_campus = tk.Entry(card, width=30, font=("Times New Roman", 12), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                              highlightthickness=1, highlightbackground=BORDER)
        reg_campus.pack(pady=(5, 15), ipady=6)

        def submit():
            u, p, r, c = reg_user.get(), reg_pass.get(), reg_role.get(), reg_campus.get()
            if not u or not p or not r:
                messagebox.showerror("Error", "Fill in all fields.")
                return

            r_lower = r.lower()
            if "admin" in r_lower:
                r = "CampusAdmin"
            elif "operator" in r_lower:
                r = "SystemOperator"
            elif "lecturer" in r_lower:
                r = "Lecturer"

            campus_id = int(c) if c else None
            if register_user(u, p, r, campus_id):
                messagebox.showinfo("Success", "Registered! Please log in.")
                self.show_login_screen()
            else:
                messagebox.showerror("Error", "Username already exists.")

        tk.Button(self.root, text="REGISTER", command=submit, bg=NAVY_DARK, fg="white", width=25,
                  font=("Times New Roman", 11, "bold"), relief="flat", pady=10, cursor="hand2",
                  activebackground=NAVY_LIGHT).pack(pady=20)
        tk.Button(self.root, text="Back to Login", command=self.show_login_screen, bg=BG_MAIN, fg=TEXT_MUTED, width=25,
                  font=("Times New Roman", 9), relief="flat", cursor="hand2").pack()

    def show_dashboard(self):
        self.clear_window()

        header = tk.Frame(self.root, bg=NAVY_DARK, pady=20)
        header.pack(fill="x")

        tk.Label(header, text=f"{self.current_user.username}", font=("Times New Roman", 16, "bold"), bg=NAVY_DARK,
                 fg="white").pack()
        tk.Label(header, text=f"{self.current_user.get_role()}", font=("Times New Roman", 10, "italic"), bg=NAVY_DARK,
                 fg=BRASS).pack()

        tk.Button(self.root, text="Logout", command=self.show_login_screen, bg=BG_MAIN, fg=TEXT_MUTED, width=10,
                  font=("Times New Roman", 9, "underline"), relief="flat", cursor="hand2").pack(anchor="ne", padx=15, pady=10)

        role = self.current_user.get_role()

        if role == "Lecturer":
            self.build_lecturer_dashboard()
        elif role == "CampusAdmin":
            self.build_admin_dashboard()
        elif role == "SystemOperator":
            self.build_operator_dashboard()
        else:
            tk.Label(self.root, text="Unknown Role. Please log out and register again.", fg="red", bg=BG_MAIN,
                     font=("Times New Roman", 12)).pack(pady=50)

    def build_lecturer_dashboard(self):
        tk.Label(self.root, text="Book a Resource", font=("Times New Roman", 16, "bold"), bg=BG_MAIN, fg=NAVY_DARK).pack(
            pady=(20, 10))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, type FROM resources WHERE campus_id = ?", (self.current_user.campus_id,))
        resources = cursor.fetchall()
        conn.close()

        if not resources:
            tk.Label(self.root, text="No resources available for your campus yet.", fg=NAVY_LIGHT, bg=BG_MAIN,
                     font=("Times New Roman", 10, "italic")).pack(pady=20)
            return

        card = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=25, pady=20)
        card.pack(pady=10, fill="x", padx=40)

        tk.Label(card, text="Select Resource", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.resource_var = tk.StringVar(self.root)
        resource_options = [f"{r['id']} - {r['name']} ({r['type']})" for r in resources]
        self.resource_var.set(resource_options[0] if resource_options else "")

        opt = tk.OptionMenu(card, self.resource_var, *resource_options)
        opt.config(font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK, relief="flat", highlightthickness=1,
                   highlightbackground=BORDER)
        opt.pack(fill="x", pady=(5, 15))

        # DATE ENTRY WITH PLACEHOLDER
        tk.Label(card, text="Date", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.date_entry = tk.Entry(card, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                   highlightthickness=1, highlightbackground=BORDER)
        self.date_entry.pack(fill="x", pady=(5, 15), ipady=5)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.config(fg="#A0A0A0")
        self.date_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "YYYY-MM-DD"))
        self.date_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, "YYYY-MM-DD"))

        tk.Label(card, text="Start Time", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.time_entry = tk.Entry(card, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                   highlightthickness=1, highlightbackground=BORDER)
        self.time_entry.pack(fill="x", pady=(5, 15), ipady=5)
        self.time_entry.insert(0, "HH:MM (e.g. 14:30)")
        self.time_entry.config(fg="#A0A0A0")
        self.time_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "HH:MM (e.g. 14:30)"))
        self.time_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, "HH:MM (e.g. 14:30)"))

        tk.Label(card, text="Duration (hours)", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.duration_entry = tk.Entry(card, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                       highlightthickness=1, highlightbackground=BORDER)
        self.duration_entry.pack(fill="x", pady=(5, 10), ipady=5)

        tk.Button(self.root, text="CONFIRM BOOKING", bg=NAVY_DARK, fg="white", width=25, font=("Times New Roman", 11, "bold"),
                  relief="flat", pady=8, cursor="hand2", activebackground=NAVY_LIGHT, command=self.submit_booking).pack(
            pady=20)

        tk.Label(self.root, text="— My Bookings —", font=("Times New Roman", 11, "bold"), bg=BG_MAIN, fg=NAVY_DARK).pack(
            pady=(10, 5))

        listbox = tk.Listbox(self.root, width=60, height=5, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK,
                             relief="flat", highlightthickness=1, highlightbackground=BORDER)
        listbox.pack(pady=5)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT b.id, r.name, b.date, b.start_time 
        FROM bookings b JOIN resources r ON b.resource_id = r.id 
        WHERE b.user_id = ?
        ''', (self.current_user.user_id,))
        my_bookings = cursor.fetchall()
        conn.close()

        self.booking_ids = []
        for b in my_bookings:
            listbox.insert(tk.END, f"  ID:{b['id']}  |  {b['name']}  |  {b['date']} at {b['start_time']}  ")
            self.booking_ids.append(b['id'])

        tk.Button(self.root, text="Cancel Selected Booking", bg=BG_MAIN, fg=TEXT_MUTED, width=20,
                  font=("Times New Roman", 9, "underline"), relief="flat", cursor="hand2",
                  command=lambda: self.cancel_booking(listbox)).pack(pady=5)

    def clear_placeholder(self, event, placeholder_text):
        if event.widget.get() == placeholder_text:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=TEXT_DARK)

    def add_placeholder(self, event, placeholder_text):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder_text)
            event.widget.config(fg="#A0A0A0")

    def cancel_booking(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return

        index = selection[0]
        booking_id = self.booking_ids[index]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Booking cancelled.")
        self.build_lecturer_dashboard()

    def submit_booking(self):
        if not self.resource_var.get(): return
        resource_id = int(self.resource_var.get().split(" - ")[0])

        date = self.date_entry.get()
        time = self.time_entry.get()
        duration = self.duration_entry.get()

        if not date or date == "YYYY-MM-DD" or not time or time == "HH:MM (e.g. 14:30)" or not duration:
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        try:
            duration = int(duration)
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number.")
            return

        is_valid, message = check_booking_rules(self.current_user.campus_id, resource_id, date, time, duration)
        if not is_valid:
            messagebox.showerror("Booking Failed", message)
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO bookings (user_id, resource_id, campus_id, date, start_time, duration)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.current_user.user_id, resource_id, self.current_user.campus_id, date, time, duration))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Booking confirmed!")
        self.build_lecturer_dashboard()


    def build_admin_dashboard(self):
        tk.Label(self.root, text="Manage Resources", font=("Times New Roman", 16, "bold"), bg=BG_MAIN, fg=NAVY_DARK).pack(
            pady=(15, 5))

        card = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=25, pady=15)
        card.pack(pady=10, fill="x", padx=40)

        tk.Label(card, text="Resource Name", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.res_name = tk.Entry(card, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                 highlightthickness=1, highlightbackground=BORDER)
        self.res_name.pack(fill="x", pady=(5, 10), ipady=4)

        tk.Label(card, text="Resource Type", font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.res_type = tk.Entry(card, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK, relief="flat",
                                 highlightthickness=1, highlightbackground=BORDER)
        self.res_type.pack(fill="x", pady=(5, 10), ipady=4)

        tk.Button(self.root, text="ADD RESOURCE", bg=NAVY_DARK, fg="white", width=25, font=("Times New Roman", 11, "bold"),
                  relief="flat", pady=6, cursor="hand2", activebackground=NAVY_LIGHT, command=self.add_resource).pack(
            pady=15)

        tk.Label(self.root, text="— Available Resources on Campus —", font=("Times New Roman", 11, "bold"), bg=BG_MAIN,
                 fg=NAVY_DARK).pack(pady=(5, 5))

        listbox = tk.Listbox(self.root, width=60, height=6, font=("Times New Roman", 10), bg=BG_CARD, fg=TEXT_DARK,
                             relief="flat", highlightthickness=1, highlightbackground=BORDER)
        listbox.pack(pady=5)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT name, type FROM resources WHERE campus_id = ?
        ''', (self.current_user.campus_id,))
        campus_resources = cursor.fetchall()
        conn.close()

        for r in campus_resources:
            listbox.insert(tk.END, f"  {r['name']}  |  {r['type']}  ")

    def add_resource(self):
        name, r_type = self.res_name.get(), self.res_type.get()
        if not name or not r_type:
            messagebox.showerror("Error", "Fill in all fields.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO resources (name, type, campus_id) VALUES (?, ?, ?)",
                           (name, r_type, self.current_user.campus_id))
            conn.commit()
            messagebox.showinfo("Success", "Resource added!")

            self.res_name.delete(0, tk.END)
            self.res_type.delete(0, tk.END)

            self.build_admin_dashboard()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Resource already exists.")
        finally:
            conn.close()

    def build_operator_dashboard(self):
        tk.Label(self.root, text="Cross-Campus Reports", font=("Times New Roman", 16, "bold"), bg=BG_MAIN, fg=NAVY_DARK).pack(
            pady=(20, 10))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT c.name, COUNT(b.id) as total
        FROM campuses c LEFT JOIN bookings b ON c.id = b.campus_id
        GROUP BY c.id
        ''')
        report1 = cursor.fetchall()

        card1 = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=25, pady=15)
        card1.pack(fill="x", padx=40, pady=10)
        tk.Label(card1, text="Campus Usage", font=("Times New Roman", 11, "bold"), bg=BG_CARD, fg=NAVY_DARK).pack(anchor="w")
        for row in report1:
            tk.Label(card1, text=f"• {row['name']}: {row['total']} bookings", bg=BG_CARD, fg=TEXT_DARK,
                     font=("Times New Roman", 10)).pack(anchor="w", pady=2)

        cursor.execute('''
        SELECT r.name, COUNT(b.id) as total
        FROM resources r LEFT JOIN bookings b ON r.id = b.resource_id
        GROUP BY r.id ORDER BY total DESC LIMIT 1
        ''')
        report2 = cursor.fetchone()

        card2 = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=25, pady=15)
        card2.pack(fill="x", padx=40, pady=10)
        tk.Label(card2, text="Most Used Resource", font=("Times New Roman", 11, "bold"), bg=BG_CARD, fg=NAVY_DARK).pack(
            anchor="w")
        if report2 and report2['total'] > 0:
            tk.Label(card2, text=f"• {report2['name']} ({report2['total']} times)", bg=BG_CARD, fg=TEXT_DARK,
                     font=("Times New Roman", 10)).pack(anchor="w", pady=2)
        else:
            tk.Label(card2, text="• No bookings yet", bg=BG_CARD, fg=TEXT_DARK, font=("Times New Roman", 10)).pack(anchor="w",
                                                                                                            pady=2)

        cursor.execute("SELECT AVG(duration) as avg_dur FROM bookings")
        report3 = cursor.fetchone()

        card3 = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=25, pady=15)
        card3.pack(fill="x", padx=40, pady=10)
        tk.Label(card3, text="Booking Trends", font=("Times New Roman", 11, "bold"), bg=BG_CARD, fg=NAVY_DARK).pack(anchor="w")
        avg = round(report3['avg_dur'], 2) if report3['avg_dur'] else 0
        tk.Label(card3, text=f"• Average duration: {avg} hours", bg=BG_CARD, fg=TEXT_DARK, font=("Times New Roman", 10)).pack(
            anchor="w", pady=2)

        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()