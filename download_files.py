import requests
import bs4
import glob
import os


def find_file_url(id):
    '''
    Accornding to the id which is a part of the url of the page 
    this function connects to the www.statistics.gr webpage and 
    returns the url of the file we want to download.
    '''

    res = requests.get(
        "https://www.statistics.gr/el/statistics/-/publication/STO04/"+id)

    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    results = soup.select(
        '#_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ table tr')

    # Every page has the urls in diffent order or format so every time we have to check
    # the text of the url to make sure that we would download the correct file.
    for result in results:
        if len(result.text) == 82 or len(result.text) == 86:
            url = result.find_all("a")[0].attrs["href"]
            return url


def save_file(path, url):
    '''
    Given the url of the file it downloads and stores it
    in the specified path.
    '''
    r = requests.get(url, allow_redirects=True)
    open(path, 'wb').write(r.content)


if __name__ == "__main__":

    print('Beginning of the program...')

    range_str = "2010-2014"
    years = range_str.split("-")

    # Deletes everything from the data folder
    files = glob.glob(
        'C:\\Users\\Ηλιάνα\\Desktop\\Current Projects\\Python Project\\data\\*')
    for f in files:
        os.remove(f)

    for year in range(int(years[0]), int(years[1])+1):

        id = str(year)+'-Q' + '4'

        url = find_file_url(id)
        if url != None:
            save_file(path='data\\'+str(year)+'.xls', url=url)
