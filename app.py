# from datetime import date, datetime, timedelta
# from flask import Flask, jsonify, request
# import requests
# import json
# import certifi
# from dateutil import parser
# import Subscribeuser
# import CreateMeeting
# import RequiredMeetingQualities,RemoveUser,RemoveRoom,sendUpdate
# from config import BOT_EMAIL
# from exceptions import handle_errors
# from config import headers



# app = Flask(__name__)

# def validate_token():
#     response = requests.get('https://api.ciscospark.com/v1/people/me', headers=headers)
 
#     if response.status_code == 401:
#         raise Exception("Invalid token")

# #Wrong Api Path
# @app.errorhandler(404)
# def page_not_found(e):
#     return jsonify({"error": "This API path is not available."}), 404

# @app.route('/CreateMeeting', methods=['POST'], endpoint='create_meeting')
# @handle_errors
# def create_meeting():
#     validate_token()
#     return CreateMeeting.create_meeting()

# @app.route('/ListMeetings', methods=['GET'], endpoint='list_meetings')
# @handle_errors
# def list_meetings():
#     validate_token()
#     return CreateMeeting.meeting_list()
    
# @app.route('/MeetingQualities', methods=['GET'], endpoint='meeting_qualities')
# @handle_errors
# def meeting_qualities():
#     validate_token()
#     return CreateMeeting.meeting_qualities()

# @app.route('/RequiredMeetingQualities', methods=['GET'], endpoint='user_details')
# @handle_errors
# def user_details():
#     validate_token()
#     return RequiredMeetingQualities.get_user_details()

# @app.route('/subscribeUser', methods=['POST','GET'],endpoint='subscribe_user')
# @handle_errors
# def subscribe_user():
#     validate_token()
#     data = request.json
#     room_title = data.get('title')
#     person_email = data.get('personEmail')
#     roomid=data.get('id')

    
#     #When there is no user_email
#     if len(person_email)==0:
#         return jsonify({"error": "User email not provided"}), 400
    
#     room_list=Subscribeuser.find_room_by_title(room_title)

#     if room_list is None:
#       print("room not created")
#       return jsonify({"message":"Room already Exist, Cannot add the user",'roomTitle': room_title}),400
      
#     room = Subscribeuser.create_room(room_title) # Creating the room
#     Subscribeuser.add_bot_to_room(room['id'], BOT_EMAIL)  # Add BOT to the room by admin or end user
#     a=Subscribeuser.add_users_to_room() # bot adding the user  
#     # if roomid:
#     #  print("bot adding user")
#     #  a=Subscribeuser.add_users_to_room() # bot adding the user
#     return jsonify({"message":a,'roomTitle': room_title, 'personEmail': person_email})
        

# @app.route('/UnsubscribeUser', methods=['POST'], endpoint="Unsubscribe_user")
# @handle_errors
# def Unsubscribe_user():
#     validate_token()
#     data = request.json
#     room_title = data.get('title')
#     person_email = data.get('personEmail')

    
#     room_list=RemoveUser.find_room_by_title(room_title)
#     print(room_list)
#     if room_list :
#       print("Room")
#       a=RemoveUser.delete_user_from_room()
#       return jsonify({"message":a[0],'roomTitle': room_title}),a[1]
#     return jsonify({"message":"Room doesn't exist"}),404


# @app.route('/RemoveRoom', methods=['POST'])
# @handle_errors
# def Remove_room():
#     validate_token()
#     data = request.json
#     room_title = data.get('title')
#     person_email = data.get('personEmail')

    
#     room_list=RemoveRoom.find_room_by_title(room_title)
#     print(room_list)
#     if room_list :
#       print("Room")
#       a=RemoveRoom.delete_room()
#       return jsonify({"message":a[0],'roomTitle': room_title}),a[1]
    
#     return jsonify({"message":"Room doesn't exist"}),404

# @app.route('/sendUpdateMessage', methods=['POST'],endpoint="send_Message")
# @handle_errors
# def send_Message():
#     data = request.json
#     print("========================",)
#     room_title = data.get('title')
#     companyName = data.get('companyName')
#     stockPrice = data.get('price')

#     print("========================",room_title)

#     room_list=sendUpdate.find_room_by_title(room_title)

#     return sendUpdate.sending_stock_update(room_list,companyName,stockPrice)
from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request
import requests
import json
import certifi
from dateutil import parser
import Subscribeuser
import CreateMeeting
import RequiredMeetingQualities,RemoveUser,RemoveRoom,sendUpdate
from config import BOT_EMAIL
from exceptions import handle_errors
from config import headers
import logging
 
logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)
 
app = Flask(__name__)
 
