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


def pincodeToStateDistrictConverter(pincode):
    """
    Function to convert user entered pincode to state and district
    using India Post Public API

    Parameters
    ----------
    pincode : String
        Pincode entered by user.

    Returns
    -------
    district : String
        District mapped to pincode.
    state : String
        State mapped to pincode.

    """
    
    district = ''
    state = ''
    india_post_url = "https://api.postalpincode.in/pincode/{pin}".format(pin = pincode)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    try:
        response = requests.get(india_post_url,headers=headers)
        parsed_response = json.loads(response.text)
        if(parsed_response[0]["Status"] == "Success"):
            district = parsed_response[0]['PostOffice'][0]['District']
            state = parsed_response[0]['PostOffice'][0]['State']
        return district,state
    except Exception as e:
        print(e)
    
def getStateID(state):
    """
    Function to get state id from state name derived by reverse engineering
    pincode

    Parameters
    ----------
    state : String
        State name.

    Returns
    -------
    state_id : String
        ID associated with that state name

    """
    
    state_id = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    try:
        response = requests.get(url,headers=headers)
        parsed_response = json.loads(response.text)
        state_length = len(parsed_response['states'])
        for idx in range(state_length):
            if((parsed_response['states'][idx]['state_name']).lower().replace(" ", "") == state.lower().replace(" ", "")):
                state_id = parsed_response['states'][idx]['state_id']
        return(state_id)
    except Exception as e:
        print(e)
    
    
def getDistrictID(st_id, lookout_district):
    """
    Function to get district id from state id and district name

    Parameters
    ----------
    st_id : String
        ID associated with a state.
    lookout_district : String
        District name for which we need the district id.

    Returns
    -------
    district_id : String
        ID associated with a district.

    """
    
    district_id = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{st}".format(st = st_id)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    try:
        response = requests.get(url,headers=headers)
        parsed_response = json.loads(response.text)
        district_length = len(parsed_response['districts'])
        for idx in range(district_length):
            if((parsed_response['districts'][idx]['district_name']).lower().replace(" ", "") == lookout_district.lower().replace(" ", "")):
                district_id = parsed_response['districts'][idx]['district_id']
        return (district_id)
    except Exception as e:
        print(e)


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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    response = requests.get(url,headers=headers)
    return json.loads(response.text)

def checkAvailability(payload, age):
    """
    Function to check availability in the hospitals based on
    user age from the json response from the public API

    Parameters
    ----------
    payload : JSON
    age: INT

    Returns
    -------
    available_centers_str : String
        Available hospitals
    total_available_centers : Integer
        Total available hospitals

    """
    available_centers = set()
    unavailable_centers = set()
    available_centers_str = False
    total_available_centers = 0
    
    if('centers' in payload.keys()):
       length = len(payload['centers'])
       if(length>1):
            for i in range(length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(sessions_len):
                    if((payload['centers'][i]['sessions'][j]['available_capacity']>0) and
                       (payload['centers'][i]['sessions'][j]['min_age_limit']<=age)):
                        available_centers.add(payload['centers'][i]['name'])
            available_centers_str =  ", ".join(available_centers)
            total_available_centers = len(available_centers)
    
    return available_centers_str,total_available_centers


if __name__=="__main__":
    with open("settings.json") as f:
        settings = json.load(f)

    # Load from JSON file
    flag = False
    key_list = ["authToken","accountSID","twilioPhone","selfPhone","userAge"]
    if all(key in settings for key in key_list):
        SECRET_TOKEN = settings["authToken"]
        ACCOUNT_SID = settings["accountSID"]
        TWILIO_PHONE_NUMBER = settings["twilioPhone"]
        CELL_PHONE_NUMBER = settings["selfPhone"]
        USER_AGE = int(settings["userAge"])
        
        client = Client(ACCOUNT_SID, SECRET_TOKEN)
        
        if("pincode" in settings.keys()):
            PINCODE = settings["pincode"]
            print("Pincode: ",PINCODE)
            dist, state = pincodeToStateDistrictConverter(PINCODE)
            if(state!="" and dist!=""):
                print("District: {d}\nState: {s}".format(d= dist,s=state))
                st_id = getStateID(state)
                print("State ID: ", st_id)
                if(st_id!=""):
                    DISTRICT_ID = getDistrictID(st_id,dist)
                    print("District ID: ", DISTRICT_ID)
                    flag = True
        
        elif("districtId" in settings.keys()):
            DISTRICT_ID = settings["districtId"]
            print("District ID: ", DISTRICT_ID)
            flag = True
        
        if(flag):
            while(True):
                date = getDate()
                data1 = pingCOWIN(date,DISTRICT_ID)
                available, total_centers = checkAvailability(data1,USER_AGE)
                if available:
                    msg_body = "Slots Available at {total} places.\n{available}".format(total = total_centers,available = available)
                    print(msg_body)
                    client.messages.create(from_=TWILIO_PHONE_NUMBER,
                               to=CELL_PHONE_NUMBER,
                               body= msg_body)
                else:
                    print("No Available Centers")

                time.sleep(900)
        else:
            print("District id or pincode error. Check settings")
    else:
        print("Arguments Missing/Invalid. Check settings.json")
            
        
