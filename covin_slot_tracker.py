#!/usr/bin/env python3
import datetime,time
import os

import requests,json
from twilio.rest import Client

def getDate():
    """
    Function to get the current date

    Returns
    -------
    date : String
        Current date in DD-MM-YYYY format

    """
    current_time = datetime.datetime.now()
    day = current_time.day
    month = current_time.month
    year = current_time.year
    date = "{dd}-{mm}-{yyyy}".format(dd=day,mm=month,yyyy=year)
    return date

def pingCOWIN(date,district_id):
    """
    Function to ping the COWIN API to get the latest district wise details

    Parameters
    ----------
    date : String
    district_id : String
    
    Returns
    -------
    json

    """
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}".format(district_id = district_id, date = date)
    response = requests.get(url)
    return json.loads(response.text)

def checkAvailability(payload):
    """
    Function to check availability in the hospitals from the json response from the public API

    Parameters
    ----------
    payload : JSON

    Returns
    -------
    available_centers_str : String
        Available hospitals
    unavailable_centers_str : String
        Unavailable hospitals

    """
    available_centers = set()
    unavailable_centers = set()
    available_centers_str = False
    unavailable_centers_str = False
    
    if('centers' in payload.keys()):
       length = len(payload['centers'])
       if(length>1):
            for i in range(length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(sessions_len):
                    if(payload['centers'][i]['sessions'][j]['available_capacity']>0):
                        available_centers.add(payload['centers'][i]['name'])
                    else:
                        unavailable_centers.add(payload['centers'][i]['name'])
            available_centers_str =  ", ".join(available_centers)
            unavailable_centers_str = ", ".join(unavailable_centers)
    
    return available_centers_str,unavailable_centers_str


if __name__=="__main__":
    with open(os.environ["settings_path"]) as f:
        settings = json.load(f)

    # Load from JSON file
    DISTRICT_ID = settings["districtId"]
    SECRET_TOKEN = settings["authToken"]
    ACCOUNT_SID = settings["accountSID"]
    TWILIO_PHONE_NUMBER = settings["twilioPhone"]
    CELL_PHONE_NUMBER = settings["selfPhone"]

    client = Client(ACCOUNT_SID, SECRET_TOKEN)

    while(True):
        date = getDate()
        data1 = pingCOWIN(date,DISTRICT_ID)
        available, unavailable = checkAvailability(data1)
        if available:
            msg_body = "Slots Available at "+available
            client.messages.create(from_=TWILIO_PHONE_NUMBER,
                       to=CELL_PHONE_NUMBER,
                       body= msg_body)
        else:
            print("No Available Centers")
        time.sleep(900)
