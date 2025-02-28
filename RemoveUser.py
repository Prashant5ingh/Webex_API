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


# try:  
#         # https://webexapis.com/v1/memberships/{membershipId}
#         url = f'{WEBEX_API_URL}/rooms'
#         params = {'max': 100}
#         response = requests.get(url, headers=HEADERS, params=params)
#         data_rooms = response.json().get('items', [])
#         #   print("Data is printing",data) 
          
#         room_title = request.json.get("title")
#         room_ID = request.json.get('id')  # ID needed to add user to the specific room
#         print("retert",room_ID)
#         user_emails=[request.json.get("personEmail")]

#         all_rooms = data_rooms
#         # print("all room",all_rooms)
#         existing_rooms = [room for room in all_rooms if room['title'] == room_title or room['id']==room_ID]
#         print("existing rooms",existing_rooms)
#         if not existing_rooms:
#             msg=f"Room '{room_title}' does not exist"
#             return msg
#         print("Coming")
#         room_id = existing_rooms[0].get('id')
#         print("room id",room_id)
#         # Get existing room members

#         room_memberships = list_membership(room_id)
#         # print("mem list",room_memberships)
#         existing_users = [membership['personEmail'] for membership in room_memberships]
#         print("user",existing_users)
 
#         print("user_emails",user_emails)
#         # Add users to the room
#         for email in user_emails:
#             if email not in existing_users:
#                 print(email)
#                 print("Enter")
#                 # bot_api.memberships.create(room_id, personEmail=email)
#                 # if existing_rooms[0].get('id')==room_id:

#                 url = f'{WEBEX_API_URL}/memberships'

#                 data = {'roomId': room_id,'personEmail':email} # bot will add the user in the new room
#                 response = requests.post(url, headers=HEADERS_BOT, json=data)
                
#                 data2 = {'roomId':room_ID,'personEmail':email}  # bot add user to specific room
#                 response = requests.post(url, headers=HEADERS_BOT, json=data2)

#                 existing_users.append(email)
#                 print("Updated")
#                 msg=f"Users added to room '{room_title}': {', '.join(user_emails)}"
#             else:
#                 print("not added")
#                 msg="User Already present!! You can't add to RoomSpace..."
#         return msg
 
 
#     except Exception as e:
#         return f"Message: {str(e)}"
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

def delete_user_from_room():
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
            return msg
        
        print("Coming")
        room_id = existing_rooms[0].get('id')
        
        print("room id",room_id)
        # Get existing room members

        room_memberships = list_membership(room_id)
        
        # print("mem list",room_memberships)
        existing_users = [membership['personEmail'] for membership in room_memberships]
        existing_users_ID = [membership['id'] for membership in room_memberships]

        print("user",existing_users)

        person_id = existing_users_ID
        print("pid",person_id)

        print("user_emails",user_emails)
        # Add users to the room

        dictionary = dict(zip(existing_users, existing_users_ID))
        print("diction",dictionary)
        for email in user_emails:
            if email in dictionary.keys():
                # for pid in dictionary.values():
                url = f'{WEBEX_API_URL}/memberships/{dictionary[email]}'

                
                response = requests.delete(url, headers=HEADERS_BOT)

                existing_users.append(email)
                print("Updated")
                msg=f"Users removed from room '{room_title}': {', '.join(user_emails)}"
                status_code=200
            else:
                print("not added")
                msg="User Email doesn't exist in room"
                status_code=400
        return msg,status_code
 
 
    except Exception as e:
        return f"Message: {str(e)}"