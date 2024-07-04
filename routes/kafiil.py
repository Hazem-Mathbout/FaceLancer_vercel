import requests
import json
from flask import Blueprint, request, jsonify
from tasks.kafiil_tasks import scrapkafiil

kafiil_blueprint = Blueprint('kafiil', __name__)

@kafiil_blueprint.route("/resKafi", methods=["POST", "GET"])
def res_Kafi(requests_session=None, output=None):
    isFuncInternal = False
    if output == None:
        try:
            requests_session = requests.Session()
            output = request.get_json()
        except Exception as e:
            print("res_Kafi initial scrapping: ", e)
            pass
    else:
        isFuncInternal = True
    response = scrapkafiil(output=output, requests_session=requests_session)

    if isFuncInternal:
        finalRes = json.dumps(response)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(response)
