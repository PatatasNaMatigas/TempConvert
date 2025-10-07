import tkinter as tk
import ctypes
from PIL import Image, ImageTk

class Calculator:

    CELSIUS = 0
    FAHRENHEIT = 1
    KELVIN = 2

    def __init__(self):
        self.mainWindow = None
        print("Calculator Initiated")

    def calculate(self, valuesTuple):
        temperature = valuesTuple[0]
        frm = valuesTuple[1]
        to = valuesTuple[2]

        result = 0
        match to:
            case self.CELSIUS:
                match frm:
                    case self.FAHRENHEIT:
                        result = (temperature - 32) * (5 / 9)
                    case self.KELVIN:
                        result = temperature - 273.15
                    case self.CELSIUS:
                        result = temperature
            case self.FAHRENHEIT:
                match frm:
                    case self.CELSIUS:
                        result = temperature * (9 / 5) + 32
                    case self.KELVIN:
                        result = (temperature - 273.15) * (9 / 5) + 32
                    case self.FAHRENHEIT:
                        result = temperature
            case self.KELVIN:
                match frm:
                    case self.CELSIUS:
                        result = temperature + 273.15
                    case self.FAHRENHEIT:
                        result = (temperature - 32) * (5 / 9) + 273.15
                    case self.KELVIN:
                        result = temperature
        return result

    def getColorTemp(self, temperature, tempUnit):
        tempInC = self.calculate((temperature, tempUnit, self.CELSIUS))
        if tempInC >= 50:
            return "#E5BF94", True
        elif tempInC >= 25:
            return "#E5BF94", False
        elif tempInC >= 10:
            return "#BAFFBA", False
        elif tempInC > 0:
            return "#BAF2FF", False
        elif tempInC <= 0:
            return "#BAF2FF", True
        return None

    def unitToChar(self, unit):
        if unit == self.CELSIUS:
            return "°C"
        elif unit == self.FAHRENHEIT:
            return "°F"
        elif unit == self.KELVIN:
            return "K"

    def start(self):
        if self.mainWindow is None:
            self.mainWindow = MainWindow(calculator)
            self.mainWindow.start()

class UserInterfaceUtils:

    def initFont(self):
        ctypes.windll.gdi32.AddFontResourceExW("res/fonts/Mono.ttf", 0x10, 0)

