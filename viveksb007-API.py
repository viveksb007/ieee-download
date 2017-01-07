from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import requests
import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

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
        return download_link


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST', 'GET'])
def download():
    paper_url = request.form['inputURL']
    pdf_url = get_download_url(paper_url=paper_url)
    if str(pdf_url) == '':
        return redirect(url_for('notfound'))
    return render_template('download_pdf.html', pdf_url=pdf_url)


@app.route('/notfound')
def not_found():
    return render_template('not_found.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
