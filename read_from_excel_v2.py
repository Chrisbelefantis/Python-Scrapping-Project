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
        pass

    def add_arrival_row(self, year, quarter, sums):
        try:

            self.c.execute("INSERT INTO touristsArrivals\
                            VALUES(?,?, ?, ?, ?, ?, ?)", (year, quarter, sums[0], sums[1], sums[2], sums[3], sums[4]))
            self.conn.commit()
        except sqlite3.DatabaseError as e:

            print("Error: %s" % (e.args))

    def export_csv(self, table_name, path):
        table = pandas.read_sql_query(
            'select * from '+table_name+'', self.conn)
        table.to_csv(path, index=False)

    def query(self, string):
        self.c.execute(string)
        return self.c.fetchall()


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


db = Database()
db.create_arrivals_table()

# Βάλε να βρίσκει ποιες χρονολογίες έχω στο data.
for year in range(2011, 2016):
    add_year_arrivals(year, db)


db.export_csv('touristsArrivals', 'touristsArrivals.csv')
