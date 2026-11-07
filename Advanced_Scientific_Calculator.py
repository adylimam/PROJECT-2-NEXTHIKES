import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from datetime import datetime, date

# Matplotlib integration with Tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class AdvancedCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Multi-Tool Calculator")
        self.geometry("680x760")
        self.minsize(620, 700)

        # Style configuration
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(bg="#222831")

        # Create Tab Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize Tabs
        self.scientific_tab = ScientificTab(self.notebook)
        self.bmi_tab = BMITab(self.notebook)
        self.age_tab = AgeTab(self.notebook)
        self.emi_tab = EMITab(self.notebook)
        self.stats_tab = StatisticsTab(self.notebook)
        self.graph_tab = GraphTab(self.notebook)

        self.notebook.add(self.scientific_tab, text="Scientific")
        self.notebook.add(self.bmi_tab, text="BMI")
        self.notebook.add(self.age_tab, text="Age")
        self.notebook.add(self.emi_tab, text="Loan EMI")
        self.notebook.add(self.stats_tab, text="Statistics")
        self.notebook.add(self.graph_tab, text="Graph")

        # Global Key Bindings for Keyboard Support
        self.bind("<Key>", self.handle_keyboard_input)

    def handle_keyboard_input(self, event):
        current_tab_index = self.notebook.index(self.notebook.select())
        active_tab = [
            self.scientific_tab,
            self.bmi_tab,
            self.age_tab,
            self.emi_tab,
            self.stats_tab,
            self.graph_tab,
        ][current_tab_index]

        if hasattr(active_tab, "process_key"):
            active_tab.process_key(event)


