#creado por equipo NoCountry-c20
import tkinter as tk
import pandas as pd
from pandastable import Table, TableModel, config
import pandastable as pt


#def de boton cerrar
def close_win():
    win.destroy()
    

def close_win2():
    win.destroy()

#definicion de match
def search():
    table.show()
    mat.pack_forget()
    listbox.pack_forget()
    scrollbarlb.pack_forget()

#crear la ventana
win= tk.Tk()
win.wm_attributes('-fullscreen', True)
win.title('MatchIT')

#color de ventana
titulo = tk.Label(win, text ='MatchIT', fg = 'blue', font= 'Times 20').pack()

#creacion de dos frames
frame1=tk.Frame(win, padx=5, pady=20)
frame1.pack()
frame2=tk.Frame(win, padx=5, pady=20)
frame2.pack()

#creacion de menu de ciudades
var0=tk.StringVar(frame1)
var0.set('City')
opcionp=['All','Burlington','Montreal','Ontario','Toronto','Vancouver']
opcione=tk.OptionMenu(frame1, var0,*opcionp)
opcione.configure(width=15)
opcione.pack(side='top', padx=10, pady=5)
#opcione.grid(row=1, column=0)

#creacion de menu de opciones de empleos
var1=tk.StringVar(frame1)
var1.set('Data Analyst')
opcionj=['Data Analyst','Data Scients','Data Enginner']
opcion0=tk.OptionMenu(frame1, var1,*opcionj)
opcion0.configure(width=30)
opcion0.pack(side='top', padx=10, pady=5)
#opcione.grid(row=2, column=0)

#creacion de menu de experiencia
var2=tk.StringVar(frame1)
var2.set('Seniority')
opcionex=['Any','Junior','Senior']
opcion1=tk.OptionMenu(frame1, var2,*opcionex)
opcion1.configure(width=30)
opcion1.pack(side='top', padx=10, pady=5)

#creacion de menu Work Type
var3=tk.StringVar(frame1)
var3.set('Work Type')
opcionw=['Any','In-Person','Remote']
opcion2=tk.OptionMenu(frame1, var3,*opcionw)
opcion2.configure(width=30)
opcion2.pack(side='top', padx=10, pady=5)


# Crear un listbox
scrollbarlb=tk.Scrollbar(frame1,orient=tk.VERTICAL)
listbox = tk.Listbox(frame1, yscrollcommand=scrollbarlb.set, width=40, height=10, selectmode=tk.MULTIPLE)
scrollbarlb.config(command=listbox.yview)
scrollbarlb.pack(side=tk.RIGHT, fill=tk.Y)

#listbox.title(Habilidades)
listbox.pack()
 
# Inserting the listbox items
listbox.insert(1, "Sql")
listbox.insert(2, "Python")
listbox.insert(3, "Power BI")
listbox.insert(4, "Machine Learning")
listbox.insert(5, "Blockchain")



#boton de match
mat=tk.Button(win,text= "MATCH", command=search)
mat.pack(pady=10)


#boton de cerrar
end=tk.Button(win, text="EXIT", command=close_win)
end.pack(side='bottom', pady = 20)

#añadir la base de datos
data2=pd.read_csv(r"\datasets\Cleaned_Dataset.csv",header=0,delimiter=",",usecols=("Position",
                                        "City",
                                        "Seniority",
                                        "Work Type",
                                        #"Job Info",
                                        "Employer",
                                        "Skill"))
#print(data2)


data2 = data2[data2['City'] == 'Toronto']
data2 = data2[data2['Position'] == 'Data Analyst']
data2 = data2[data2['Seniority'] == 'ANY']
#data2 = data2[data2['Work Type'] == 'Remote']
#data2 = data2[data2['Skill'].str.contains('Jira')]

#print(data2)

#Label Resultados
titulo1 = tk.Label(win, text ='Resultados', fg = 'blue', font= 'Times 20').pack()

#imprimir los datos en la tabla
df=pd.DataFrame(data2)
print(df)
table = pt.Table(frame2, dataframe=df, showtoolbar=True, showstatusbar=True)

table.autoResizeColumns()
table.config()
table.editable = False





win.mainloop()