import requests
import json
from flask import Blueprint, request, jsonify
from tasks.mostaql_tasks import scrapmostaql

mostaql_blueprint = Blueprint('mostaql', __name__)

@mostaql_blueprint.route("/resMost", methods=["POST", "GET"])
def res_Most(requests_session=None, output=None):
    isFuncInternal = False
    if output == None:
        try:
            requests_session = requests.Session()
            output = request.get_json()
        except Exception as e:
            print("res_Most initial scrapping: ", e)
            pass
    else:
        isFuncInternal = True
    response = scrapmostaql(output, requests_session, isFuncInternal)

    if isFuncInternal:
        finalRes = json.dumps(response)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(response)