def validate_token():
    try:
        response = requests.get('https://api.ciscospark.com/v1/people/me', headers=headers)
 
        if response.status_code == 401:
            raise Exception("Invalid token")
    except Exception as e:
        logging.error(f"Error in validate_token: {e}")
        raise
 
@app.errorhandler(404)
def page_not_found(e):
    logging.error("This API path is not available.")
    return jsonify({"error": "This API path is not available."}), 404
 

# Scheduling meetings
@app.route('/CreateMeeting', methods=['POST'], endpoint='create_meeting')
@handle_errors
def create_meeting():
    try:
        validate_token()
        return CreateMeeting.create_meeting()
    except Exception as e:
        logging.error(f"Error in create_meeting: {e}")
        raise
 
# Fetching all meetings created
@app.route('/ListMeetings', methods=['GET'], endpoint='list_meetings')
@handle_errors
def list_meetings():
    try:
        validate_token()
        return CreateMeeting.meeting_list()
    except Exception as e:
        logging.error(f"Error in list_meetings: {e}")
        raise

# Meeting Qualities of latest meeting (ended or ongoing)
@app.route('/MeetingQualities', methods=['GET'], endpoint='meeting_qualities')
@handle_errors
def meeting_qualities():
    try:
        validate_token()
        return CreateMeeting.meeting_qualities()
    except Exception as e:
        logging.error(f"Error in meeting_qualities: {e}")
        raise

#  Meeting Qualities specific details
@app.route('/RequiredMeetingQualities', methods=['GET'], endpoint='user_details')
@handle_errors
def user_details():
    try:
        validate_token()
        return RequiredMeetingQualities.get_user_details()
    except Exception as e:
        logging.error(f"Error in user_details: {e}")
        raise

# Add user to room
@app.route('/subscribeUser', methods=['POST','GET'],endpoint='subscribe_user')
@handle_errors
def subscribe_user():
    try:
        validate_token()
        data = request.json
        room_title = data.get('title')
        person_email = data.get('personEmail')
        roomid=data.get('id')
 
        # When there is no user_email
        if len(person_email)==0:
            return jsonify({"error": "User email not provided"}), 400
        
        # When there is no title
        if len(room_title)==0:
            return jsonify({"error": "room title not provided"}), 400
 
        room_list=Subscribeuser.find_room_by_title(room_title)
 
        if room_list is None:
            logging.error("Room not created")
            return jsonify({"message":"Room already Exist, Cannot add the user",'roomTitle': room_title}),400
 
        room = Subscribeuser.create_room(room_title) # Creating the room
        Subscribeuser.add_bot_to_room(room['id'], BOT_EMAIL)  # Add BOT to the room by admin or end user
        a=Subscribeuser.add_users_to_room() # bot adding the user  

        return jsonify({"message":a,'roomTitle': room_title, 'personEmail': person_email})
    except Exception as e:
        logging.error(f"Error in subscribe_user: {e}")
        raise
 
# Sending stocks update
@app.route('/sendUpdateMessage', methods=['POST'],endpoint="send_Message")
@handle_errors
def send_Message():
    try:
        validate_token()
        data = request.json
        room_title = data.get('title')
        companyName = data.get('companyName')
        stockPrice = data.get('price')
 
        room_list=sendUpdate.find_room_by_title(room_title)
        if room_list:
            return sendUpdate.sending_stock_update(room_list,companyName,stockPrice)
        return jsonify({"message":"Room doesn't exist"}),400
    except Exception as e:
        logging.error(f"Error in send_Message: {e}")
        raise
 
# Unsubscribe user
@app.route('/UnsubscribeUser', methods=['POST'], endpoint="Unsubscribe_user")
@handle_errors
def Unsubscribe_user():
    try:
        validate_token()
        data = request.json
        room_title = data.get('title')
        person_email = data.get('personEmail')
 
        room_list=RemoveUser.find_room_by_title(room_title)
        if room_list :
            a=RemoveUser.delete_user_from_room()
            return jsonify({"message":a[0],'roomTitle': room_title}),a[1]
        return jsonify({"message":"Room doesn't exist"}),400
    except Exception as e:
        logging.error(f"Error in Unsubscribe_user: {e}")
        raise

# Remove room
@app.route('/RemoveRoom', methods=['POST'])
@handle_errors
def Remove_room():
    try:
        validate_token()
        data = request.json
        room_title = data.get('title')
        person_email = data.get('personEmail')
 
        room_list=RemoveRoom.find_room_by_title(room_title)
        if room_list :
            a=RemoveRoom.delete_room()
            return jsonify({"message":a[0],'roomTitle': room_title}),a[1]
 
        return jsonify({"message":"Room doesn't exist"}),400
    except Exception as e:
        logging.error(f"Error in Remove_room: {e}")
        raise
 
 


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)
    # app.run(debug=True,host='10.82.101.97',port=5000)