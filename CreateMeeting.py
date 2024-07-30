from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request
import requests
import json
import certifi
from config import BASE_URL,BASE_URL2,headers
from dateutil import parser
# ACCESS_TOKEN = 'ZTJjMjc5ZTctZDg2My00MTEyLWExZjItMjk1OGFjYjllMzAxZmVhMzJjNmUtNzI5_P0A1_2402b330-da2a-4f60-bf8b-3cdd53f9f977'



#CREATING A NEW MEETING
def create_meeting():
    # headers = {
    #     'Authorization': f'Bearer {ACCESS_TOKEN}',
    #     'Content-Type': 'application/json'
    # }
    data = request.get_json()
    # Parse the start and end times
    start_time = datetime.strptime(data['start'], '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime(data['end'], '%Y-%m-%dT%H:%M:%S')
 
        # Subtract 5.30 hours
    adjusted_start_time = start_time - timedelta(hours=5, minutes=30)
    adjusted_end_time = end_time - timedelta(hours=5, minutes=30)
    print(adjusted_start_time, adjusted_end_time)
 
    # Replace the original start and end times with the adjusted ones
    data['start'] = adjusted_start_time.strftime('%Y-%m-%dT%H:%M:%S')
    data['end'] = adjusted_end_time.strftime('%Y-%m-%dT%H:%M:%S')
 
    response = requests.post(f'{BASE_URL}/meetings', headers=headers, data=json.dumps(data))
    response1 = response.json()
    if "errors" in response1:
        return jsonify({"error": response1["errors"][0]["description"]}), 400
    
    return jsonify({"message":"Meeting created"}),200   
    # data = {
    #     "title": request.json.get('title'),
    #     "start": request.json.get('start'),
    #     "end": request.json.get('end'),
    #     "invitees": request.json.get('invitees')
    # }
    # start_time = datetime.strptime(data['start'], '%Y-%m-%dT%H:%M:%S')
    # end_time = datetime.strptime(data['end'], '%Y-%m-%dT%H:%M:%S')

    # # Subtract 5.30 hours
    # adjusted_start_time = start_time - timedelta(hours=5, minutes=30)
    # adjusted_end_time = end_time - timedelta(hours=5, minutes=30)
    # print(adjusted_start_time, adjusted_end_time)
 
    # # Replace the original start and end times with the adjusted ones
    # data['start'] = adjusted_start_time.strftime('%Y-%m-%dT%H:%M:%S')
    # data['end'] = adjusted_end_time.strftime('%Y-%m-%dT%H:%M:%S')

    # # print("data",data)
    # response = requests.post(f'{BASE_URL}/meetings', headers=headers, json=data)
    # response1 = response.json()
    # print(response.json())
    # if response.status_code == 200:
    #     return jsonify({"message":"meeting created"}), 200
    # else:
    #     return jsonify({"error": "Failed to create meeting"}), response.status_code


#TO FETCH MEETING LIST
def meeting_list():
    # meeting_id = requests.args.get('meetingId')
    response = requests.get(f'{BASE_URL}/meetings?meetingType=meeting&hostEmail=team1user3@ameeahme-7xfd.wbx.ai', headers=headers)
    data=response.json()
    # print(data['items'][0]['id'])

    if "errors" in data:
        return jsonify({"error": data["errors"][0]["description"]}), response.status_code
    
    if response.status_code == 200:
        # Save the meeting list to a JSON file
        with open('meeting_list.json', 'w') as file:
            json.dump(response.json(), file)
            # Check if 'items' is not empty before trying to access its first item
            if data['items']:
                return data['items'][0]['id']
            else:
                return jsonify({"message": "No meetings found"}), response.status_code
    else:
        return jsonify({"error": "Failed to fetch meeting list"}), response.status_code


#TO FETCH LATEST MEETING QUALITY BY MEETING ID
def meeting_qualities():

    a=meeting_list()
    print("ml",a)

    # meeting_id = 'e7eb06a614ae4c7b8f36be35071b497b_I_599787452716125307'
    # https://analytics.webexapis.com/v1/meeting/qualities https://analytics.webexapis.com/v1/meeting/qualities
    response = requests.get(f'{BASE_URL2}?meetingId={a}', headers=headers, verify=False)
    data = response.json()
    
    if "errors" in data:
        return jsonify({"error": data["errors"][0]["description"]}), 400

    if response.status_code == 200:
        if data:
            # Save the meeting qualities to a JSON file
            with open('meeting_qualities.json', 'w') as file:
                json.dump(data, file)
                return jsonify({"message": "Meeting qualities saved to meeting_qualities.json"}), 200
        else:
                return jsonify({"message": "No meeting qualities found"}), response.status_code
    
    # if "errors" in response1:
    #     return jsonify({"error": response1["errors"]}), 400
    else:
        return jsonify({"error": "Failed to fetch meeting qualities"}), response.status_code