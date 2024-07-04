import requests
import json
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import concurrent.futures

from tasks.khamsat_tasks import scrapKhamsat
from tasks.kafiil_tasks import scrapkafiil
from tasks.mostaql_tasks import scrapmostaql

notification_blueprint = Blueprint('notification', __name__)

@notification_blueprint.route("/notification", methods=["POST", "GET"])
def fetchNotifications():
    requests_session = requests.Session()
    allData = []
    final_Data_Notification = []
    payload = json.loads(request.data, strict=False)
    
    notif_hour = 6  # <-- override notif_hour the client option -->
    notif_min = 0  # <-- override notif_min the client option -->
    td_client = timedelta(hours=notif_hour, minutes=notif_min)
    
    websiteDisabled = payload['websiteDisabled']
    LISTSCRAPING = getListScrappingForNotification(websiteDisabled)

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_website = {executor.submit(website, payload, requests_session): website for website in LISTSCRAPING}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception in route /notification: %s' % (website, exc))
            else:
                if isinstance(data, list):
                    allData.extend(data)
                try:
                    output = json.loads(data)
                    if isinstance(output, list):
                        allData.extend(output)
                    else:
                        print("Warning: The loaded JSON data is not a list.")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    
    allData_without_allPostId = [item for item in allData if item.get('all_post_id') is None]
    
    for offer in allData_without_allPostId:
        date_now = datetime.utcnow()
        date_offer_string = offer['dateTime']
        date_time_offer_obj = datetime.strptime(date_offer_string, '%Y-%m-%d %H:%M:%S')
        td_all_info = date_now - date_time_offer_obj
        days = td_all_info.days
        hours, remainder = divmod(td_all_info.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        td_offer = timedelta(hours=hours, minutes=minutes)
        
        if td_client >= td_offer and days == 0:
            final_Data_Notification.append(offer)
    
    print(f"Number of offers in notification list: {len(final_Data_Notification)}")
    print(f"Websites blocked from notification: {websiteDisabled}")
    requests_session.close()
    return jsonify(final_Data_Notification)


def getListScrappingForNotification(listNotAllowed: str) -> list:
    listSCRAPING = [scrapKhamsat, scrapkafiil, scrapmostaql]
    if not listNotAllowed or listNotAllowed == ",":
        return listSCRAPING
    
    makeListNotAllowed = listNotAllowed.removesuffix(',').split(",")
    for element in makeListNotAllowed:
        if 'khamsat' in element:
            listSCRAPING.remove(scrapKhamsat)
        elif 'mostaql' in element:
            listSCRAPING.remove(scrapmostaql)
        elif 'kafiil' in element:
            listSCRAPING.remove(scrapkafiil)
    
    return listSCRAPING