from dataclasses import replace
import json
from sre_constants import FAILURE, SUCCESS
import requests

from plate.plate_detection import plate_detection, CAM_ID


headers = {"Content-Type": "application/json; charset=utf-8"}
url = "http://qthcmute.ddns.net:81/vehicle/parking"



def post(body, box_id):
  body = json.loads(body)
  body['blockId'] = str(CAM_ID)
  body['slotId'] = box_id
  
  if body['type'] == "PARKING":
      resp = requests.patch(url, headers=headers, json=json.loads(str(body).replace("'", '"')))
      print(str(body).replace("'", '"'))
      return resp