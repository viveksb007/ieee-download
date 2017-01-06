from flask import Flask, request, jsonify
import json
import requests
import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = 'http://ieeexplore.ieee.org.sci-hub.io/document/'

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


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'author': 'Vivek Singh Bhadauria',
        'author_url': 'http://viveksb007.github.io/',
        'Description': 'This would give PDF download link for IEEE papers, its built on top of SCI-HUB, So a big thanks to those guys :D'
    })



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
