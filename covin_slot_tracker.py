#!/usr/bin/env python3
import time
from datetime import timedelta, datetime
import os,sys
import requests,json

def getDate():
    """
    Function to get the next date => Today + 1 day

    Returns
    -------
    date : String
        Next date in DD-MM-YYYY format

    """
    tomorrow = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")
    return tomorrow


def pincodeToStateDistrictConverter(pincode):
    district = ''
    state = ''
    india_post_url = "https://api.postalpincode.in/pincode/{pin}".format(pin = pincode)
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
    state_id = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
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
    district_id = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{st}".format(st = st_id)
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

def sendTelegramMessage(TOKEN, CHAT_ID, MSG):
    """
    Function to send message to telegram bot

    Parameters
    ----------
    TOKEN : STRING
        Telegram secret token.
    CHAT_ID : STRING
        Telegram chat id of user/ group to which you want to send msg.
    MSG : TYPE
        Message sent to telegram.

    Returns
    -------
    None.

    """
    url = "https://api.telegram.org/bot{token}/sendMessage?".format(token = TOKEN)
    payload = url + "chat_id={chat_id}&text={msg}".format(chat_id = CHAT_ID, msg = MSG)
    status = json.loads((requests.get(payload)).text).get('ok')
    if(status == False):
        print("Message sending to telegram failed. Check Telegram ID or Telegram Token entered. Exiting!!!")
        sys.exit()


if __name__=="__main__":
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
    with open("settings.json") as f:
        settings = json.load(f)

    # Load from JSON file
    flag = False
    key_list = ["authToken","chatId","userAge"]
    if all(key in settings for key in key_list):
        SECRET_TOKEN = settings["authToken"]
        CHAT_ID = settings["chatId"]
        USER_AGE = int(settings["userAge"])
        
        
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
                    sendTelegramMessage(SECRET_TOKEN,CHAT_ID,msg_body)
                else:
                    print("No Available Centers")

                time.sleep(900)
        else:
            print("District id or pincode error. Check settings")
    else:
        print("Arguments Missing/Invalid. Check settings.json")
            
        
