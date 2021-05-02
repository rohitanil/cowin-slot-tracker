#!/bin/bash
export settings_path="settings/settings.json"
python initial_setup.py "$1"
python covin_slot_tracker.py
