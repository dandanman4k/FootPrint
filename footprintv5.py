from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import themed_tk as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
import webbrowser

#---------------------------------------------------------------------------------------------------------------------------
import math
import sqlite3
import datetime
from datetime import date

from tkinter import *
from tkinter import ttk

conn=sqlite3.connect('data.sqlite')
c=conn.cursor()

prev_app=''


class APPLIANCE():
    def __init__(self,name,wattage):
        self.wattage=wattage
        self.name=name
    def calc_energy(self,time): #in minutes
        return round((float(self.wattage)*float(time)*60)*(1/3600000),3) #in KWh

class TRIP():
    def __init__(self,name,co2):
        self.name=name
        self.co2=co2 #CO2 per km
    def carbon_output(self,distance):
        return float(self.co2)*float(distance)*1000 #in g

class POWER_CARBON():
    def __init__(self,name,efficiency):
        self.name=name
        self.efficiency=efficiency #CO2 grams per kilowatt hour
    def carbon_output(self,energy): #in kwh
        return((round(float(energy)*float(self.efficiency),3))) #in grams





def lin_search(obj,list):
    for i in range(len(list)):
        if list[i].name==obj:
            return(i)

def trip_co2(car,distance):
    global totall
    global conn
    global prev_app
    totall+=(float(trips_list[lin_search(car,trips_list)].carbon_output(distance)))
    c.execute("""UPDATE Total
                SET val= """+str(totall)+";")
    conn.commit()
    score_calc()

    prev_action(str('You used a '+str(car)+' for '+str(distance)+' kilometers and that created '+str(round(trips_list[lin_search(car,trips_list)].carbon_output(distance),3))+' grams of carbon'))

    return (trips_list[lin_search(car,trips_list)].carbon_output(distance))

def prev_action(ins):
    c.execute("""INSERT INTO Track (Logs) 
                VALUES('"""+str(ins)+"""')""")
    conn.commit()
    set_prev()

def set_prev():
    global prev_app
    prev_app=[]
    c.execute("""SELECT Logs
            FROM Track """)
    tempval=c.fetchall()
    for i in range(len(tempval)):
        prev_app.append(tempval[i][0])

def reset():
    global totall
    global prev_app
    c.execute("""UPDATE Total
                SET val = 0 """)
    conn.commit()
    c.execute("""UPDATE Total
                SET Start = 1 """)
    conn.commit()

    c.execute("""DELETE FROM Track""")
    set_prev()

    totall=0

    cd = datetime.date.today()

    cd = str(cd)

    cdstr = ''

    for i in range(len(cd)):
        if cd[i] == '-':
            cdstr += ","
        else:
            cdstr += cd[i]

    c.execute("""UPDATE Total
                SET Time_Start = '""" + cdstr + """'""")
    conn.commit()
    numOfDays()
    score_calc()
    count_setup(0)



def app_co2(app,time):
    global totall
    global conn
    global prev_app
    global country

    totall+=(float(countries_list[lin_search(country,countries_list)].carbon_output(appliances_list[lin_search(app,appliances_list)].calc_energy(time))))
    c.execute("""UPDATE Total
                SET val ="""+str(totall)+";")
    conn.commit()
    score_calc()
    prev_action(str('You used the '+app+' for '+time+' minutes, this used '+str(round(appliances_list[lin_search(app,appliances_list)].calc_energy(time),3))+' kiloWatts of energy and created '+str(countries_list[lin_search(country,countries_list)].carbon_output(appliances_list[lin_search(app,appliances_list)].calc_energy(time)))+' grams of carbon'))
    return(countries_list[lin_search(country,countries_list)].carbon_output(appliances_list[lin_search(app,appliances_list)].calc_energy(time)))


countries_list=[]
appliances_list=[]
trips_list=[]
score=0
country=''

c.execute("""SELECT Country
            FROM Total""")
country=str(c.fetchall()[0][0])

cd=datetime.date.today()

cd=str(cd)

cdstr=''

for i in range(len(cd)):
    if cd[i]=='-':
        cdstr+=","
    else:
        cdstr+=cd[i]




c.execute("""SELECT Start 
        FROM Total""")
tempval=c.fetchall()

if str(tempval[0][0])=='0':
    c.execute("""UPDATE Total
                SET Start = 1 """)
    conn.commit()
    c.execute("""UPDATE Total
                SET Time_Start = '"""+cdstr+"""'""")
    conn.commit()


