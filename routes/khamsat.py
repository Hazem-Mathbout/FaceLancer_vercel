import requests
import json
from flask import Blueprint, request, jsonify
from tasks.khamsat_tasks import scrapKhamsat

khamsat_blueprint = Blueprint('khamsat', __name__)

@khamsat_blueprint.route("/resKham", methods=["POST", "GET"])
def res_kham(requests_session=None, output=None):
    isFuncInternal = False
    if output == None:
        try:
            requests_session = requests.Session()
            output = request.get_json()
        except Exception as e:
            print("res_kham initial scrapping: ", e)
            pass
    else:
        isFuncInternal = True
    response = scrapKhamsat(output, requests_session, isFuncInternal)

    requests_session.close()

    if isFuncInternal:
        finalRes = json.dumps(response)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(response)
