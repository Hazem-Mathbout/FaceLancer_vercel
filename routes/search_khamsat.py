import requests
import json
from flask import Blueprint, request, jsonify
from tasks.khamsat_tasks import scrapKhamsat

searchKhamsat_blueprint = Blueprint('searchKhamsat', __name__)

@searchKhamsat_blueprint.route("/searchKhamsat", methods=["POST", "GET"])
def searchKhamsat():
    requests_session = requests.Session()
    allData = []
    dataLoadMore = None
    total_num_page = 0
    try:
        output = request.get_json()
        dataLoadMore = "" if output["dataLoadMore"] == None else output["dataLoadMore"]
        total_num_page = output["total_num_page"]
        num_page_khamsat = 1
        offset = 0
        limit = 25
        payload_khamsat = {"dataLoadMore": dataLoadMore,
            "num_page_khamsat": num_page_khamsat, "offset_khamsat": offset, "limit": limit}
        for _ in range(total_num_page):
            data = scrapKhamsat(requests_session=requests_session, output=payload_khamsat)
            data_object = json.loads(data)
            lastElement = data_object.pop()
            num_page_khamsat = num_page_khamsat + 1
            payload_khamsat["dataLoadMore"] = payload_khamsat["dataLoadMore"] + \
                lastElement["all_post_id"]
            payload_khamsat["num_page_khamsat"] = num_page_khamsat
            allData.extend(data_object)
    except Exception as exc:
        print(f"generated an exception in searchKhamsat => : {exc}")
    print(f"========== Number of List Search is : {len(allData)}")
    requests_session.close()
    return jsonify(allData)