c.execute("""SELECT Time_Start 
        FROM Total""")
tempval=c.fetchall()[0][0]
tempval.split(",")

Start_Time = date(int(tempval.split(",")[0]),int(tempval.split(",")[1]),int(tempval.split(",")[2]),)
e = datetime.datetime.now()




c.execute("""SELECT *
            FROM Total""")
tempval=c.fetchall()
totall=float(tempval[0][0])

def numOfDays():
    global day_num
    global Start_Time
    date2 = date(e.year, e.month, e.day)
    day_num = str(int(1+float(str((date2 - Start_Time).days))))



def score_calc():
    global score
    global day_num
    global totall
    score = (1000/((float(totall)+1)/(float(day_num)))*float(day_num)**1.8)


c.execute("""SELECT *
            FROM Countries""")
tempval=c.fetchall()
for i in range(len(tempval)):
    countries_list.append(POWER_CARBON(tempval[i][0],tempval[i][1]))

c.execute("""SELECT *
          FROM appliances""")
tempval=c.fetchall()
for i in range(len(tempval)):
    appliances_list.append(APPLIANCE(tempval[i][0],tempval[i][1]))

c.execute("""SELECT *
          FROM Travel""")
tempval=c.fetchall()
for i in range(len(tempval)):
    trips_list.append(TRIP(tempval[i][0],tempval[i][1]))

numOfDays()
score_calc()



#-----------------------------------------------------------------------------------------------------------------------------------------------------------
def count_setup(var):
    def select(select_count):
        global country
        country=(select_count.get())



    startup=tk.ThemedTk()
    startup.title('country')
    startup.get_themes()
    startup.set_theme('equilux')
    startup.config(bg='#464646')
    startup.geometry('300x250')
    country_nams=['Australia', 'Brazil', 'Canda', 'China', 'Denmark', 'Germany', 'India', 'Ireland', 'Japan', 'Kenya', 'Mexico', 'Nigeria', 'Russia', 'Rwanda', 'South Africa', 'South Korea', 'Spain', 'Uganda', 'Ukraine', 'United Kingdom', 'United States']

    clicked= StringVar()
    clicked.set(country_nams[0])
    l1 = ttk.Label(startup, text='SELECT COUNTRY', font=50)
    l1.grid(row=0, column=0, columnspan=2)
    select_count= ttk.Combobox(startup, value=country_nams)
    select_count.grid(row=1, column=0, pady=10, padx=10)
    select_count.current(0)
    if var==1:
        enter=ttk.Button(startup, text="Enter", command=lambda:[select(select_count),startup.destroy()])
    else:
        enter = ttk.Button(startup, text="Enter",command=lambda: [select(select_count), startup.destroy(), openMainWindow()])
    enter.grid(row=1, column=1, pady=10, padx=10)

    startup.mainloop()

    c.execute("""UPDATE Total
                SET Country =  '"""+country+"""'""")
    conn.commit()

prev_app=[]
c.execute("""SELECT Logs 
            FROM Track""")
tempval=c.fetchall()
for i in range(len(tempval)):
    prev_app.append(tempval[i][0])

c.execute("""SELECT Country
        FROM Total """)
tempval=c.fetchall()[0][0]
if str(tempval)=='0':
    count_setup(1)

#---------------------------------------------------------------------------------------------------------------------------

cmb=''
durationslider=''
cmb1=''
durationslider1=''

#info page hyperlinks
recycleurl1 = 'https://www.thepapermillstore.com/paper/recycled-paper'
recycleurl2 = 'https://www.google.com/search?q=e+waste+recycling+near+me'
recycleurl3 = 'https://www.bbc.com/news/science_and_environment'
new = 1
def openweb1():
    webbrowser.open(recycleurl1,new=new)
def openweb2():
    webbrowser.open(recycleurl2,new=new)
def openweb3():
    webbrowser.open(recycleurl3, new=new)

def getTrip():
    global cmb
    global durationslider
    var1=cmb.get()
    var2=durationslider.get()
    trip_co2(str(var1),str(var2))

def getApp():
    global cmb1
    global durationslider1
    var1=cmb1.get()
    var2=durationslider1.get()
    app_co2(str(var1),str(var2))



