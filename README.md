# Cowin-Slot-Tracker
Tracker to check the covid vaccine slot availability in your district and send mobile notifications through Telegram.

## Requirements
Telegram App account
Anaconda

## How to use?
There are two parts to this system
1. Pinging the public COWIN API to get district wise data and checking for availability, every 15 minutes.
2. Open Telegram App and type `@Get_Channel_User_Telegram_ID_Bot` or go to https://t.me/Get_Channel_User_Telegram_ID_Bot and type Hi in the chat
You should get something like
<img src="telegram_get_id.png"/>

Use your Telegram id and add it to setting.json file in Telegram_ID section
Eg:
{
  "districtId": "1",
  "Telegram_ID": "18353498",
  "userAge": "45"
}

3. Now, open the link http://t.me/CowinSlotTrackerBot and click on Start.
4. After successfully completing the above steps, install Anaconda using the link
https://docs.anaconda.com/anaconda/install/ depending on your operating system i.e Windows, Linux, MAC

5. Post installation of Anaconda, go to your start menu and search for Spyder application
<img src="spyder_logo.png"/>


Once all the above requirements are met, do the following
1. Git clone this repository(if you are techie enough), otherwise download the repository by clicking on `Download ZIP` under `Code`.
2. Open settings.json and put in your preference
Eg:
{
  "districtId": "1",
  "Telegram_ID": "18353498",
  "userAge": "45"
}

3. Open Spyder application
4. Go to the folder you downloaded and open the file covin_slot_tracker.py
5. Click on the run button <img src="spyder_run_button.png"/>
6. If there is a slot available in the district code you have provided, you will receive an message on Telegram on your phone.


#### Example Response
You can either use `pincode` or `districtId`.

Sample settings.json with `districtId`
```
{
  "districtId": "391",
  "authToken": "1602################",
  "chatId" : "71############"",
  "selfPhone": "+91#########",
  "userAge": "45"
}
```

Sample settings.json with `pincode`
```
{
  "pincode": "391",
  "authToken": "1602################",
  "chatId" : "71############"",
  "selfPhone": "+91#########",
  "userAge": "45"
}
```

Response
```
Slots Available at 16 places.
SAKUR RH 2, Samsherpur RH, NIRAMAY HOSPITAL, Rahata RH, Chichondi Patil RH, Sakur RH, WAMBORI RH 2,
Wambori RH, JAMKHED RH 2, Topkhana HP, Rajur RH, SHRIRAMPUR RH 2, CHICHONDI PATIL RH 2, TAKALI DHOKESHWAR RH 2,
RAJUR RH 2, SAMSHERPUR RH 2

Here 391 is the district id for Ahmednagar, Maharashtra
```

#### Sample District Codes in Kerala
- 301: Alappuzha
- 307: Ernakulam
- 306: Idukki
- 297: Kannur
- 295: Kasaragod
- 298: Kollam
- 304: Kottayam
- 305: Kozhikode
- 302: Malappuram
- 308: Palakkad
- 300: Pathanamthitta
- 296: Thiruvananthapuram
- 303: Thrissur
- 299: Wayanad

#### Other States
To find District ID for other states:

Got to [Cowin Portal](https://www.cowin.gov.in/home) in the browser
- Open Network tab in browser
- Search for vaccine availabilty in portal
- Check Network tab for requests
- Find district_id property value from the requests