# ==============================================================================
# TAB 1: SCIENTIFIC CALCULATOR (UPDATED)
# ==============================================================================
class ScientificTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.expression = ""
        self.angle_mode = "DEG"  # Default mode: 'DEG' or 'RAD'

        # Top Bar: Angle Mode Indicator & Switch Buttons
        top_bar = tk.Frame(self, bg="#222831")
        top_bar.pack(fill="x", padx=10, pady=(8, 2))

        self.mode_label = tk.Label(
            top_bar,
            text="MODE: DEG",
            font=("Arial", 10, "bold"),
            bg="#222831",
            fg="#00ADB5",
        )
        self.mode_label.pack(side="left", padx=5)

        self.btn_deg = tk.Button(
            top_bar,
            text="DEG",
            font=("Arial", 9, "bold"),
            bg="#00ADB5",
            fg="#EEEEEE",
            activebackground="#008C94",
            activeforeground="#FFFFFF",
            relief="flat",
            width=6,
            command=lambda: self.set_angle_mode("DEG"),
        )
        self.btn_deg.pack(side="right", padx=3)

        self.btn_rad = tk.Button(
            top_bar,
            text="RAD",
            font=("Arial", 9, "bold"),
            bg="#393E46",
            fg="#EEEEEE",
            activebackground="#008C94",
            activeforeground="#FFFFFF",
            relief="flat",
            width=6,
            command=lambda: self.set_angle_mode("RAD"),
        )
        self.btn_rad.pack(side="right", padx=3)

        # Display Entry
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Consolas", 22, "bold"),
            bg="#393E46",
            fg="#EEEEEE",
            bd=10,
            relief="flat",
            justify="right",
        )
        self.display.pack(fill="x", padx=10, pady=8)

        # Buttons Grid Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 7 Rows x 6 Columns Layout
        buttons = [
            ("sin", 0, 0), ("cos", 0, 1), ("tan", 0, 2), ("^", 0, 3), ("sqrt", 0, 4), ("C", 0, 5),
            ("asin", 1, 0), ("acos", 1, 1), ("atan", 1, 2), ("log", 1, 3), ("ln", 1, 4), ("DEL", 1, 5),
            ("sinh", 2, 0), ("cosh", 2, 1), ("tanh", 2, 2), ("(", 2, 3), (")", 2, 4), ("/", 2, 5),
            ("x^2", 3, 0), ("x^3", 3, 1), ("1/x", 3, 2), ("7", 3, 3), ("8", 3, 4), ("9", 3, 5),
            ("10^x", 4, 0), ("e^x", 4, 1), ("abs", 4, 2), ("4", 4, 3), ("5", 4, 4), ("6", 4, 5),
            ("fact", 5, 0), ("pi", 5, 1), ("e", 5, 2), ("1", 5, 3), ("2", 5, 4), ("3", 5, 5),
            ("%", 6, 0), ("*", 6, 1), ("-", 6, 2), ("0", 6, 3), (".", 6, 4), ("=", 6, 5),
        ]

        for i in range(7):
            btn_frame.rowconfigure(i, weight=1)
        for j in range(6):
            btn_frame.columnconfigure(j, weight=1)

        for text, row, col in buttons:
            if text == "=":
                bg_color = "#00ADB5"
            elif text in ("C", "DEL"):
                bg_color = "#D65A31"
            elif text.isdigit() or text in (".", "%"):
                bg_color = "#2E3440"
            else:
                bg_color = "#393E46"

            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Arial", 11, "bold"),
                bg=bg_color,
                fg="#EEEEEE",
                activebackground="#00ADB5",
                activeforeground="#FFFFFF",
                relief="groove",
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def set_angle_mode(self, mode):
        self.angle_mode = mode
        self.mode_label.config(text=f"MODE: {mode}")
        if mode == "DEG":
            self.btn_deg.config(bg="#00ADB5")
            self.btn_rad.config(bg="#393E46")
        else:
            self.btn_rad.config(bg="#00ADB5")
            self.btn_deg.config(bg="#393E46")

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        elif char == "=":
            self.calculate()
        elif char in [
            "sin", "cos", "tan", "asin", "acos", "atan",
            "sinh", "cosh", "tanh", "sqrt", "log", "ln", "abs", "fact"
        ]:
            if self.display_var.get() == "0":
                self.expression = f"{char}("
            else:
                self.expression += f"{char}("
            self.display_var.set(self.expression)
        elif char == "^":
            self.expression += "**"
            self.display_var.set(self.expression)
        elif char == "x^2":
            self.expression += "**2"
            self.display_var.set(self.expression)
        elif char == "x^3":
            self.expression += "**3"
            self.display_var.set(self.expression)
        elif char == "10^x":
            self.expression += "10**"
            self.display_var.set(self.expression)
        elif char == "e^x":
            self.expression += "exp("
            self.display_var.set(self.expression)
        elif char == "1/x":
            self.expression += "1/("
            self.display_var.set(self.expression)
        elif char == "pi":
            self.expression += str(math.pi)
            self.display_var.set(self.expression)
        elif char == "e":
            self.expression += str(math.e)
            self.display_var.set(self.expression)
        else:
            if self.display_var.get() == "0" and char not in "+-*/.%":
                self.expression = char
            else:
                self.expression += char
            self.display_var.set(self.expression)

    def calculate(self):
        try:
            # Trig handlers based on current DEG / RAD setting
            if self.angle_mode == "DEG":
                sin_fn = lambda x: math.sin(math.radians(x))
                cos_fn = lambda x: math.cos(math.radians(x))
                tan_fn = lambda x: math.tan(math.radians(x))
                asin_fn = lambda x: math.degrees(math.asin(x))
                acos_fn = lambda x: math.degrees(math.acos(x))
                atan_fn = lambda x: math.degrees(math.atan(x))
            else:
                sin_fn = math.sin
                cos_fn = math.cos
                tan_fn = math.tan
                asin_fn = math.asin
                acos_fn = math.acos
                atan_fn = math.atan

            safe_dict = {
                "sin": sin_fn,
                "cos": cos_fn,
                "tan": tan_fn,
                "asin": asin_fn,
                "acos": acos_fn,
                "atan": atan_fn,
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "exp": math.exp,
                "fact": math.factorial,
                "abs": abs,
                "pi": math.pi,
                "e": math.e,
            }

            result = eval(self.expression, {"__builtins__": None}, safe_dict)
            self.display_var.set(round(result, 8) if isinstance(result, float) else result)
            self.expression = str(self.display_var.get())
        except ZeroDivisionError:
            self.display_var.set("Error: Div by 0")
            self.expression = ""
        except ValueError:
            self.display_var.set("Math Domain Error")
            self.expression = ""
        except Exception:
            self.display_var.set("Syntax Error")
            self.expression = ""

    def process_key(self, event):
        if event.char in "0123456789+-*/.()":
            self.on_button_click(event.char)
        elif event.keysym in ("Return", "KP_Enter"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.on_button_click("DEL")
        elif event.keysym == "Escape":
            self.on_button_click("C")


# ==============================================================================
# TAB 2: BMI CALCULATOR
# ==============================================================================
class BMITab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        container = ttk.Frame(self, padding=25)
        container.pack(expand=True)

        ttk.Label(container, text="Weight (kg):", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        self.weight_entry = ttk.Entry(container, font=("Arial", 12))
        self.weight_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(container, text="Height (cm):", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        self.height_entry = ttk.Entry(container, font=("Arial", 12))
        self.height_entry.grid(row=1, column=1, pady=10, padx=10)

        calc_btn = tk.Button(container, text="Calculate BMI", bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), command=self.calculate_bmi)
        calc_btn.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        self.result_lbl = ttk.Label(container, text="BMI: --", font=("Arial", 14, "bold"))
        self.result_lbl.grid(row=3, column=0, columnspan=2, pady=5)

        self.status_lbl = ttk.Label(container, text="Category: --", font=("Arial", 12))
        self.status_lbl.grid(row=4, column=0, columnspan=2, pady=5)

    def calculate_bmi(self):
        try:
            w = float(self.weight_entry.get())
            h = float(self.height_entry.get()) / 100.0
            bmi = round(w / (h * h), 2)

            if bmi < 18.5:
                cat = "Underweight"
            elif bmi < 24.9:
                cat = "Normal weight"
            elif bmi < 29.9:
                cat = "Overweight"
            else:
                cat = "Obese"

            self.result_lbl.config(text=f"BMI: {bmi}")
            self.status_lbl.config(text=f"Category: {cat}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for height and weight.")

    def process_key(self, event):
        if event.keysym in ("Return", "KP_Enter"):
            self.calculate_bmi()


# ==============================================================================
# TAB 3: AGE CALCULATOR
# ==============================================================================
class AgeTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        container = ttk.Frame(self, padding=25)
        container.pack(expand=True)

        ttk.Label(container, text="Birth Date (DD/MM/YYYY):", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        self.dob_entry = ttk.Entry(container, font=("Arial", 12))
        self.dob_entry.grid(row=0, column=1, pady=10, padx=10)
        self.dob_entry.insert(0, "15/08/1995")

        calc_btn = tk.Button(container, text="Calculate Age", bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), command=self.calculate_age)
        calc_btn.grid(row=1, column=0, columnspan=2, pady=15, sticky="ew")

        self.result_lbl = ttk.Label(container, text="Age: --", font=("Arial", 13, "bold"), justify="center")
        self.result_lbl.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_age(self):
        dob_str = self.dob_entry.get().strip()
        try:
            dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
            today = date.today()

            if dob > today:
                messagebox.showerror("Invalid Date", "Date of birth cannot be in the future.")
                return

            years = today.year - dob.year
            months = today.month - dob.month
            days = today.day - dob.day

            if days < 0:
                months -= 1
                prev_month = today.month - 1 or 12
                prev_year = today.year if prev_month != 12 else today.year - 1
                days += (date(today.year, today.month, 1) - date(prev_year, prev_month, 1)).days

            if months < 0:
                years -= 1
                months += 12

            total_days = (today - dob).days
            self.result_lbl.config(text=f"{years} Years, {months} Months, {days} Days\nTotal Days Lived: {total_days}")
        except ValueError:
            messagebox.showerror("Invalid Format", "Use DD/MM/YYYY format (e.g., 25/12/2000).")

    def process_key(self, event):
        if event.keysym in ("Return", "KP_Enter"):
            self.calculate_age()


# ==============================================================================
# TAB 4: LOAN EMI CALCULATOR
# ==============================================================================
class EMITab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        container = ttk.Frame(self, padding=25)
        container.pack(expand=True)

        ttk.Label(container, text="Principal Loan Amount:", font=("Arial", 11)).grid(row=0, column=0, pady=8, sticky="w")
        self.p_entry = ttk.Entry(container, font=("Arial", 11))
        self.p_entry.grid(row=0, column=1, pady=8, padx=10)

        ttk.Label(container, text="Annual Interest Rate (%):", font=("Arial", 11)).grid(row=1, column=0, pady=8, sticky="w")
        self.r_entry = ttk.Entry(container, font=("Arial", 11))
        self.r_entry.grid(row=1, column=1, pady=8, padx=10)

        ttk.Label(container, text="Tenure (Years):", font=("Arial", 11)).grid(row=2, column=0, pady=8, sticky="w")
        self.t_entry = ttk.Entry(container, font=("Arial", 11))
        self.t_entry.grid(row=2, column=1, pady=8, padx=10)

        calc_btn = tk.Button(container, text="Compute EMI", bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), command=self.calculate_emi)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

        self.emi_lbl = ttk.Label(container, text="Monthly EMI: --", font=("Arial", 12, "bold"))
        self.emi_lbl.grid(row=4, column=0, columnspan=2, pady=3)

        self.interest_lbl = ttk.Label(container, text="Total Interest: --", font=("Arial", 11))
        self.interest_lbl.grid(row=5, column=0, columnspan=2, pady=3)

        self.total_lbl = ttk.Label(container, text="Total Payment: --", font=("Arial", 11))
        self.total_lbl.grid(row=6, column=0, columnspan=2, pady=3)

    def calculate_emi(self):
        try:
            p = float(self.p_entry.get())
            annual_r = float(self.r_entry.get())
            years = float(self.t_entry.get())

            monthly_r = (annual_r / 12) / 100
            months = int(years * 12)

            if monthly_r == 0:
                emi = p / months
            else:
                emi = (p * monthly_r * ((1 + monthly_r) ** months)) / (((1 + monthly_r) ** months) - 1)

            total_payment = emi * months
            total_interest = total_payment - p

            self.emi_lbl.config(text=f"Monthly EMI: {emi:,.2f}")
            self.interest_lbl.config(text=f"Total Interest: {total_interest:,.2f}")
            self.total_lbl.config(text=f"Total Payment: {total_payment:,.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please provide valid numeric inputs.")

    def process_key(self, event):
        if event.keysym in ("Return", "KP_Enter"):
            self.calculate_emi()


# ==============================================================================
# TAB 5: STATISTICS CALCULATOR
# ==============================================================================
class StatisticsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Enter comma-separated numbers:", font=("Arial", 11)).pack(anchor="w", pady=5)
        self.data_entry = ttk.Entry(container, font=("Arial", 11))
        self.data_entry.pack(fill="x", pady=5)
        self.data_entry.insert(0, "12, 15, 23, 23, 16, 19, 24, 26, 30")

        calc_btn = tk.Button(container, text="Calculate Statistics", bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), command=self.calculate_stats)
        calc_btn.pack(fill="x", pady=10)

        self.results_text = tk.Text(container, height=12, font=("Consolas", 11), bg="#393E46", fg="#EEEEEE", relief="flat")
        self.results_text.pack(fill="both", expand=True, pady=5)

    def calculate_stats(self):
        raw = self.data_entry.get().strip()
        try:
            data = [float(x.strip()) for x in raw.split(",") if x.strip()]
            if not data:
                return

            n = len(data)
            mean_val = np.mean(data)
            median_val = np.median(data)
            std_dev = np.std(data, ddof=1) if n > 1 else 0.0
            variance = np.var(data, ddof=1) if n > 1 else 0.0
            min_val = np.min(data)
            max_val = np.max(data)
            sum_val = np.sum(data)

            self.results_text.delete("1.0", tk.END)
            output = (
                f"Count (N)         : {n}\n"
                f"Sum               : {sum_val:.4f}\n"
                f"Mean (Average)    : {mean_val:.4f}\n"
                f"Median            : {median_val:.4f}\n"
                f"Sample Std Dev    : {std_dev:.4f}\n"
                f"Sample Variance   : {variance:.4f}\n"
                f"Minimum           : {min_val:.4f}\n"
                f"Maximum           : {max_val:.4f}\n"
                f"Range             : {(max_val - min_val):.4f}\n"
            )
            self.results_text.insert(tk.END, output)
        except ValueError:
            messagebox.showerror("Input Error", "Please verify that all entries are comma-separated numbers.")

    def process_key(self, event):
        if event.keysym in ("Return", "KP_Enter"):
            self.calculate_stats()


