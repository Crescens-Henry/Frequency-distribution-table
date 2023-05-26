from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import PyE_tools as pye
from decimal import Decimal
import numpy


class TableFrecuency:
    def __init__(self, root):
        self.data = []
        dataToShow = []

        # Configuracion base de el Frame
        mainframe = ttk.Frame(root, padding="20 20 20 20")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Labels
        ttk.Label(mainframe, text="Number:", anchor="e").grid(
            column=1, row=1, sticky="E"
        )
        ttk.Label(mainframe, text="Results:", anchor="e").grid(
            column=1, row=3, sticky="E"
        )
        ttk.Label(mainframe, text="Data:", anchor="e").grid(column=2, row=1, sticky="e")
        ttk.Label(mainframe, text="Numero de clases =", anchor="e").grid(
            column=1, row=4, sticky="e"
        )
        ttk.Label(mainframe, text="Rango =", anchor="e").grid(
            column=1, row=5, sticky="e"
        )
        ttk.Label(mainframe, text="Amplitud =", anchor="e").grid(
            column=1, row=6, sticky="e"
        )
        ttk.Label(mainframe, text="Unidad de variacion =", anchor="e").grid(
            column=1, row=7, sticky="e"
        )
        ttk.Label(mainframe, text="Medidas de tendencia central", anchor="e").grid(
            column=1, row=9, sticky="e"
        )
        ttk.Label(mainframe, text="Moda=", anchor="e").grid(
            column=1, row=10, sticky="e"
        )
        ttk.Label(mainframe, text="Media aritemetica=", anchor="e").grid(
            column=1, row=11, sticky="e"
        )
        ttk.Label(mainframe, text="Mediana=", anchor="e").grid(
            column=1, row=12, sticky="e"
        )

        # Labels response
        global result
        self.result = StringVar()
        print(self.result)
        ttk.Label(mainframe, textvariable=self.result).grid(
            column=3, row=1, sticky=(W, E, N, S), columnspan=8
        )
        # Results the Calculate
        self.num_classes = StringVar()
        ttk.Label(mainframe, textvariable=self.num_classes).grid(
            column=2, row=4, sticky=(W, E, N, S)
        )
        self.range = StringVar()
        ttk.Label(mainframe, textvariable=self.range).grid(column=2, row=5, sticky="W")
        self.amplitude = StringVar()
        ttk.Label(mainframe, textvariable=self.amplitude).grid(
            column=2, row=6, sticky=(W, E, N, S)
        )
        self.unit_of_variation = StringVar()
        ttk.Label(mainframe, textvariable=self.unit_of_variation).grid(
            column=2, row=7, sticky="EW"
        )
        self.statistical_mode = StringVar()
        ttk.Label(mainframe, textvariable=self.statistical_mode).grid(
            column=2, row=10, sticky="EW"
        )
        self.arithmetic_average = StringVar()
        ttk.Label(mainframe, textvariable=self.arithmetic_average).grid(
            column=2, row=11, sticky="EW"
        )
        self.median = StringVar()
        ttk.Label(mainframe, textvariable=self.median).grid(
            column=2, row=12, sticky="EW"
        )
        # Inputs
        self.number = StringVar()
        self.number_entry = ttk.Entry(mainframe, width=10, textvariable=self.number)
        self.number_entry.grid(column=2, row=1, sticky=W)

        # Buttons
        ttk.Button(mainframe, text="Agregar", command=self.add_number).place(
            x=1420, y=730
        )
        ttk.Button(mainframe, text="Calcular", command=self.calculate).place(
            x=1300, y=730
        )
        ttk.Button(mainframe, text="Borrar todo", command=self.clear_data).place(
            x=1200, y=730
        )
        ttk.Button(mainframe, text="Corregir", command=self.delete_last_number).place(
            x=1100, y=730
        )
        #! Treeview widget
        columns = (
            "Clase",
            "Limite Inferior",
            "Limite Inferior exacto",
            "Limite Superior",
            "Limite Superior exacto",
            "Frecuencia",
            "marca de clase",
            "Frecuencia relativa en %",
            "Frecuencia acumulada",
            "Frecuencia absoluta",
            "Frecuencia complementaria",
        )
        self.treeview = ttk.Treeview(mainframe, columns=columns, show="headings")
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, minwidth=0, width=135)
        self.treeview.grid(column=1, row=8, columnspan=12, padx=5, pady=5, sticky="EW")

    def add_number(self):
        try:
            value = Decimal(self.number_entry.get())
            self.data.append(value)
            self.result.set(", ".join(str(x) for x in numpy.sort(self.data)))
            self.number_entry.delete(0, END)
            self.number_entry.focus()
            print(numpy.sort(self.data))  #! imprimimos en consola
        except Decimal.InvalidOperation:
            messagebox.showerror("Error", "Ingrese un número válido")

    def calculate(self):
        dataSorted = pye.numpy.sort(self.data)
        k = pye.klassesNumber(self.data)
        r = pye.dataRange(dataSorted)
        a = pye.dataAmplitudeByList(dataSorted, True)
        uv = pye.variationUnit(dataSorted)
        dataTable = pye.calculateFrecuencyByDataList(dataSorted, k, a, uv)
        arithmetic_average = round(
            pye.arithmetic_average(dataSorted, dataSorted[0], (dataSorted[0] + a - uv)),
            3,
        )
        statistical_mode = pye.statistical_mode(dataSorted)
        median = pye.median(dataSorted)
        self.num_classes.set(str(k))
        self.range.set(str(r))
        self.amplitude.set(str(a))
        self.unit_of_variation.set(str(uv))
        self.statistical_mode.set(str(statistical_mode))
        self.arithmetic_average.set(str(arithmetic_average))
        self.median.set(str(median))
        # Update treeview
        self.treeview.delete(*self.treeview.get_children())
        for row in dataTable:
            self.treeview.insert("", "end", values=row)

    def clear_data(self):
        self.data = []
        self.result.set("")

    def delete_last_number(self):
        if len(self.data) > 0:
            self.data.pop()
            self.result.set(self.data)
            self.number_entry.focus_set()


root = Tk()
TableFrecuency(root)

# Obtiene las dimensiones de la pantalla
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Establece las dimensiones de la ventana a las dimensiones de la pantalla
root.geometry(f"{width}x{height}+0+0")

root.mainloop()
