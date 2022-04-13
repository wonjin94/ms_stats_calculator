# https://docs.google.com/spreadsheets/d/1RcHI5aHA_wxME7psInB9HCt1oZOTTimgqRwuaq4tWH4/edit?usp=sharing


import pandas as pd
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import pickle
import cv2
import mspython
import numpy as np
from autocorrect import Speller


# cd onedrive/desktop/discord bot/oneeyebot


API_NAME= 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']



spreadsheet_id = '1RcHI5aHA_wxME7psInB9HCt1oZOTTimgqRwuaq4tWH4'
SAMPLE_RANGE_NAME='A2:A23'

# most of the codes are from the following website
# https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c
def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'MS-python-client.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')
    

    # get images files to be processed
    # imgages are stored in "equips" folder
    files = os.listdir("equips")
    
    ring_pend = { 2 : [0,1,0],
    4 : [0,1,2,3,0]
    }

    for i in files:
        print("reading " + i)

        # read image
        file_name = "equips/" + i
        im = cv2.imread(file_name,0)
                
        # enhance the image for better result
        im = cv2.resize(im, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        im = cv2.resize(im,(600,950))
        kernel = np.ones((1, 1), np.uint8)
        im = cv2.dilate(im, kernel, iterations=1)
        im = cv2.erode(im, kernel, iterations=1)
        im=cv2.threshold(cv2.GaussianBlur(im, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # perform ocr
        result = mspython.perform_ocr(im)

        print(result)
        
        # process text to extract info
        col,result = mspython.process_img_text(result)


        l = len(col)
        if l > 1:
            col = col[ring_pend[l][-1]]
            ring_pend[l][-1] += 1
        
        # asign coulum info to be stored in google sheet
        col_string = col+"5:"+col+"26"

        # put values on google sheet
        request = sheet.values().update(spreadsheetId = spreadsheet_id, range = col_string, valueInputOption = "USER_ENTERED", body = {"values":result}).execute()
        
        print(i + " done")
main()
