import json
import os
import sys

KEYS = ("districtId", "authToken", "accountSID", "twilioPhone", "selfPhone")


def verify_settings():
    try:
        with open(os.environ["settings_path"], 'r') as f:
            settings = json.load(f)
            values = [settings.get(key) for key in KEYS]
            return all(values)

    except (AssertionError, FileNotFoundError, json.decoder.JSONDecodeError):
        print("settings.json not configured")


if __name__ == "__main__":
    # Accept new settings if not configured or if argument passed is true
    if not verify_settings() or sys.argv[1] == "true":
        new_settings = {}
        for key in KEYS:
            new_settings[key] = input("Enter %s: " % key)
        with open(os.environ["settings_path"], 'w') as f:
            json.dump(new_settings, f)
