import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker


def plot_tourists_arrivals(csv_path):
    '''
    This functions plots two graphs in the same 
    figure illustrating the tourists arrivals 
    per year and per quarter of the year.
    '''

    fig, (ax, ax2) = plt.subplots(nrows=2, ncols=1)

#~~~~~~~~~~~Ploting the tourists arrival per year~~~~~~~~~~~~~~~~~~~#
    df = pd.read_csv(csv_path)

    sums_per_year = df.groupby(['Year']).sum()
    years = sums_per_year.index.values
    tourists_arrivals = sums_per_year["Sum"]

    ax.plot(years, tourists_arrivals, marker='.')

    locator = matplotlib.ticker.MultipleLocator(1)
    ax.xaxis.set_major_locator(locator)

    formatter_x = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
    ax.xaxis.set_major_formatter(formatter_x)

    formatter_y = matplotlib.ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter_y)

    ax.set_xlabel('Year')
    ax.set_ylabel('Arrivals')
    ax.set_title('Tourists Arrivals per Year')

#~~~~~~~~~~~Ploting the tourists arrival per quarter of the year~~~~~~~~~~~~~~~~~~~#

    # We merge the year and the quarter column into one making the
    # appropriate arithmetic operations in order this variable
    # to be our x axis for the tourists arivvals by quarter of the year.
    years_quarter = df['Year'].astype(
        float) + df['Quarter'].astype(float).subtract(1).multiply(0.25)

    sums_per_quarter = df['Sum']

    ax2.plot(years_quarter, sums_per_quarter, marker='.')

    formatter_y = matplotlib.ticker.StrMethodFormatter('{x:,.0f}')
    ax2.yaxis.set_major_formatter(formatter_y)

    ax2.set_xlabel('Year')
    ax2.set_ylabel('Arrivals')
    ax2.set_title('Tourists Arrivals per Quarter of the Year')

#~~~~~~~~~~~~~~~~~~~~~Displaying~~~~~~~~~~~~~~~~~~~~~~~~~#
    plt.style.use('seaborn')
    plt.tight_layout()
    plt.show()


def plot_arrivals_by_country(csv_path):

    df = pd.read_csv(csv_path)
    df_grp = df.groupby(['Name']).sum()
    df_grp_sort = df_grp.sort_values(by=['Arrivals'], ascending=False)
    countries = df_grp_sort.index.values
    arrivals = df_grp_sort['Arrivals']

    fig, ax = plt.subplots()
    fig.set_size_inches(8.5, 5)
    ax.bar(countries[0:8], arrivals[0:8], width=0.5, align='center')

    ax.set_xlabel('Countries')
    ax.set_ylabel('Arrivals')
    ax.set_title('Arrivals by Country')

    formatter_y = matplotlib.ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter_y)

    plt.style.use('seaborn')
    plt.tight_layout()
    plt.show()


def plot_arrivals_by_mean_of_transport(csv_path):

    plt.style.use('seaborn')
    df = pd.read_csv(csv_path)
    df_grp = df.groupby(['Year']).sum()
    years = df_grp.index.values
    plain_arrivals = df_grp['By_Plane']
    train_arrivals = df_grp['By_Train']
    ship_arrivals = df_grp['By_Ship']
    car_arrivals = df_grp['By_Car']

    fig, ax = plt.subplots()
    fig.set_size_inches(8.5, 5)

    ax.plot(years, plain_arrivals, color='red', label='Plane Arrivals')
    ax.plot(years, ship_arrivals, color='blue', label='Ship Arrivals')
    ax.plot(years, train_arrivals, color='yellow', label='Train Arrivals')
    ax.plot(years, car_arrivals, color='green', label='Car Arrivals')

    locator = matplotlib.ticker.MultipleLocator(1)
    ax.xaxis.set_major_locator(locator)

    formatter_x = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
    ax.xaxis.set_major_formatter(formatter_x)

    formatter_y = matplotlib.ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter_y)

    ax.set_xlabel('Year')
    ax.set_ylabel('Arrivals')
    ax.set_title('Tourists Arrivals per Mean of Transport')

    plt.legend()
    plt.tight_layout()
    plt.show()


# plot_arrivals_by_mean_of_transport("touristsArrivals.csv")
# plot_tourists_arrivals("touristsArrivals.csv")
# plot_arrivals_by_country("countries.csv")
