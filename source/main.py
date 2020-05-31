from download_files import find_file_url, save_file
from excel_to_db import Database, add_countries, add_year_arrivals
from plot_data import plot_arrivals_by_mean_of_transport
from plot_data import plot_arrivals_by_country
from plot_data import plot_tourists_arrivals
import re
import glob
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~Taking input and checking its validity~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
range_str = input("Give the year range:")
matches = re.search('201[0-5]-201[0-5]', str(range_str))

while matches == None:
    print("\nThis range is invalid")
    print("The maximum available range is '2010-2015'\n")
    range_str = input("Give the year range:")
    matches = re.search('201[0-5]-201[0-5]', str(range_str))

years = range_str.split("-")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~Downloading the appropriate files from the statistics.gr website~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Deletes everything from the data folder or creates
if os.path.exists('data'):
    files = glob.glob('data\\*')
    for f in files:
        os.remove(f)
else:
    os.mkdir('data')

# We download the .xls for every year in the range

print("\nDownloading the xls files...\n")

for year in range(int(years[0]), int(years[1])+1):
    id = str(year)+'-Q' + '4'
    url = find_file_url(id)
    if url != None:
        save_file(path='data\\'+str(year)+'.xls', url=url)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~Reading the data and importing to the database~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

print("\nReading the data and importing it to the database...\n")

db = Database()
db.create_arrivals_table()
db.create_countries_table()

for year in range(int(years[0]), int(years[1])+1):
    add_year_arrivals(year, db)
    add_countries(year, db)


if os.path.exists('csv'):
    files = glob.glob('csv\\*')
    for f in files:
        os.remove(f)
else:
    os.mkdir('csv')


db.export_csv('touristsArrivals', 'csv\\touristsArrivals.csv')
db.export_csv('countries', 'csv\\countries.csv')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~Ploting the data~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

choice = 0

while choice != 4:
    print("~~~Plotting Menu~~~")
    print("1. Tourists Arrivals")
    print("2. Arrivals per Mean of Transport")
    print("3. Arrivals by Country")
    print("4. Exit")
    choice = input("Select: ")
    choice = int(choice)

    if choice == 1:
        plot_tourists_arrivals("csv\\touristsArrivals.csv")
    elif choice == 2:
        plot_arrivals_by_mean_of_transport("csv\\touristsArrivals.csv")
    elif choice == 3:

        plot_arrivals_by_country("csv\\countries.csv", years)
    elif choice != 4:
        print("Invalid input")

    print("\n")
