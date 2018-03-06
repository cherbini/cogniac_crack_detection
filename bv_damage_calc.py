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


# MIDPOINT FUNCTION
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# API AUTH SETUP
tenant_id = "9mujenxvws3a"
crack_detect_application = "77xqVBEj"
crack_bounding_output = "cracksbounding_4qr"
url_prefix = ('https://api.cogniac.io/1')
username = ('')
password = ('')

# TOKEN SETUP
tenant_data = {"tenant_id": tenant_id}
resp = requests.get(url_prefix + "/oauth/token", params=tenant_data,
                    auth=HTTPBasicAuth(username, password), timeout=8)
token = resp.json()
# print token
request_headers = {"Authorization": "Bearer %s" % token['access_token']}

# MEDIA GET REQUEST
request = requests.get(
    'https://api.cogniac.io/1/subjects/cracksbounding_4qr/media?probability_upper=1.0&probability_lower=0.9&consensus=True&limit=5',
    headers=request_headers)

# RESPONSE HANDLER
jsonResponse = request.json()
jsonData = jsonResponse['data']

# **TEST**PRINT ALL KEYS IN JSON
# for key in jsonData:
# pprint("Key:")
# pprint(key)

# OPEN A CSV FILE FOR RESULT EXPORT
download_dir = "crackDamageCSV.csv"
csv = open(download_dir, "w")

# WRITE CSV STRUCTURE
columnTitleRow = "mediaID, fileName, damageRatio\n"
csv.write(columnTitleRow)

# ITERATE THROUGH REQUIRED JSON VARS
for item in jsonData:
    # DISPLAY BASIC IMAGE STATISTICS
    #print '\n'
    mediaID = item['subject']['media_id']
    print 'Media ID:' + mediaID
    fileName = item['media']['filename']
    print 'File Name:' + fileName
    print 'File Type:' + item['media']['media_format']
    print 'Consensus:' + item['subject']['consensus']
    # ROUND THE PROBABILITY RETURN
    probRnd = round(item['subject']['probability'], 3)
    print 'Probability:' + str(probRnd)

    # DISPLAY AND SET IMAGE HEIGHT AND WIDTH
    print 'Image Height:' + str(item['media']['image_height'])
    img_height = item['media']['image_height']
    print 'Image Width:' + str(item['media']['image_width'])
    img_width = item['media']['image_width']

    # DIG INTO NEXT LEVEL BOX COORDINATE ITEMS
    box = item['subject']['app_data']
    n = 1
    pixelTotal = 0
    for coord in box:
        # print 'x0:' + str(coord['box']['x0'])
        x0 = coord['box']['x0']
        # print 'x1:' + str(coord['box']['x1'])
        x1 = coord['box']['x1']
        # print 'y0:' + str(coord['box']['y0'])
        y0 = coord['box']['y0']
        # print 'y1:' + str(coord['box']['y1'])
        y1 = coord['box']['y1']

    ###START TO SET UP IMAGE PROCESSING
    pixelsPerMetric = None
    if pixelsPerMetric is None:
        pixelsPerMetric = img_width / 40

    # SET CORNERS
    tl = y0, x0
    tr = y0, x1
    br = y1, x1
    bl = y1, x0

    # CALCULATE MIDPOINTS
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    # compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # compute the size of the object
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric
    area = dimA * dimB
    areaRnd = round((area), 2)

    # COMPUTE NUMBER OF DAMAGED PIXELS
    pixelsDamaged = dA * dB
    pixelTotal = pixelTotal + pixelsDamaged
    # print 'PixelTotal: ' + str(pixelTotal)

    print 'Area for box ' + str(n) + ': ' + str(areaRnd) + "ft/sq"
    n = n + 1

    # CALCULATE RATIO OF GOOD PIXELS TO "CRACKED" PIXELS
    ratioRnd = round(((pixelTotal) / (img_height * img_width)), 2)
    print 'Damage Ratio for Image:' + str(ratioRnd)

    # PRINT IMAGE DATA TO CSV
    row = str(mediaID) + "," + str(fileName) + "," + str(ratioRnd) + "\n"
    csv.write(row)

# UPDATE META TAGS
update_contents = {"meta_tags": ["test"]}
post_update = requests.post(url_prefix +
                            "/media/SJVACNYAJ24KZKLI4JYXE2FZ3GNN", params=update_contents,
                            headers=request_headers, timeout=8)
post_token = post_update.json()
# print post_tokrn

# OUTPUT META_TAG VARIABLE
meta_post = {"Post Meta Tag": "%s" % post_token['meta_tags']}
print meta_post

####BELOW THIS IS LEGACY!
# THIS IS THE NEXT PART OF OPENCV TO ITERATE THROUGH FOR EACH OF THE IMAGES ABOVE^^^^^^
# SET IMAGE SIZE
# xSize = 4000
# ySize = 3000

# SET PER PIXEL METRIC BASED ON ALTITUDE
# pixelsPerMetric = None

# if pixelsPerMetric is None:
# pixelsPerMetric = xSize / 40

# BOUNDING BOX PAYLOAD READ
# x0 = 543
# y0 = 0
# x1 = 2589
# y1 = 3000

# SET CORNERS
# tl = y0, x0
# tr = y0, x1
# br = y1, x1
# bl = y1, x0

# CALCULATE MIDPOINTS
# (tltrX, tltrY) = midpoint(tl, tr)
# (blbrX, blbrY) = midpoint(bl, br)
# (tlblX, tlblY) = midpoint(tl, bl)
# (trbrX, trbrY) = midpoint(tr, br)

# LOAD IMAGE
# img = cv2.imread('test_image.jpg')

# DRAW BOUNDING BOX
# cv2.rectangle(img,(int(x1),int(y0)),(int(x0),int(y1)),(0,255,0),3)

# DRAW MIDPOINTS
# cv2.line(img, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 0), 5)
# cv2.line(img, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 0), 5)

# compute the Euclidean distance between the midpoints
# dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
# dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

# compute the size of the object
# dimA = dA / pixelsPerMetric
# dimB = dB / pixelsPerMetric
# area = dimA * dimB

# draw the object sizes on the image
# cv2.putText(img, "{:.1f}ft".format(dimA),
# (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
# 10, (255, 255, 255), 3)
# cv2.putText(img, "{:.1f}ft".format(dimB),
# (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
# 10, (255, 255, 255), 3)
# cv2.putText(img, "{:.1f}ft/sq".format(area),
# (int(trbrX), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
# 10, (255, 255, 255), 3)

# DISPLAY IMAGE IN A WINDOW
# screen_res = 1280, 720
# scale_width = screen_res[0] / img.shape[1]
# scale_height = screen_res[1] / img.shape[0]
# scale = min(scale_width, scale_height)
# window_width = int(img.shape[1] * scale)
# window_height = int(img.shape[0] * scale)

# cv2.namedWindow('Crack_Area_Measurement', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Crack_Area_Measurement', window_width, window_height)

# WAIT FOR KEYSTROKE TO CLOSE WINDOW
# cv2.imshow('Crack_Area_Measurement',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
