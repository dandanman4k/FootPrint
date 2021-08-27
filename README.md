# FootPrint

Footprint is a carbon tracking app which helps the user reduce their CO2 emissions.

## installation

pip install ttkthemes, ttkwidgets, webbrowser

## usage

on startup, Country window opens. user selects their country and presses enter.

the Main window opens, containing the following buttons and functions:
New Trip (button)
	opens New Trip window
		takes user vehicle (from combobox) and trip distance (from slider)
		Add Journey button adds a string describing the trip to logs, adds carbon emmission from trip to total, recalculates score, closes Trip window
Use Applicance (button)
	opens Use Appliance window
		takes user appliance (from combobox) and use duration (from slider)
		Add Appliance button adds a string describing the appliance use to logs, adds carbon emission from trip to total, closes Appliance window
Total Carbon Emissions (text)
	displays total carbon emissions in grams
Score (text)
	displays user score
		this is a value inversely proportional to the average carbon output per day of a user, and increases logarithmically with the amount of time spent using the app
Days since initial use (text)
	displays number of days since setup/last restart
Log (button)
	opens Log window
		displays recent actions (trips and appliances)
		Home button closes Log window
Recycling and Environmentalism (button)
	opens Recycling window
		contains information and links to help users be more environmentally aware and lessen their carbon footprint, as well as stay up to date on enrionmental issues
Change Country (button)
	reopens Country window
Country (text)
	displays current country
Reset (button)
	reinitialises the database of the app and resets start date, total emissions, and log

##DateBase

data.sqlite this is a database file which contains:
	all the values for the carbon output per kWh for specific countries
	all the values for carbon output per km for specific vehicles
	the start date
	the score
	the total carbon output
	the log of previous actions
this data is all accessed in the python script using sqlite3 with commands in SQL