def openMainWindow():
    global score
    global day_num
    mainWindow = Toplevel(root)
    mainWindow.attributes('-topmost', True)
    mainWindow.title('Footprint')
    mainWindow.config(bg='#464646')
    mainWindow.geometry('800x450')
    l1 = ttk.Label(mainWindow, text='HOME', font=50)
    l1.grid(row=0, pady=10)
    button = ttk.Button(mainWindow, text='New Trip', command=lambda:[openTripWindow(), mainWindow.destroy()])
    button.grid(row=1, column=0, padx=300, pady=10, columnspan=2)
    button = ttk.Button(mainWindow, text='Use Appliance', command=lambda:[openApplianceWindow(), mainWindow.destroy()])
    button.grid(row=2, column=0, padx=25, pady=10, columnspan=2)
    l1 = ttk.Label(mainWindow, text='Total Carbon Emissions (g): '+str(round(float(totall),3)))
    l1.grid(row=3, column=0, padx=325)
    l1 = ttk.Label(mainWindow, text='Score: '+str(round(float(score),3)))
    l1.grid(row=4, column=0, padx=325)
    l1 = ttk.Label(mainWindow, text='Days since initial use: '+str(int(float(day_num)-1)))
    l1.grid(row=5, column=0, padx=325)
    button = ttk.Button(mainWindow, text='History', command=lambda: [mainWindow.destroy(),openLogWindow()])
    button.grid(row=6, column=0, padx=25, pady=10, columnspan=2)
    button = ttk.Button(mainWindow, text='Recycling and Environmentalism', command=lambda:[openRecyclingWindow(), mainWindow.destroy()])
    button.grid(row=7, column=0, padx=25, pady=10, columnspan=2)
    button = ttk.Button(mainWindow, text='Change Country', command=lambda: [ mainWindow.destroy(),count_setup(0)])
    button.grid(row=8, column=0, padx=25, pady=10, columnspan=2)
    l1 = ttk.Label(mainWindow, text='Country: ' +str(country))
    l1.grid(row=9, column=0, padx=325)
    button = ttk.Button(mainWindow, text='Reset', command=lambda:[mainWindow.destroy(),reset()])
    button.grid(row=10, column=0, padx=25, pady=25, columnspan=2)

def openTripWindow():
    global cmb
    global durationslider
    tripWindow = Toplevel(root)
    tripWindow.attributes('-topmost', True)
    tripWindow.title('New Trip')
    tripWindow.config(bg='#464646')
    tripWindow.geometry('800x450')
    l1 = ttk.Label(tripWindow, text='TRIP', font=50)
    l1.grid(row=0, pady=10)
    #Combobox
    vehicle=['Taxi', 'Classic Bus', 'Eco Bus', 'Coach', 'National Train', 'Light Rail', 'Subway', 'Ferry On Foot', 'Ferry In Car', 'Small Diesel Car', 'Medium Diesel Car', 'Large Diesel Car', 'MediumHybrid Car', 'Large Hybrid Car', 'Medium LPG Car', 'LargeLPG Car', 'Medium CNG Car', 'Large CNG Car', 'Small Petrol Van', 'Large Petrol Van', 'Small Dielsel Van', 'Medium Dielsel Van', 'Large Dielsel Van', 'LPG Van', 'CNG Van', 'Small Petrol Car', 'Medium Petrol Car', 'Large Petrol Car']
    l1 = ttk.Label(tripWindow, text='Select mode of transport:')
    l1.grid(row=1, column=0, padx=325, pady=25)
    cmb = AutocompleteCombobox(tripWindow, completevalues=vehicle, width=20)
    cmb.grid(row=2, column=0, columnspan=2)
    cmb.current (0)
    #distance slider
    l1 = ttk.Label(tripWindow, text='Distance (Km):')
    l1.grid(row=3, column=0, pady=25)
    durationslider = Scale(tripWindow, from_=0, to=120, length=500, sliderrelief='flat', highlightthickness=0, background='#464646', fg='#a6a6a6', troughcolor='#a6a6a6', activebackground='#414141', orient=HORIZONTAL)
    durationslider.grid(row=4, column=0)
    #end action
    button = ttk.Button(tripWindow, text='Add Journey', command=lambda:[getTrip(), openMainWindow(), tripWindow.destroy()])
    button.grid(row=5, column=0, pady=25, columnspan=2)

