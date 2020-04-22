import xlrd
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('testDatabase.db')
        self.c = self.conn.cursor()

    def create_year_table(self, year):
        self.c.execute("CREATE TABLE year"+year+"(\
                         Quarter INTEGER,\
                         By_Plane INTEGER,\
                         By_Train INTEGER,\
                         By_Ship INTEGER,\
                         By_Car INTEGER,\
                         Sum    INTEGER \
                                        ) ")

        self.conn.commit()

    def create_countries_table(self):
        pass


file_location = "data/2011.xls"
workbook = xlrd.open_workbook(file_location)

month_counter = 0
quarter = 1
by_plane_sum = 0
by_train_sum = 0
by_ship_sum = 0
by_car_sum = 0
general_quarter_sum = 0
for month in range(12):
    sheet = workbook.sheet_by_index(month)
    month_counter += 1

    pointer = ''
    counter = 0
    # We are looking for the row where the sums are stored
    while pointer != "ΓΕΝΙΚΟ ΣΥΝΟΛΟ":
        counter += 1
        pointer = sheet.cell_value(counter, 1)

    by_plane_sum += int(sheet.cell_value(counter, 2))
    by_train_sum += int(sheet.cell_value(counter, 3))
    by_ship_sum += int(sheet.cell_value(counter, 4))
    by_car_sum += int(sheet.cell_value(counter, 5))
    general_quarter_sum += int(sheet.cell_value(counter, 6))

    if month_counter == 3:
        print(by_plane_sum, by_train_sum, by_ship_sum, by_car_sum,
              general_quarter_sum, "quarter = "+str(quarter)+"\n\n")
        by_plane_sum = 0
        by_train_sum = 0
        by_ship_sum = 0
        general_quarter_sum = 0
        month_counter = 0
        quarter += 1
