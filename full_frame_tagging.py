from __future__ import division
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from pprint import pprint
import numpy as np
import cv2
import imutils
import requests
from requests.auth import HTTPBasicAuth
import pprint
import json
import csv

# API AUTH SETUP
tenant_id = "9mujenxvws3a"
crack_detect_application = "Ttf5p5Cx"
crack_bounding_output = "jc_crack_full_frame_output_3xe"
url_prefix = ('https://api.cogniac.io/1')
username = ('')
password = ('')

# TOKEN SETUP
tenant_data = {"tenant_id": tenant_id}
resp = requests.get(url_prefix + "/oauth/token", params=tenant_data,
                    auth=HTTPBasicAuth(username, password), timeout=8)
token = resp.json()
#print token
request_headers = {"Authorization": "Bearer %s" % token['access_token']}

# MEDIA GET REQUEST
request = requests.get(
    url_prefix + "/subjects/" + crack_bounding_output + "/media?probability_upper=1.0&probability_lower=0.9&consensus=True&limit=5",
    headers=request_headers)

# RESPONSE HANDLER
jsonResponse = request.json()
jsonData = jsonResponse['data']

# ITERATE THROUGH REQUIRED JSON VARS
for item in jsonData:
    # DISPLAY BASIC IMAGE STATISTICS
    print ("\n")
    mediaID = item['subject']['media_id']
    print ('Media ID:' + mediaID)
    fileName = item['media']['filename']
    print ('File Name:' + fileName)
    print ('Consensus:' + item['subject']['consensus'])
    # ROUND THE PROBABILITY RETURN
    probRnd = round(item['subject']['probability'], 3)
    print ('Probability:' + str(probRnd))
