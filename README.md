# Cowin-Slot-Tracker
Tracker to check the covid vaccine slot availability in India and send mobile notifications through Twilio Messaging Service.

## Requirements
Docker must be installed in the local system. Refer [docker documentation](https://docs.docker.com/engine/install/) to set it locally based on your machine specification.
If you are a Windows user and wants to setup docker, follow this [video](
https://youtu.be/_9AWYlt86B8)

## How to use?
There are two parts to this system
1. Pinging the public COWIN API to get district wise data and checking for availability, every 15 minutes.
2. Relaying this information to the user's mobile via Twilio Messaging Service. For that, one must configure Twilio
    1. Sign up on [Twilio](https://www.twilio.com/) using your email id. After verifying your email log into the Twilio Dashboard. For this purpose, we will remain on free trial.
    2. Once you are in the dashboard, click **Get a trial phone number**.
    3. Under Project Info, you can find the **ACCOUNT SID**, **AUTH TOKEN** and **PHONE NUMBER** (Twilio Phone Number and not yours). Make a note of these numbers.
4. After successfully completing above steps, you are good to go.

Once all the above requirements are met, do the following
1. Git clone this repository(if you are techie enough), otherwise download the repository by clicking on **Download ZIP** under **Code**.
2. Open Terminal and change your directory to the folder you have just cloned/ downloaded. (Remember to extract the .zip file if you have downloaded it)
3. Make sure Docker Desktop is running.
4. Modify `settings.json` with your settings.   
5. Run `docker build -t covin --rm .`
6. Run `docker run -it --name covin-schedule --rm covin`
7. If there is a slot available in the district code you have provided, you will receive an SMS on your phone.

If you want to change settings, rebuild the image and run(Step 5)

#### Example Response
You can either use pincode or districtId.

Sample settings.json with districtId
```
{
  "districtId": "391",
  "authToken": "09cbfca2asdad5ae4fe991ac8858adca1b",
  "accountSID": "AC6b24b0sdasuef906ed07sdfasd4e8d",
  "twilioPhone": "+1xxxxxxxxx",
  "selfPhone": "+919xxxxxxxx",
  "userAge": "45"
}

```

Sample settings.json with pincode
```
{
  "pincode": "695013",
  "authToken": "09cbfca2asdad5ae4fe991ac8858adca1b",
  "accountSID": "AC6b24b0sdasuef906ed07sdfasd4e8d",
  "twilioPhone": "+1xxxxxxxxx",
  "selfPhone": "+919xxxxxxxx",
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