# ==============================================================================
# TAB 6: GRAPH CALCULATOR (Matplotlib Integration)
# ==============================================================================
class GraphTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(fill="x")

        ttk.Label(control_frame, text="f(x) =", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.func_entry = ttk.Entry(control_frame, font=("Arial", 11), width=20)
        self.func_entry.pack(side="left", padx=5)
        self.func_entry.insert(0, "sin(x) * x")

        ttk.Label(control_frame, text="Range x:", font=("Arial", 10)).pack(side="left", padx=5)
        self.xmin_entry = ttk.Entry(control_frame, width=5)
        self.xmin_entry.insert(0, "-10")
        self.xmin_entry.pack(side="left")

        ttk.Label(control_frame, text="to").pack(side="left", padx=2)
        self.xmax_entry = ttk.Entry(control_frame, width=5)
        self.xmax_entry.insert(0, "10")
        self.xmax_entry.pack(side="left")

        plot_btn = tk.Button(control_frame, text="Plot", bg="#00ADB5", fg="white", font=("Arial", 10, "bold"), command=self.plot_graph)
        plot_btn.pack(side="left", padx=10)

        # Matplotlib Canvas Embed
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.plot_graph()

    def plot_graph(self):
        expr = self.func_entry.get().strip()
        try:
            xmin = float(self.xmin_entry.get())
            xmax = float(self.xmax_entry.get())
            if xmin >= xmax:
                messagebox.showerror("Range Error", "X min must be strictly less than X max.")
                return

            x = np.linspace(xmin, xmax, 1000)

            # Safe numpy-backed namespace
            safe_env = {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "sqrt": np.sqrt,
                "exp": np.exp,
                "log": np.log,
                "pi": np.pi,
                "e": np.e,
                "abs": np.abs,
            }

            y = eval(expr, {"__builtins__": None}, safe_env)

            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {expr}", color="#00ADB5", linewidth=2)
            self.ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
            self.ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
            self.ax.grid(True, linestyle=":", alpha=0.6)
            self.ax.set_title(f"Graph of y = {expr}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.legend()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Evaluation Error", f"Could not plot expression:\n{e}")

    def process_key(self, event):
        if event.keysym in ("Return", "KP_Enter"):
            self.plot_graph()


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = AdvancedCalculatorApp()
    app.mainloop()