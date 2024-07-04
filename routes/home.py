import requests
import json
from flask import Blueprint, request, jsonify
import concurrent.futures
from tasks.khamsat_tasks import scrapKhamsat
from tasks.kafiil_tasks import scrapkafiil
from tasks.mostaql_tasks import scrapmostaql

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route("/home", methods=["POST", "GET"])
def offersForHome():
    requests_session = requests.Session()
    allData = []
    payload = json.loads(request.data, strict=False)
    LISTSCRAPING = [scrapKhamsat, scrapkafiil, scrapmostaql]
    NEW_LIST_SCRAPING = removeUnSpportWebSiteForSearching(
        LISTSCRAPING, payload)
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_website = {executor.submit(
            website, requests_session, payload): website for website in NEW_LIST_SCRAPING}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception in route /home: %s' %(website, exc))
            else:
                output = json.loads(data)
                allData.extend(output)
                # try :
                #     allData.sort(key=lambda x: x['dateTime'], reverse=True)
                # except:
                #     print("Key dateTime Not Found!")
    mapAllPostId = [item for item in allData if item.get(
        'all_post_id') != None]
    sortedAllData = [
        item for item in allData if item.get('all_post_id') == None]
    try:
        sortedAllData.sort(key=lambda x: x['dateTime'], reverse=True)
    except Exception as exc:
        print(f"Error occure when sorting offers home, error is:{exc}")
    sortedAllData.extend(mapAllPostId)
    print("number offers in home: ", len(sortedAllData))
    requests_session.close()
    return jsonify(sortedAllData)


def removeUnSpportWebSiteForSearching(list_website, payload):
    List_Not_Support_Searching = [scrapKhamsat]
    if (payload["budget_max"] != "" and payload["budget_max"] != "None" and payload["budget_max"] != "10000.0") or (payload["budget_min"] != "" and payload["budget_min"] != "None" and payload["budget_min"] != "25.0") or (payload["category_mostaql"] != "" and payload["category_mostaql"] != "None") or (payload["category_kafiil"] != "" and payload["category_kafiil"] != "None") or (payload["delivery_duration_for_kafiil"] != "" and payload["delivery_duration_for_kafiil"] != "None") or (payload["delivery_duration_for_mostaql"] != "" and payload["delivery_duration_for_mostaql"] != "None") or (payload["skills_for_mostaql"] != "" and payload["skills_for_mostaql"] != "None"):
        for website in list_website:
            for websiteNotSupportSearch in List_Not_Support_Searching:
                if websiteNotSupportSearch == website:
                    list_website.remove(websiteNotSupportSearch)
    return list_website