def openApplianceWindow():
    global cmb1
    global durationslider1
    applianceWindow = Toplevel(root)
    applianceWindow.attributes('-topmost', True)
    applianceWindow.title('Use Appliance')
    applianceWindow.config(bg='#464646')
    applianceWindow.geometry('800x450')
    l1 = ttk.Label(applianceWindow, text='APPLIANCE', font=50)
    l1.grid(row=0, pady=10)
    appliance = ['Blender', 'Computer', 'Dishwasher', 'Hair dryer', 'Iron', 'Lamp', 'Micro Wave', 'Printer', 'Refrigerator', 'RiceCooker', 'Toaster', 'Tv', 'Washing Machine', 'Water Heater']
    l1 = ttk.Label(applianceWindow, text='Select appliance:')
    l1.grid(row=1, column=0, padx=325, pady=25)
    cmb1 = AutocompleteCombobox(applianceWindow, completevalues=appliance, width=20)
    cmb1.grid(row=2, column=0)
    cmb1.current(0)
    l1 = ttk.Label(applianceWindow, text='Duration (minutes):')
    l1.grid(row=3, column=0, pady=25)
    durationslider1 = Scale(applianceWindow, from_=0, to=120, length=500, sliderrelief='flat', highlightthickness=0, background='#464646', fg='#a6a6a6', troughcolor='#a6a6a6', activebackground='#414141', orient=HORIZONTAL)
    durationslider1.grid(row=4, column=0)
    button = ttk.Button(applianceWindow, text='add appliance', command=lambda:[getApp(),openMainWindow(), applianceWindow.destroy()])
    button.grid(row=5, column=0, pady=25)

def openLogWindow():
    global prev_app
    logWindow = Toplevel(root)
    logWindow.attributes('-topmost', True)
    logWindow.title('History')
    logWindow.config(bg='#464646')
    logWindow.geometry('800x450')
    l1 = ttk.Label(logWindow, text='HISTORY', font=50)
    l1.grid(row=0, pady=10, padx=325)
    for i in range(len(prev_app)):
        l1 = ttk.Label(logWindow, text=str(prev_app[i]))
        l1.grid(row=(i+1), column=0, padx=150)
    button = ttk.Button(logWindow, text='Home', command=lambda:[openMainWindow(), logWindow.destroy()])
    button.grid(row=0, column=0, padx=10, sticky='w')

def openRecyclingWindow():
    recyclingWindow = Toplevel(root)
    recyclingWindow.attributes('-topmost', True)
    recyclingWindow.title('Recycling')
    recyclingWindow.config(bg='#464646')
    recyclingWindow.geometry('800x450')
    l1 = ttk.Label(recyclingWindow, text='HOME', font=50)
    l1.grid(row=0, pady=10)
    l1 = ttk.Label(recyclingWindow, text='1. Reduce paper waste by using recycled paper and printing on both sides.')
    l1.grid(row=1, column=0, pady=5)
    button = ttk.Button(recyclingWindow, text='Buy recycled paper from PaperMill', command=openweb1)
    button.grid(row=2, column=0, pady=5)
    l1 = ttk.Label(recyclingWindow, text='2. Recycle old technology.')
    l1.grid(row=3, column=0, pady=5)
    button = ttk.Button(recyclingWindow, text='Find e-waste recyclers near you', command=openweb2)
    button.grid(row=4, column=0, pady=5)
    l1 = ttk.Label(recyclingWindow, text='3. Have recycling bins at home.')
    l1.grid(row=5, column=0, pady=5)
    l1 = ttk.Label(recyclingWindow, text='4. Use reusable shopping bags, water bottles, containers, etc.')
    l1.grid(row=6, column=0, pady=5)
    l1 = ttk.Label(recyclingWindow, text='5. Buy in bulk to reduce packaging waste and cost.')
    l1.grid(row=7, column=0, pady=5)
    l1 = ttk.Label(recyclingWindow, text='6. Go digital. Use emails instead of paper mail, and share files online instead of printing them.')
    l1.grid(row=8, column=0, pady=5, padx=175)
    l1 = ttk.Label(recyclingWindow, text='7. Be well informed about environmental issues.')
    l1.grid(row=9, column=0, pady=5)
    button = ttk.Button(recyclingWindow, text='Go to BBC Environmental', command=openweb3)
    button.grid(row=10, column=0, pady=5)
    button = ttk.Button(recyclingWindow, text='Home', command=lambda:[openMainWindow(), recyclingWindow.destroy()])
    button.grid(row=11, column=0, pady=25)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#window 1
root = tk.ThemedTk()
root.get_themes()
root.set_theme('equilux')
root.config(bg='#464646')
root.geometry('1x1')
openMainWindow()
root.mainloop()
