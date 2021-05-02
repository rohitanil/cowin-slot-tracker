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
4. Run `docker build -t covin --rm .`
5. Run `docker run -it --name covin-schedule --rm covin`
6. Run `python covin_slot_tracker.py <DISTRICT_ID> <TWILIO AUTH TOKEN> <TWILIO ACCOUNT SID> <TWILIO PHONE NUMBER> <YOUR PHONE NUMBER>` in the interactive shell. Make sure your phone number has the country code. eg: +919xxxxxxxx
7. If there is a slot available in the district code you have provided, you will receive an SMS on your phone.

#### Alternative Way

1. Create `settings.json` file similar to schema in `settings.example.json` and fill in your details.
2. Run `docker build -t covin --rm .`
3. Run `docker run -it --name covin-schedule --rm covin`
4. Run `python covin_slot_tracker.py`

#### Example Usage and Response
```
python covin_slot_tracker.py 391 09cbfca2asdad5ae4fe991ac8858adca1b AC6b24b0sdasuef906ed07sdfasd4e8d +1xxxxxxxxx +919xxxxxxxx

{"value1": "Slot Available: Rahata RH, Taharabad RH, Shevgaon RH, KARJAT SDH2, CHICHONDI PATIL RH 2, WAMBORI RH 2, Rajur RH, Chichondi Patil RH, SAKUR RH 2, Samsherpur RH, Khirwire PHC, SHEVGAON RH2, Wambori RH, PUNTAMBA RH 2, Jamkhed RH, SAMSHERPUR RH 2, RAHURI RH 2, Taklibhan PHC, Takali Dokeshwar RH, Chapadgaon(S) PHC, Dr Mane Hospital, JAMKHED RH 2, Bota PHC, Puntamba RH, Topkhana HP, GHODEGAON RH 2, Bodhegaon RH, TAKALI DHOKESHWAR RH 2, TAHRABAD RH 2, Sakur RH, Shendi PHC, BODHEGAON RH 2, RAJUR RH 2, LONI RH 2"}

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
