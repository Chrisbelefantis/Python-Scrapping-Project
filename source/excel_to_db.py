import xlrd
import sqlite3
import pandas


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()

    def create_arrivals_table(self):
        self.c.execute("CREATE TABLE touristsArrivals(\
                         Year INTEGER,\
                         Quarter INTEGER,\
                         By_Plane INTEGER,\
                         By_Train INTEGER,\
                         By_Ship INTEGER,\
                         By_Car INTEGER,\
                         Sum    INTEGER \
                                        ) ")

        self.conn.commit()

    def create_countries_table(self):
        self.c.execute("CREATE TABLE countries(\
                         Name TEXT,\
                         Year INTEGER,\
                         Arrivals INTEGER\
                                        ) ")
        self.conn.commit()

    def add_arrival_row(self, year, quarter, sums):
        try:

            self.c.execute("INSERT INTO touristsArrivals\
                            VALUES(?,?, ?, ?, ?, ?, ?)", (year, quarter, sums[0], sums[1], sums[2], sums[3], sums[4]))
            self.conn.commit()
        except sqlite3.DatabaseError as e:

            print("Error: %s" % (e.args))

    def add_country_row(self, name, year, arrivals):
        try:

            self.c.execute("INSERT INTO countries\
                            VALUES(?,?, ?)", (name, year, arrivals))
            self.conn.commit()

        except sqlite3.DatabaseError as e:

            print("Error: %s" % (e.args))

    def export_csv(self, table_name, path):
        table = pandas.read_sql_query(
            'select * from '+table_name+'', self.conn)
        table.to_csv(path, index=False)


def add_year_arrivals(year, database):
    '''
    For the given year this function takes necessary information
    from the correct .xls file and stores it in the given database.
    It stores the arrivals for every quarter of the year as 
    the arrivals per mean of transort.
    '''

    file_location = "data/"+str(year)+".xls"
    workbook = xlrd.open_workbook(file_location)

    month_counter = 0
    quarter = 1
    sums = [0, 0, 0, 0, 0]
    for month in range(12):
        sheet = workbook.sheet_by_index(month)
        month_counter += 1

        pointer = ''
        counter = 0
        # We are looking for the row where the sums are stored
        while pointer != "ΓΕΝΙΚΟ ΣΥΝΟΛΟ":
            counter += 1
            pointer = sheet.cell_value(counter, 1)

        sums[0] += int(sheet.cell_value(counter, 2))
        sums[1] += int(sheet.cell_value(counter, 3))
        sums[2] += int(sheet.cell_value(counter, 4))
        sums[3] += int(sheet.cell_value(counter, 5))
        sums[4] += int(sheet.cell_value(counter, 6))

        if month_counter == 3:
            database.add_arrival_row(year, quarter, sums)
            sums = [0, 0, 0, 0, 0]
            month_counter = 0
            quarter += 1


def add_countries(year, db):

    file_location = "data/"+str(year)+".xls"
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(11)

    illegal_fields = ['', 'Μη προσδιορίσιμες χώρες ταξιδιωτών', 'Λοιπά Κράτη Ευρώπης',
                      'Λοιπά κράτη Ασίας', 'Λοιπά κράτη Αφρικής', 'Λοιπά κράτη Αμερικής', 'Λοιπά κράτη Ωκεανίας']

    counter = 0
    i = 0

    # We are placing the start index at the beggining of the
    # second table.
    while counter < 2:
        i += 1
        if sheet.cell_value(i, 6) == 'ΣΥΝΟΛΟ':
            counter += 1
    start_index = i+3

    pointer = ''
    index = start_index
    while pointer != 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ':

        current_value = sheet.cell_value(index, 6)
        current_country = sheet.cell_value(index, 1)

        # Adding this country to the database
        if current_country not in illegal_fields:
            db.add_country_row(current_country, year, int(current_value))

        index += 1
        pointer = sheet.cell_value(index, 1)


if __name__ == "__main__":
    db = Database()
    db.create_arrivals_table()
    db.create_countries_table()

    for year in range(2010, 2015):
        add_year_arrivals(year, db)
        add_countries(year, db)

    db.export_csv('touristsArrivals', 'touristsArrivals.csv')
    db.export_csv('countries', 'countries.csv')
