from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request
import requests
import json
import certifi
from dateutil import parser
from config import ACCESS_TOKEN


#We Should return certain capabilities of the latest meeting as per individual teams requirement.
def get_user_details():
    # Step 1: Read the JSON File
    try:
        with open('meeting_qualities.json', 'r') as file:  # Update the path to your JSON file
            data = json.load(file)
            print("Data is printing",data) 
            participants_data = []   
    # Step 2: Extract Required Data
            for participant in data['items']: 
                participant_info = {
                    "webexUserEmail": participant.get("webexUserEmail"),
                    "joinTime": participant.get("joinTime"),
                    # Assuming 'videoIn' and 'audioIn' are lists with at least one item
                    "videoInSamplingInterval": participant["videoIn"][0].get("samplingInterval") if participant.get("videoIn") else None,
                    "audioInSamplingInterval": participant["audioIn"][0].get("samplingInterval") if participant.get("audioIn") else None
                }
                participants_data.append(participant_info)
                return jsonify(participants_data) 
    except FileNotFoundError:
        return jsonify({"error": "JSON file not found"}), 404
  