class MainWindow:

    # values -- SUPER CLUTCHHH wahahahaha nag pointer sa python 😆
    unitFrom = ctypes.c_int(0)
    unitFromPtr = ctypes.pointer(unitFrom)
    unitTo = ctypes.c_int(0)
    unitToPtr = ctypes.pointer(unitTo)

    def __init__(self, calculator):
        self.tempInput = None
        self.calculator = calculator
        window = tk.Tk()
        window.title("TempConvert Pro Max")
        window.geometry("300x210")
        window.resizable(False, False)
        window.config(
            bg = "#A57EFF"
        )
        self.window = window

    def createCanvas(self):
        canvas = tk.Canvas(
            self.window,
            width = 300,
            height = 210,
            bg = "#A57EFF",
            highlightthickness = 0
        )
        canvas.create_line(
            100, 65, 180, 65,
            fill = "#FFFFFF",
            width = 5
        )
        canvas.create_rectangle(
            0, 0, 300, 210,
            outline = "#000000",
            width = 10
        )
        canvas.create_text(
            60, 50,
            text = "Temp:",
            fill = "#FFFFFF",
            justify = "left",
            font = ("VCR OSD Mono", 20)
        )
        canvas.create_text(
            100, 105,
            text = "Convert:",
            fill = "#FFFFFF",
            justify = "left",
            font = ("VCR OSD Mono", 20)
        )
        canvas.pack()

    def createUnitSelector(self, x, y, varPtr):
        leftIcon = ImageTk.PhotoImage(Image.open("res/assets/left.png").resize((20, 20)))
        rightIcon = ImageTk.PhotoImage(Image.open("res/assets/right.png").resize((20, 20)))

        unit = tk.Label(
            self.window,
            bg = self.window["bg"],
            fg = "#FFFFFF",
            font = ("VCR OSD Mono", 22),
            bd = 0,
            text = "°C",
            highlightthickness = 0,
            justify = "center"
        )
        unit.place(
            x = x + 25,
            y = y
        )

        def updateVar(increment):
            if increment:
                varPtr.contents.value = varPtr.contents.value + 1 if varPtr.contents.value < 2 else 0
            else:
                varPtr.contents.value = varPtr.contents.value - 1 if varPtr.contents.value > 0 else 2

            if varPtr.contents.value == 0:
                unit.config(text = "°C")
            elif varPtr.contents.value == 1:
                unit.config(text = "°F")
            elif varPtr.contents.value == 2:
                unit.config(text = "K")

        leftButton = tk.Button(
            self.window,
            image = leftIcon,
            borderwidth = 0,
            highlightthickness = 0,
            background = self.window["bg"],
            activebackground = self.window["bg"],
            command = lambda: updateVar(True)
        )
        leftButton.image = leftIcon
        leftButton.place(
            x = x,
            y = y + 6
        )

        rightButton = tk.Button(
            self.window,
            image = rightIcon,
            borderwidth = 0,
            highlightthickness = 0,
            background = self.window["bg"],
            activebackground = self.window["bg"],
            command = lambda: updateVar(False)
        )
        rightButton.image = rightIcon
        rightButton.place(
            x = x + 65,
            y = y + 6
        )

    def createTempInput(self):

        def checkInput(newValue):
            if newValue == "":
                return True
            if newValue == "-":
                return True
            if newValue.lstrip("-").replace(".", "", 1).isdigit():
                if newValue.count(".") <= 1:
                    return True
            return False

        checkValidInputs = (self.window.register(checkInput), "%P")

        tempInput = tk.Entry(
            self.window,
            bg = self.window["bg"],
            fg = "#FFFFFF",
            font = ("VCR OSD Mono", 20),
            bd = 0,
            highlightthickness = 0,
            justify = "center",
            validate = "key",
            validatecommand = checkValidInputs
        )
        tempInput.place(
            x = 100,
            y = 35,
            w = 80,
            h = 30
        )
        self.tempInput = tempInput

    def createSolveButton(self):
        doneUp = ImageTk.PhotoImage(Image.open("res/assets/doneUp.png").resize((96, 48)))
        doneDown = ImageTk.PhotoImage(Image.open("res/assets/doneDown.png").resize((96, 48)))

        def calculate():
            if self.tempInput.get() == "":
                self.tempInput.delete(0, tk.END)
                self.tempInput.insert(0, "0")
            values = self.getValues()
            temp = values[0]
            frm = values[1]
            to = values[2]
            tempInC = round(self.calculator.calculate((temp, frm, self.calculator.CELSIUS)), 2)
            bg = self.calculator.getColorTemp(temp, frm)
            resultWindow = ResultWindow(
                temp = round(temp, 2),   # round original input
                result = round(self.calculator.calculate(values), 2),
                unitFrom = self.calculator.unitToChar(frm),
                unitTo = self.calculator.unitToChar(to),
                color = bg[0],
                vfx = bg[1],
                tempInC = tempInC        # <-- add this extra argument for clarity
            )

            resultWindow.start()

        done = tk.Button(
            self.window,
            image = doneUp,
            borderwidth = 0,
            highlightthickness = 0,
            background = self.window["bg"],
            activebackground = self.window["bg"],
            command = lambda: calculate()
        )
        done.image = doneUp
        done.bind("<Leave>", lambda e: done.config(image = doneUp))
        done.bind("<Enter>", lambda e: done.config(image = doneDown))
        done.place(
            x = 105,
            y = 150
        )

    def initComponents(self):
        self.createCanvas()
        self.createTempInput()
        self.createUnitSelector(190, 35, self.unitFromPtr)
        self.createUnitSelector(170, 90, self.unitToPtr)
        self.createSolveButton()

    def start(self):
        self.initComponents()
        self.window.mainloop()

    def getValues(self):
        return (
            float(self.tempInput.get()),
            self.unitFromPtr.contents.value,
            self.unitToPtr.contents.value
        )

