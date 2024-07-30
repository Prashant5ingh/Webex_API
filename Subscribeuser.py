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
    
    for room in rooms:
        if room['title'] == room_title:
            print("rt",room['title'])
            return None
    return rooms

def create_room(room_title):
    #Creating a room and adding bot when new room is created
    
    url = f'{WEBEX_API_URL}/rooms'
    data = {'title': room_title}

    # Check if 'roomTitle' exists in the request data
    if 'title' not in data:
        return jsonify({"error": "Missing 'roomTitle' in request data"}), 400
    
    response = requests.post(url, headers=HEADERS, json=data)
    # print("create data:",response.json())
    data1=response.json()
    if "errors" in data1:
        return jsonify({"error": data1["errors"][0]["description"]}), response.status_code
    
    return response.json()

def list_membership(room_id):
    url = f'{WEBEX_API_URL}/memberships?roomId={room_id}'
    # data = {'roomId': room_id, 'personEmail': person_email}
    response = requests.get(url, headers=HEADERS)

    data=response.json()
    if "errors" in data:
        return jsonify({"error": data["errors"][0]["description"]}), response.status_code
    # print("room list:",room_members)
    return response.json().get('items', [])


def add_bot_to_room(room_id, person_email):
    #Adding bot to the room

    url = f'{WEBEX_API_URL}/memberships'
    data = {'roomId': room_id, 'personEmail': person_email}
    response = requests.post(url, headers=HEADERS, json=data)

    data=response.json()
    if "errors" in data:
        return jsonify({"error": data["errors"][0]["description"]}), response.status_code

    return response.json()

def add_users_to_room():
    try:
        url = f'{WEBEX_API_URL}/rooms'
        params = {'max': 100}
        response = requests.get(url, headers=HEADERS, params=params)

        data1=response.json()
        if "errors" in data1:
             return jsonify({"error": data1["errors"][0]["description"]}), response.status_code
        
        data_rooms = response.json().get('items', [])

        #   print("Data is printing",data) 
          
        room_title = request.json.get("title")
        room_ID = request.json.get('id')  # ID needed to add user to the specific room
        print("rID from postman",room_ID)


        user_emails=[request.json.get("personEmail")]

        all_rooms = data_rooms
        # print("all room",all_rooms)
        existing_rooms = [room for room in all_rooms if room['title'] == room_title or room['id']==room_ID]
        print("existing rooms",existing_rooms)

        if not existing_rooms:
            msg=f"Room '{room_title}' does not exist"
            return msg,404
        
        print("Coming")
        room_id = existing_rooms[0].get('id')
        
        #When there is no room_id fetched
        if len(room_id)==0:
            return jsonify({"error": "room_id not fetched"}), 400
   
        # #When there is no user_email
        # if user_emails is None:
        #     return jsonify({"error": "User email not provided"}), 400

        print("room id",room_id)
        # Get existing room members

        room_memberships = list_membership(room_id)
        # print("mem list",room_memberships)
        existing_users = [membership['personEmail'] for membership in room_memberships]
        print("user",existing_users)
 
        print("user_emails",user_emails)
        # Add users to the room
        for email in user_emails:
            if email not in existing_users:
                print(email)
                print("Enter")

                url = f'{WEBEX_API_URL}/memberships'

                data = {'roomId': room_id,'personEmail':email} # bot will add the user in the new room
                data2=response = requests.post(url, headers=HEADERS_BOT, json=data)
                if "errors" in data2:
                    return jsonify({"error": data2["errors"][0]["description"]}), response.status_code
                # data2 = {'roomId':room_ID,'personEmail':email}  # bot add user to specific room
                # response = requests.post(url, headers=HEADERS_BOT, json=data2)

                existing_users.append(email)
                print("Updated")
                msg=f"Users added to room '{room_title}': {', '.join(user_emails)}"
            else:
                print("not added")
                msg="User Already present!! You can't add to RoomSpace..."
        return msg
 
 
    except Exception as e:
        return f"Message: {str(e)}"



#10.82.101.97  --> linux ip