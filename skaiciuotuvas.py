import datetime
from tkinter import Tk, Label, Entry, Button, Listbox, Text, END, DoubleVar, Toplevel, Menu, messagebox
from baze import engine, Duomenubaze
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Session = sessionmaker(bind=engine)
session = Session()


def irasyti():
    try:
        iraso_data = datetime.date.today()
        baze = Duomenubaze(iraso_data, float(e1.get()), float(e2.get()), float(e3.get()), float(e4.get()))
        session.add(baze)
        session.commit()
    except ValueError:
        messagebox.showerror(title="Ispejimas", message="Galima įrašyti tik skaičius")

    e1.delete(0, END)
    e1.insert(END, 0.0)
    e2.delete(0, END)
    e2.insert(END, 0.0)
    e3.delete(0, END)
    e3.insert(END, 0.0)
    e4.delete(0, END)
    e4.insert(END, 0.0)
    e1.focus()


def pajamu_suma():
    pajamos = session.query(func.sum(Duomenubaze.dienos_pajamos)).filter(
        Duomenubaze.iraso_data.between('2021-01-01', '2021-12-31')).scalar()
    return pajamos


pajamos_suma = pajamu_suma()


def islaidu_suma():
    suma_islaidu_kurui = session.query(func.sum(Duomenubaze.islaidos_kurui)).filter(
        Duomenubaze.iraso_data.between('2021-01-01', '2021-12-31')).scalar()
    suma_kitos_islaidos = session.query(func.sum(Duomenubaze.kitos_islaidos)).filter(
        Duomenubaze.iraso_data.between('2021-01-01', '2021-12-31')).scalar()
    islaidos = suma_islaidu_kurui + suma_kitos_islaidos
    return islaidos


islaidos_suma = islaidu_suma()


def nuvaziuota_km():
    atstumas = session.query(func.sum(Duomenubaze.nuvaziuotas_atstumas)).filter(
        Duomenubaze.iraso_data.between('2021-01-01', '2021-12-31')).scalar()
    return atstumas


def skaiciuokle():
    pajamos = pajamos_suma
    islaidos = islaidos_suma
    try:
        procentas = float(e33.get())
    except ValueError:
        messagebox.showerror(title="Ispejimas",
                             message="Neteisingai įrasytas kaupiamasis procentas. Privalo būti 2.4 arba 3")

    if procentas == 2.4 or procentas == 3:
        if islaidos > pajamos:
            print("Nuostolingi metai")
        elif islaidos >= pajamos*0.3:
            pelnas = pajamos - islaidos
        else:
            pelnas = pajamos - pajamos*0.3

    vsdi = (pelnas - pelnas * 0.1) * 0.01 * (12.52 + procentas)
    psd = (pelnas - pelnas * 0.1) * 0.01 * 6.98
    gpm = pelnas * 0.01 * 15
    viso_uzdirbta = pelnas - vsdi - psd - gpm
    pranesimas1 = f"Valstybinio socialinio draudimo mokestis sudaro: {round(vsdi, 2)}"
    pranesimas2 = f"Privalomo sveikatos draudimo mokestis sudaro: {round(psd, 2)}"
    pranesimas3 = f"Gyventojų pajamų mokestis sudaro: {round(gpm, 2)}"
    pranesimas4 = f"Viso uždirbta: {round(viso_uzdirbta, 2)}"

    lb1 = Listbox(root)
    lb1.insert(END, pranesimas1, pranesimas2, pranesimas3, pranesimas4)
    lb1.grid(row=14, column=0, columnspan=3, padx=10, ipady=10, sticky="ew")


def naujas_langas():
    tekstas = open("mokejimo_info.txt", "r", encoding="utf-8")
    info = tekstas.read()
    popup = Toplevel(root)
    popup.geometry("450x400")
    tekstas = Text(popup,  font=("Arial", 10))
    tekstas.insert(END, info)
    tekstas.pack()


def uzdaryti():
    root.destroy()


root = Tk()
# root.geometry('640x360+300+100')
root.iconbitmap('tax2.ico')
root.title('Individualios veiklos mokesčių skaiciuoklė vairuotojamas a.k.a. "Ubwolbol"')

num1 = DoubleVar(0.0)
num2 = DoubleVar(0.0)
num3 = DoubleVar(0.0)
num4 = DoubleVar(0.0)

data = datetime.date.today().strftime("%d-%m-%Y")
dienos_data = Label(root, text=f'Šiandienos data: {data}', font=("Arial", 10))
dienos_data.grid(row=0, column=0, padx=10, sticky='sw')

l1 = Label(root, text='Įrašykite dienos pajamas: ')
l1.grid(row=1, column=0, padx=10, pady=10, sticky='sw')
l2 = Label(root, text='Įrašykite išlaidas kurui: ')
l2.grid(row=2, column=0, padx=10, pady=10, sticky='sw')
l3 = Label(root, text='Įrašykite nuvažiuotą atstumą: ')
l3.grid(row=3, column=0, padx=10, pady=10, sticky='sw')
l4 = Label(root, text='Kitos išlaidos: ')
l4.grid(row=4, column=0, padx=10, pady=10, sticky='sw')

e1 = Entry(root, width=24, font=('Arial', 10), text=num1)
e1.grid(row=1, column=2)
e2 = Entry(root, width=24, font=('Arial', 10), text=num2)
e2.grid(row=2, column=2)
e3 = Entry(root, width=24, font=('Arial', 10), text=num3)
e3.grid(row=3, column=2)
e4 = Entry(root, width=24, font=('Arial', 10), text=num4)
e4.grid(row=4, column=2)

b1 = Button(root, text='Irasyti', command=irasyti)
b1.grid(row=5, column=2, columnspan=1, padx=10, sticky="ew")

l11 = Label(root, text='Metinės pajamos yra')
l11.grid(row=8, column=0, padx=10, pady=10, sticky='sw')
l22 = Label(root, text='Metinės išlaidos yra')
l22.grid(row=9, column=0, padx=10, pady=10, sticky='sw')
l33 = Label(root, text='Ar kaupiate papildomai pensijai? 2.4 ar 3 procentai?')
l33.grid(row=10, column=0, padx=10, pady=10, sticky='sw')

e11 = Entry(root, width=24, font=('Arial', 10))
e11.insert(END, round(pajamu_suma(), 2))
e11.grid(row=8, column=2)
e22 = Entry(root, width=24, font=('Arial', 10))
e22.insert(END, round(islaidu_suma(), 2))
e22.grid(row=9, column=2)
e33 = Entry(root, width=24, font=('Arial', 10))
e33.grid(row=10, column=2)

b11 = Button(root, text='Apskaičiuoti metinius mokesčius', command=lambda: skaiciuokle())
b11.grid(row=12, column=2, padx=10)

meniu = Menu(root)
root.config(menu=meniu)
submeniu = Menu(meniu, tearoff=0)
meniu.add_cascade(label='Meniu', menu=submeniu)
submeniu.add_command(label='Informacija', command=naujas_langas)
submeniu.add_separator()
submeniu.add_command(label='Uždaryti', command=uzdaryti)

langas = Label(root)
langas.grid()

root.mainloop()
