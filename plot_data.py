import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker


def plot_tourists_arrivals():
    '''
    This functions plots two graphs in the same 
    figure illustrating the tourists arrivals 
    per year and per quarter of the year.
    '''

    fig, (ax, ax2) = plt.subplots(nrows=2, ncols=1)

#~~~~~~~~~~~Ploting the tourists arrival per year~~~~~~~~~~~~~~~~~~~#
    df = pd.read_csv('touristsArrivals.csv')

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


plot_tourists_arrivals()
