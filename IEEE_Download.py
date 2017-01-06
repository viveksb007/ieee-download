import re
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

BASE_URL = 'http://ieeexplore.ieee.org.sci-hub.io/document/'

DEMO_URL = ['http://ieeexplore.ieee.org/document/7804836/',
            'http://ieeexplore.ieee.org/document/7566745/',
            'http://ieeexplore.ieee.org/document/7514560/',
            'http://ieeexplore.ieee.org/document/7514630/',
            'http://ieeexplore.ieee.org/document/7805456/']

# CAN"T DOWNLOAD ALWAYS BECAUSE IN SOME PAPERS CAPTCHA APPEARS, SO LINK DIRECTLY, USERS WILL SOLVE CAPTCHA AND DOWNLOAD
def download_pdf(download_url, name):
    response_page = urlopen(download_url)
    pdf_file = open(name + ".pdf", "wb")
    pdf_file.write(response_page.read())
    pdf_file.close()


def get_download_url(paper_url):
    document_number = re.findall("[0-9]+", paper_url)
    REQUIRED_URL = BASE_URL + document_number[0] + '/'
    response = requests.get(REQUIRED_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("iframe", id="pdf"):
        download_link = str(link['src'])
        if download_link == '':
            print("Can't download this paper. Try later. Sorry :P")
            break
        if str(download_link).find('http') == -1:
            download_link = 'http:' + download_link
        print(download_link)


# download_pdf(download_link, document_number) can't download because captca is coming to solve


if __name__ == '__main__':
    get_download_url(input("Enter URL of paper you want to Download :\n "))
