import ctypes
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
import requests
import customtkinter as ctk


# Keep the fixed-size window from scaling up to fill the display.
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).parent
else:
    APP_DIR = Path(__file__).parent

RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))


def resource_path(relative_path):
    return RESOURCE_DIR / relative_path


FONT_FAMILY = "JetBrains Mono"


def load_custom_fonts():
    font_path = resource_path(Path("assets") / "JetBrainsMono-Bold.ttf")
    if sys.platform == "win32" and font_path.exists():
        try:
            ctypes.windll.gdi32.AddFontResourceExW(str(font_path), 0x10, 0)
        except Exception as e:
            print(f"Error loading custom font: {e}")


load_custom_fonts()


class Theme:
    BG_MAIN = "#0C0E22"
    BG_CARD = "#0F1028"
    BG_WIDGET = "#161840"
    BORDER = "#252560"
    TEXT = "#EAE8F6"
    TEXT_MUTED = "#9488CC"
    ACCENT = "#6448E4"
    ACCENT_HOVER = "#7860F8"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        scale = min(
            0.63,
            max(0.1, (screen_width - 40) / 1280),
            max(0.1, (screen_height - 80) / 800),
        )
        ctk.set_widget_scaling(scale)
        ctk.set_window_scaling(1.0)
        self.window_width = round(1280 * scale)
        self.window_height = round(800 * scale)
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        
        self.title("Converto")
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.minsize(self.window_width, self.window_height)
        self.maxsize(self.window_width, self.window_height)
        try:
            self.iconbitmap(str(resource_path("icon.ico")))
        except Exception:
            pass
        self.configure(fg_color=Theme.BG_MAIN)
        self.resizable(False, False)
        
        self.FONT_TITLE = (FONT_FAMILY, 56, "bold")
        self.FONT_SUBTITLE = (FONT_FAMILY, 32, "bold")
        self.FONT_RESULT = (FONT_FAMILY, 32, "bold")
        self.FONT_LABEL = (FONT_FAMILY, 40, "bold")
        self.FONT_COMBOBOX_LABEL = (FONT_FAMILY, 28, "bold")
        self.FONT_BUTTON = (FONT_FAMILY, 36, "bold")
        self.FONT_ENTRY = (FONT_FAMILY, 36, "bold")
        
        self.initialise_data()
        self._setup_widgets()

        self.combobox_unit.set("Length")
        self.on_unit_change()

    def initialise_data(self):
        self.categories = {
            "Currency": ["EUR", "USD", "GBP", "CHF", "JPY", "CAD", "AUD"],
            "Length": ["Meter(m)", "Millimeter(mm)", "Centimeter(cm)", "Kilometer(km)", "Foot(ft)", "Inch(in)", "Mile(mi)", "Yard(yd)"],
            "Mass": ["Gram(g)", "Kilogram(kg)", "Milligram(mg)", "Pound(lb)", "Ounce(oz)"],
            "Temperature": ["Celsius(°C)", "Fahrenheit(°F)", "Kelvin(K)"],
            "Volume": ["Liter(L)", "Milliliter(mL)", "Gallon(gal)", "Quart(qt)", "Pint(pt)"],
            "Area": ["Square Meter(m²)", "Square Millimeter(mm²)", "Square Centimeter(cm²)", "Square Kilometer(km²)", "Square Foot(ft²)", "Square Inch(in²)", "Square Mile(mi²)", "Square Yard(yd²)"],
            "Time": ["Second(s)", "Millisecond(ms)", "Minute(min)", "Hour(h)", "Day(d)", "Week(wk)", "Month(mo)", "Year(yr)", "Decade(dc)", "Century(c)", "Millennium(ml)"],
            "Digital Storage": ["Bit(b)", "Kilobit(kb)", "Megabit(Mb)", "Gigabit(Gb)", "Terabit(Tb)", "Petabit(Pb)", "Exabit(Eb)", "Zettabit(Zb)", "Yottabit(Yb)", "Byte(B)", "Kilobyte(KB)", "Megabyte(MB)", "Gigabyte(GB)", "Terabyte(TB)", "Petabyte(PB)", "Exabyte(EB)", "Zettabyte(ZB)", "Yottabyte(YB)"],
            "Data Rate": ["bps", "kbps", "Mbps", "Gbps", "Tbps", "Pbps", "Ebps", "Zbps", "Ybps"],
            "Pressure": ["Pa", "kPa", "MPa", "hPa", "mbar", "bar", "atm", "mmHg", "inHg"],
            "Power": ["Watt(W)", "Kilowatt(kW)", "Megawatt(MW)", "Gigawatt(GW)", "Terawatt(TW)", "Petawatt(PW)", "Exawatt(EW)", "Zettawatt(ZW)", "Yottawatt(YW)"],
            "Energy": ["Joule(J)", "Kilojoule(kJ)", "Megajoule(MJ)", "Gigajoule(GJ)", "Terajoule(TJ)", "Petajoule(PJ)", "Exajoule(EJ)", "Zettajoule(ZJ)", "Yottajoule(YJ)"],
            "Speed": ["km/h", "km/min", "km/s", "m/h", "m/min", "m/s", "mile/h", "mile/min", "mile/s"]
        }

        self.length_units = {
            "Meter(m)": 1.0, "Millimeter(mm)": 0.001, "Centimeter(cm)": 0.01,
            "Kilometer(km)": 1000.0, "Foot(ft)": 0.3048, "Inch(in)": 0.0254,
            "Mile(mi)": 1609.34, "Yard(yd)": 0.9144
        }
        self.mass_units = {
            "Gram(g)": 1.0, "Kilogram(kg)": 1000.0, "Milligram(mg)": 0.001,
            "Pound(lb)": 453.592, "Ounce(oz)": 28.3495
        }
        self.time_units = {
            "Second(s)": 1.0, "Millisecond(ms)": 0.001, "Minute(min)": 60.0,
            "Hour(h)": 3600.0, "Day(d)": 86400.0, "Week(wk)": 604800.0,
            "Month(mo)": 2592000.0, "Year(yr)": 31536000.0, "Decade(dc)": 315360000.0,
            "Century(c)": 3153600000.0, "Millennium(ml)": 31536000000.0
        }
        self.volume_units = {
            "Liter(L)": 1.0, "Milliliter(mL)": 0.001, "Gallon(gal)": 3.78541,
            "Quart(qt)": 0.946353, "Pint(pt)": 0.473176
        }
        self.area_units = {
            "Square Meter(m²)": 1.0, "Square Millimeter(mm²)": 0.000001, "Square Centimeter(cm²)": 0.0001,
            "Square Kilometer(km²)": 1000000.0, "Square Foot(ft²)": 0.092903, "Square Inch(in²)": 0.00064516,
            "Square Mile(mi²)": 2589990.0, "Square Yard(yd²)": 0.836127
        }
        self.data_transfer_units = {
            "bps": 1.0, "kbps": 1000.0, "Mbps": 1000000.0,
            "Gbps": 1000000000.0, "Tbps": 1000000000000.0,
            "Pbps": 1000000000000000.0, "Ebps": 1000000000000000000.0,
            "Zbps": 1e21, "Ybps": 1e24
        }
        self.speed_units = {
            "km/h": 1.0, "km/min": 60.0, "km/s": 3600.0,
            "m/h": 0.001, "m/min": 0.06, "m/s": 3.6,
            "mile/h": 1.60934, "mile/min": 96.5597, "mile/s": 5793.58
        }
        self.digital_storage_units = {
            "Bit(b)": 1.0, "Kilobit(kb)": 1000.0, "Megabit(Mb)": 1000000.0,
            "Gigabit(Gb)": 1000000000.0, "Terabit(Tb)": 1000000000000.0,
            "Petabit(Pb)": 1000000000000000.0, "Exabit(Eb)": 1000000000000000000.0,
            "Zettabit(Zb)": 1e21, "Yottabit(Yb)": 1e24,
            "Byte(B)": 8.0, "Kilobyte(KB)": 8000.0, "Megabyte(MB)": 8000000.0,
            "Gigabyte(GB)": 8000000000.0, "Terabyte(TB)": 8000000000000.0,
            "Petabyte(PB)": 8000000000000000.0, "Exabyte(EB)": 8000000000000000000.0,
            "Zettabyte(ZB)": 8e21, "Yottabyte(YB)": 8e24
        }
        self.energy_units = {
            "Joule(J)": 1.0, "Kilojoule(kJ)": 1000.0, "Megajoule(MJ)": 1000000.0,
            "Gigajoule(GJ)": 1000000000.0, "Terajoule(TJ)": 1000000000000.0,
            "Petajoule(PJ)": 1000000000000000.0, "Exajoule(EJ)": 1000000000000000000.0,
            "Zettajoule(ZJ)": 1e21, "Yottajoule(YJ)": 1e24
        }
        self.power_units = {
            "Watt(W)": 1.0, "Kilowatt(kW)": 1000.0, "Megawatt(MW)": 1000000.0,
            "Gigawatt(GW)": 1000000000.0, "Terawatt(TW)": 1000000000000.0,
            "Petawatt(PW)": 1000000000000000.0, "Exawatt(EW)": 1000000000000000000.0,
            "Zettawatt(ZW)": 1e21, "Yottawatt(YW)": 1e24
        }
        self.pressure_units = {
            "Pa": 1.0, "kPa": 1000.0, "MPa": 1000000.0,
            "hPa": 100.0, "mbar": 100.0, "bar": 100000.0,
            "atm": 101325.0, "mmHg": 133.322, "inHg": 3386.38867
        }

    def _setup_widgets(self):
        self.header = ctk.CTkLabel(self, text="Converto", text_color=Theme.TEXT, font=self.FONT_TITLE, fg_color="transparent")
        self.header.place(relx=0.5, y=50, anchor="center")

        self.secondary_header = ctk.CTkLabel(self, text="Unit Converter", text_color=Theme.TEXT_MUTED, font=self.FONT_SUBTITLE, fg_color="transparent")
        self.secondary_header.place(relx=0.5, y=95, anchor="center")

        self.main_frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, border_color=Theme.BORDER, border_width=1, corner_radius=12, width=600, height=530)
        self.main_frame.place(relx=0.5, y=200, anchor="n")

        self.label_unit = ctk.CTkLabel(self.main_frame, text="Unit", text_color=Theme.TEXT_MUTED, font=self.FONT_LABEL, anchor="w", fg_color="transparent")
        self.label_unit.place(x=40, y=40)

        self.label_from = ctk.CTkLabel(self.main_frame, text="From", text_color=Theme.TEXT_MUTED, font=self.FONT_LABEL, anchor="w", fg_color="transparent")
        self.label_from.place(x=40, y=100)

        self.label_to = ctk.CTkLabel(self.main_frame, text="To", text_color=Theme.TEXT_MUTED, font=self.FONT_LABEL, anchor="w", fg_color="transparent")
        self.label_to.place(x=40, y=160)

        self.label_value = ctk.CTkLabel(self.main_frame, text="Value", text_color=Theme.TEXT_MUTED, font=self.FONT_LABEL, anchor="w", fg_color="transparent")
        self.label_value.place(x=40, y=220)

        unit_values = ["Currency", "Length", "Mass", "Volume", "Temperature", "Energy", "Power", "Pressure", "Speed", "Digital Storage", "Data Rate"]

        self.combobox_unit = ctk.CTkComboBox(
            self.main_frame, values=unit_values, fg_color=Theme.BG_MAIN, border_color=Theme.BORDER, width=350, height=45,
            font=self.FONT_COMBOBOX_LABEL, button_color=Theme.ACCENT, button_hover_color=Theme.ACCENT_HOVER,
            dropdown_font=self.FONT_COMBOBOX_LABEL, text_color=Theme.TEXT, dropdown_fg_color=Theme.BG_MAIN,
            dropdown_hover_color=Theme.ACCENT, dropdown_text_color=Theme.TEXT, hover=True, command=self.on_unit_change
        ) 
        self.combobox_unit.place(x=210, y=40)

        self.combobox_from = ctk.CTkComboBox(
            self.main_frame, values=[], fg_color=Theme.BG_MAIN, border_color=Theme.BORDER, width=350, height=45,
            font=self.FONT_COMBOBOX_LABEL, button_color=Theme.ACCENT, button_hover_color=Theme.ACCENT_HOVER,
            dropdown_font=self.FONT_COMBOBOX_LABEL, text_color=Theme.TEXT, dropdown_fg_color=Theme.BG_MAIN,
            dropdown_hover_color=Theme.ACCENT, dropdown_text_color=Theme.TEXT, hover=True, state="readonly"
        ) 
        self.combobox_from.place(x=210, y=100)

        self.combobox_to = ctk.CTkComboBox(
            self.main_frame, values=[], fg_color=Theme.BG_MAIN, border_color=Theme.BORDER, width=350, height=45,
            font=self.FONT_COMBOBOX_LABEL, button_color=Theme.ACCENT, button_hover_color=Theme.ACCENT_HOVER,
            dropdown_font=self.FONT_COMBOBOX_LABEL, text_color=Theme.TEXT, dropdown_fg_color=Theme.BG_MAIN,
            dropdown_hover_color=Theme.ACCENT, dropdown_text_color=Theme.TEXT, hover=True, state="readonly"
        ) 
        self.combobox_to.place(x=210, y=160)

        self.entry_value = ctk.CTkEntry(
            self.main_frame, placeholder_text="Enter value...", fg_color=Theme.BG_WIDGET, border_color=Theme.BORDER,
            text_color=Theme.TEXT, corner_radius=8, font=self.FONT_ENTRY, width=350, height=50,
            border_width=1, placeholder_text_color=Theme.TEXT_MUTED
        )
        self.entry_value.place(x=210, y=220)

        self.button_convert = ctk.CTkButton(
            self.main_frame, text="Convert", fg_color=Theme.ACCENT, text_color=Theme.TEXT, corner_radius=12,
            hover_color=Theme.ACCENT_HOVER, font=self.FONT_BUTTON, anchor="center", width=520, height=60,
            command=self.perform_conversion
        )
        self.button_convert.place(x=40, y=285)

        self.frame_result = ctk.CTkFrame(self.main_frame, fg_color=Theme.BG_WIDGET, border_color=Theme.BORDER, border_width=1, corner_radius=12, width=520, height=150)
        self.frame_result.place(x=40, y=360)

        self.label_result = ctk.CTkLabel(self.frame_result, text="Result:", text_color=Theme.TEXT_MUTED, font=self.FONT_RESULT, anchor="w", fg_color="transparent")
        self.label_result.place(x=30, y=15)

        self.result = ctk.CTkLabel(self.frame_result, text="—", text_color=Theme.TEXT, font=self.FONT_RESULT, anchor="w", fg_color="transparent")
        self.result.place(x=30, y=65)

    def on_unit_change(self, category=None):
        category = category or self.combobox_unit.get()
        units = self.categories.get(category, [])
        
        self.combobox_from.configure(values=units)
        self.combobox_to.configure(values=units)
        
        if units:
            self.combobox_from.set(units[0])
            self.combobox_to.set(units[1] if len(units) > 1 else units[0])

    def perform_conversion(self):
        try:
            val_str = self.entry_value.get().strip()
            if not val_str:
                self.result.configure(text="Please enter a value")
                return
            amount = float(val_str)
        except ValueError:
            self.result.configure(text="Invalid number format")
            return

        category = self.combobox_unit.get()
        from_unit = self.combobox_from.get()
        to_unit = self.combobox_to.get()

        if from_unit == to_unit:
            self.show_output(amount)
            return


        if category == "Currency":
            try:
                currency_amount = Decimal(val_str)
            except InvalidOperation:
                self.result.configure(text="Invalid number format")
                return

            if not currency_amount.is_finite():
                self.result.configure(text="Invalid number format")
                return

            digit_count = len(currency_amount.normalize().as_tuple().digits)
            integer_digit_count = max(currency_amount.copy_abs().adjusted() + 1, 1)
            if max(digit_count, integer_digit_count) > 16:
                self.result.configure(text="Currency max: 16 digits")
                return

            try:
                res = self.convert_currency(currency_amount, from_unit, to_unit)
                self.show_output(res)
            except requests.ConnectionError:
                self.result.configure(text="No internet. Check Wi-Fi.")
            except requests.Timeout:
                self.result.configure(text="Currency request timed out")
            except requests.RequestException:
                self.result.configure(text="Currency API unavailable")
            except Exception:
                self.result.configure(text="Currency conversion failed")
            return

        if category == "Temperature":
            res = self.convert_temperature(amount, from_unit, to_unit)
            self.show_output(res)
            return

        unit_dictionary_map = {
            "Length": self.length_units,
            "Mass": self.mass_units,
            "Volume": self.volume_units,
            "Area": self.area_units,
            "Time": self.time_units,
            "Digital Storage": self.digital_storage_units,
            "Data Rate": self.data_transfer_units,
            "Pressure": self.pressure_units,
            "Power": self.power_units,
            "Energy": self.energy_units,
            "Speed": self.speed_units
        }

        unit_dict = unit_dictionary_map.get(category)
        if unit_dict and from_unit in unit_dict and to_unit in unit_dict:
            res = self.convert(amount, from_unit, to_unit, unit_dict)
            self.show_output(res)
        else:
            self.result.configure(text="Unsupported conversion")

    def convert(self, amount, from_unit, to_unit, unit_dict):
        return amount * (unit_dict[from_unit] / unit_dict[to_unit])

    def convert_currency(self, amount, from_currency, to_currency):
        url = f"https://api.frankfurter.app/latest?amount={format(amount, 'f')}&from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["rates"][to_currency]

    def convert_temperature(self, amount, from_unit, to_unit):
        def parse_symbol(unit):
            if "Celsius" in unit: return "C"
            if "Fahrenheit" in unit: return "F"
            if "Kelvin" in unit: return "K"
            return "C"

        from_temp, to_temp = parse_symbol(from_unit), parse_symbol(to_unit)
        if from_temp == to_temp:
            return amount

        # Convert to Celsius base
        if from_temp == "F":
            celsius = (amount - 32) * 5/9
        elif from_temp == "K":
            celsius = amount - 273.15
        else:
            celsius = amount

        # Convert from Celsius base to target
        if to_temp == "F":
            return (celsius * 9/5) + 32
        elif to_temp == "K":
            return celsius + 273.15
        return celsius

    def show_output(self, value):
        if value == 0:
            formatted = "0"
        elif abs(value) < 1e-4 or abs(value) > 1e9:
            formatted = f"{value:.4e}"
        else:
            formatted = f"{value:.4f}".rstrip('0').rstrip('.')
        self.result.configure(text=formatted)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()