class ResultWindow:

    def __init__(self, temp=0, result=0, unitFrom="°C", unitTo="°C", color="", vfx=False, tempInC=0):
        self.temp = temp
        self.tempInC = tempInC
        self.result = result
        self.unitFrom = unitFrom
        self.unitTo = unitTo
        self.vfx = vfx
        print(temp, unitFrom, unitTo, result, color, vfx)
        window = tk.Toplevel()
        window.title("TempConvert Pro Max")
        window.geometry("300x210")
        window.resizable(False, False)
        window.config(
            bg = color
        )
        self.window = window

    def createCanvas(self):

        def animate():
            frame = self.frames[self.frameIndex]
            self.frameIndex = (self.frameIndex + 1) % len(self.frames)
            self.canvas.itemconfig(self.imageItem, image = frame)
            self.window.after(80, animate)

        canvas = tk.Canvas(
            self.window,
            width = 300,
            height = 210,
            bg = self.window["bg"],
            highlightthickness = 0
        )

        self.canvas = canvas

        if self.vfx and self.tempInC >= 50:

            self.frames = [tk.PhotoImage(
                file = "res/assets/fire.gif",
                format = f"gif - {i}") for i in range(8)
            ]
            self.frameIndex = 0

            self.imageItem = self.canvas.create_image(
                150,
                150,
                anchor = "center",
                image = self.frames[0]
            )
            animate()
        elif self.vfx and self.tempInC < 50:
            self.frames = [tk.PhotoImage(
                file = "res/assets/snow.gif",
                format = f"gif - {i}") for i in range(8)
            ]
            self.frameIndex = 0

            self.imageItem = self.canvas.create_image(
                150, 110,
                anchor = "center",
                image = self.frames[0]
            )

            animate()

        canvas.create_rectangle(
            0, 0, 300, 210,
            outline = "#000000",
            width = 10
        )
        canvas.create_text(
            150, 40,
            width = 300,
            justify = "center",
            anchor="center",
            fill="#000000",
            text = f"{self.temp}{self.unitFrom}",
            font = ("VCR OSD Mono", 20)
        )
        canvas.create_text(
            150, 80,
            width = 300,
            justify = "center",
            anchor="center",
            fill="#000000",
            text = f"Converted to {self.unitTo} is",
            font = ("VCR OSD Mono", 18)
        )
        canvas.create_text(
            150, 120,
            width = 300,
            justify = "center",
            anchor = "center",
            fill = "#000000",
            text = f"{self.result}{self.unitTo}",
            font = ("VCR OSD Mono", 20)
        )

        self.canvas.pack()


    def createExitButton(self):
        doneUp = ImageTk.PhotoImage(Image.open("res/assets/doneUp.png").resize((96, 48)))
        doneDown = ImageTk.PhotoImage(Image.open("res/assets/doneDown.png").resize((96, 48)))

        def calculate():
            self.window.destroy()

        done = tk.Button(
            self.window,
            image = doneUp,
            borderwidth = 0,
            highlightthickness = 0,
            background = self.window["bg"],
            activebackground = self.window["bg"],
            command = lambda: calculate()
        )
        done.image = doneUp
        done.bind("<Leave>", lambda e: done.config(image = doneUp))
        done.bind("<Enter>", lambda e: done.config(image = doneDown))
        done.place(
            x = 105,
            y = 150
        )

    def initComponents(self):
        self.createCanvas()
        self.createExitButton()

    def start(self):
        self.initComponents()
        self.window.mainloop()

userInterfaceUtils = UserInterfaceUtils()
userInterfaceUtils.initFont()

calculator = Calculator()
calculator.start()