from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import json

app = Flask(__name__)

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


# @app.route("/resKham", methods=["POST", "GET"])
# def scrapKhamsat(requests_session=None, output=None):
#     isFuncInternal = False
#     payloadForSearchTerm = ""
#     baseSoup = BeautifulSoup("", 'lxml')
#     ORIGN = f"https://khamsat.com"
#     URL = ORIGN + "/community/requests"
#     URL_LOAD_MORE = "https://khamsat.com/ajax/load_more/community/requests"
#     listResult = []
#     templistResult = []
#     try:
#         if output == None:
#             requests_session = requests.Session()
#             try:
#                 output = request.get_json()
#             except Exception as exc:
#                 pass
#                 print(
#                     f"generated an exception when convert to json in route /resKham =>: {exc}")
#         else:
#             isFuncInternal = True

#         num_page_khamsat = output["num_page_khamsat"]
#         offset = output["offset_khamsat"]
#         limit = 25 if output["limit"] > 25 else output["limit"]

#         if (num_page_khamsat > 1):
#             dataLoadMore = str(output["dataLoadMore"])
#             response = requests_session.post(
#                 URL_LOAD_MORE, headers=HEADERS, data=dataLoadMore.removesuffix('&'))
#             print("status code for load more khamsat request is: ",
#                   response.status_code)
#             if response.status_code == 200 or response.status_code == 201:
#                 body = response.json()
#                 htmlString = body["content"]
#                 baseSoup = BeautifulSoup(htmlString, "lxml")
#         else:
#             basePage = requests_session.get(URL, headers=HEADERS)
#             baseSoup = BeautifulSoup(basePage.text, "lxml")

#         results = baseSoup.findAll(name='tr', attrs={"class": "forum_post"})
#         results = results[offset: offset+limit]
#         print("results khasmat befor looping is: {results}")
#         if (len(results) != 0):
#             with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
#                 future_to_offer = {executor.submit(
#                     taskKahmsatScraping, offer): offer for offer in results}
#                 for future in concurrent.futures.as_completed(future_to_offer):
#                     offer = future_to_offer[future]
#                     try:
#                         data = future.result()
#                     except Exception as exc:
#                         print(
#                             '%r generated an exception in route /resKham: %s' % (offer, exc))
#                     else:
#                         if len(data) != 0:
#                             templistResult.append(data)

#                 future_to_Link_offer = {executor.submit(
#                     taskScrapLinksKhamsat, offer, requests_session): offer for offer in templistResult}
#                 for future in concurrent.futures.as_completed(future_to_Link_offer):
#                     offer = future_to_Link_offer[future]
#                     try:
#                         data = future.result()
#                     except Exception as exc:
#                         print(
#                             '%r generated an exception in route /resKham: %s' % (offer, exc))
#                     else:
#                         payloadForSearchTerm = payloadForSearchTerm + \
#                             data["postId"] + "&"
#                         listResult.append(data)
#         try:
#             listResult.sort(key=lambda x: x['dateTime'], reverse=True)
#         except Exception as exc:
#             print(f"Error occure when sorting offers khamsat, error is:{exc}")
#         listResult.append({"all_post_id": payloadForSearchTerm})
#         print(f"Number Offers in khamsat: {len(listResult)}")
#     except Exception as exc:
#         pass
#         print(f"This Exception When Connect To Khamsat error is : {exc}")
#     if isFuncInternal:
#         finalRes = json.dumps(listResult)
#         return (finalRes)
#     else:
#         requests_session.close()
#         return jsonify(listResult)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)
