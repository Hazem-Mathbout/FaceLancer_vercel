import requests
import json
from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

updateInfo_blueprint = Blueprint('updateInfo', __name__)

@updateInfo_blueprint.route("/updateInfo", methods=["POST", "GET"])
def updateInfo():
    requests_session = requests.Session()
    number_of_offers = None
    payload = json.loads(request.data, strict=False)
    url = str(payload["url"])
    basePage = requests_session.get(url, headers=HEADERS)
    soup = BeautifulSoup(basePage.text, "lxml")
    try:
        if url.__contains__("kafiil.com"):
            number_of_offers = soup.find(name='table', attrs={
                "class": "info-table"}).findAll('tr')[3].findAll('td')[1].text.strip()
            number_of_offers = f"التعليقات ({number_of_offers})"
        elif url.__contains__("khamsat.com"):
            number_of_offers = soup.findAll(name='div', attrs={
                "class": "card-header bg-white"})[1].find(name='h3').text.strip()
        elif url.__contains__("mostaql.com"):
            number_of_offers = soup.find('table', attrs={
                "class": "table table-borderless mrg--an text-meta"}).findAll('tr')[5].findAll('td')[1].text.strip()
            number_of_offers = f"التعليقات ({number_of_offers})"
    except Exception as exc:
        print(
            f"Exception occure when updated info in route /updateInfo, the error is: {exc}")
        pass
    print(number_of_offers)
    requests_session.close()
    return jsonify(number_of_offers)