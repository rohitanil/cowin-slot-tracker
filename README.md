# Cowin-Slot-Tracker
Tracker to check the covid vaccine slot availability in your district and send mobile notifications through Telegram.

## Requirements
Anaconda
  - For Anaconda: Refer [Anaconda](https://docs.anaconda.com/anaconda/install/) to set it locally based on your machine specification.If you are a Windows user and wants to setup Anaconda, follow this [WINDOWS INSTALLATION](https://www.youtube.com/watch?v=syijLJ3oQzU&ab_channel=AmitThinksAmitThinks), for MAC follow [MAC INSTALLATION](https://www.youtube.com/watch?v=V6ZAv7hBH6Y&ab_channel=JustUnderstandingData) and for LINUX [LINUX INSTALLATION](https://www.youtube.com/watch?v=WFswV4J2ZEs&ab_channel=BoostUpStation)

## How to use?
There are two parts to this system
1. Pinging the public COWIN API to get district wise data and checking for availability, every 15 minutes.
2. Relaying this information to the user's mobile via Telegram Bot.
    - Open Anaconda Power Shell Prompt as shown in the image below
      ![AnancondaPowershell](/images/anaconda_prompt.PNG)
    - Type in ```pip install telegram-send```
    - Type in ```telegram-send configure```
    - Then follow the steps mentioned here [Setting up Telegram Bot](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580) to create a telegram bot.[Only follow till Step 2]
    - Now, open Telegram App and type `@Get_Channel_User_Telegram_ID_Bot`, and go to the chat. Type something and this should help you get your `Telegram ID`, which is your chat id. Note that as well.
    - After successfully completing the above steps, update your settings.json and update your
      ```
      {
        "authToken": "1602################",
        "chatId" : "71############"",
      }
      ```

      and then you are good to go.

Once all the above requirements are met, do the following
1. Git clone this repository(if you are techie enough), otherwise download the repository by clicking on `Download ZIP` under `Code`.
2. Open Terminal and change your directory to the folder you have just cloned/ downloaded. (Remember to extract the .zip file if you have downloaded it)
3. Modify `settings.json` with your settings.   
4. Open Spyder which is an Python IDE and run `covin_slot_tracker.py` file.
   ![Spyder](/images/spyder.PNG)
5. In case you need help on how to run kindly watch this 3 minute video to understand how to navigate in the application [Spyder - Getting Stated](https://youtu.be/E2Dap5SfXkI)
6. If there is a slot available in the district id or pincode you have provided, you will receive an SMS on your phone.

#### Example Response
You can either use `pincode` or `districtId`.

Sample settings.json with `pincode`
```
{
  "pincode": "695013",
  "authToken": "1602################",
  "chatId" : "71############",
  "userAge": "45"
}
```

Sample settings.json with `districtId`
```
{
  "districtId": "391",
  "authToken": "1602################",
  "chatId" : "71############",
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
