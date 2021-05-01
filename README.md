# cowin-slot-tracker
Tracker to check the covid vaccine slot availability in India and send mobile notifications through IFTTT

## Requirements
Docker must be installed in the local system. Refer [docker documentation](https://docs.docker.com/engine/install/) to set it locally based on your machine specification.

## How to use?
There are two parts to this system
1. Pinging the public COWIN API to get district wise data and checking for availability, every 15 minutes.
2. Relaying this information to the user's mobile via IFTTT app. For this, one must configure the IFTTT settings by following this. **DO AS MENTIONED IN THIS LINK**  [IFTTT setup](https://betterprogramming.pub/how-to-send-push-notifications-to-your-phone-from-any-script-6b70e34748f6)
3. After successfully completing step 2, you will get the SECRET IFTTT TOKEN

Once all the above requirements are met, do the following
1. Git clone this repository and cd into it.
2. Run `docker build -t cowin --rm .`
3. Run `docker run -it --name cowin-schedule --rm cowin`
4. Run `python covin_slot_tracker.py <DISTRICT ID> <SECRET IFTTT TOKEN> <MINIMUM AGE LIMIT (18 or 45)>` in the interactive shell

#### Example Usage and Response
```
python covin_slot_tracker.py 391 asdadkaskdajncaj

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
