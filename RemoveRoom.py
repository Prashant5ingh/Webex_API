import json
from webexteamssdk import WebexTeamsAPI
from flask import Flask, request, jsonify
import requests
from config import HEADERS,HEADERS_BOT,WEBEX_API_URL

def find_room_by_title(room_title):
    #Listing webex room details 

    url = f'{WEBEX_API_URL}/rooms'
    params = {'max': 100}
    response = requests.get(url, headers=HEADERS, params=params)

    data=response.json()
    if "errors" in data:
        return jsonify({"error": data["errors"][0]["description"]}), response.status_code
    
    rooms = response.json().get('items', [])
    print(rooms)
    if response.status_code == 200:
        # Save the room list to a JSON file
        print("going")
        with open('room_list.json', 'w') as file:
           json.dump(response.json().get('items', []), file)   
    else:
        return jsonify({"error": "Failed to fetch room list"}), response.status_code
    print("iiii")
    for room in rooms:
        print(room['title'])
        if room['title'] == room_title:
            print("iiiooooo")
            print("rt",room['title'])
            return rooms
    return None


def list_membership(room_id):
    url = f'{WEBEX_API_URL}/memberships?roomId={room_id}'
    # data = {'roomId': room_id, 'personEmail': person_email}
    response = requests.get(url, headers=HEADERS)
    data=response.json()
    if "errors" in data:
        return jsonify({"error": data["errors"][0]["description"]}), response.status_code
    
    room_members = response.json().get('items', [])
    # print("room list:",room_members)
    return room_members


def delete_room():
    try:
        url = f'{WEBEX_API_URL}/rooms'
        params = {'max': 100}
        response = requests.get(url, headers=HEADERS, params=params)

        data=response.json()
        if "errors" in data:
             return jsonify({"error": data["errors"][0]["description"]}), response.status_code
        
        data_rooms = response.json().get('items', [])
        #   print("Data is printing",data) 
          
        room_title = request.json.get("title")
        # room_ID = request.json.get('id')  # ID needed to add user to the specific room
        # print("retert",room_ID)
        user_emails=[request.json.get("personEmail")]

        all_rooms = data_rooms
        # print("all room",all_rooms)


        existing_rooms = [room for room in all_rooms if room['title'] == room_title]
        print("existing rooms",existing_rooms)
        if not existing_rooms:
            msg=f"Room '{room_title}' does not exist"
            return msg,400
        
        print("Coming")
        room_id = existing_rooms[0].get('id')
        
        #When room is not found
        if room_id is None:
            return jsonify({"message": "Room not found"}), 404


        room_memberships = list_membership(room_id)
        # Check if there are any memberships left in the room
        print(room_memberships[0].get('personEmail'))
        for i in room_memberships:
            print(i)
            if i['personEmail'] not in ["stock_update_bot@webex.bot","team1user3@ameeahme-7xfd.wbx.ai"]:

                   a=400
                   msg="Please remove all members before deleting the room"
                   return msg,a
    
       
                   
        # Get existing room members
        url = f'{WEBEX_API_URL}/rooms/{room_id}'
        response = requests.delete(url, headers=HEADERS_BOT)

        print("Updated")
        msg=f"Room Deleted '{room_title}'"
        a=200
        return msg,a       
 
 
    except Exception as e:
        return f"Message: {str(e)}"