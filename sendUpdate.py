from flask import Flask, request, jsonify
import requests
from config import HEADERS,HEADERS_BOT,WEBEX_API_URL

def find_room_by_title(room_title):
    #Listing webex room details 
    url = f'{WEBEX_API_URL}/rooms'
    params = {'max': 100}
    response = requests.get(url, headers=HEADERS)
    rooms = response.json().get('items', [])
    print(rooms)
    if response.status_code == 200:
        # Save the room list to a JSON file
        print("going")
        # with open('room_list.json', 'w') as file:
        #    json.dump(response.json().get('items', []), file)   
    else:
        return jsonify({"error": "Failed to fetch room list"}), response.status_code
    
    for room in rooms:
        if room['title'] == room_title:
            print("rt",room['title'])
            print("rt",room['id'])
            return room['id']
    return None

def sending_stock_update(room_title, companyName, stockPrice):
    #Listing webex room details 
    normalPrice=1880
    string_number=float(stockPrice)
    difference = string_number - normalPrice

# Calculate the percentage difference
    percentage_difference = abs((difference / normalPrice) * 100)
    percentage_difference_str = f" ({percentage_difference:.2f})%"

# Convert to strings
    difference_str = str(difference) 
    final_String = difference_str + percentage_difference_str
    json_body= [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
          {
            "type": "TextBlock",
            "text": companyName,
            "size": "large",
            "wrap": True,
            "style": "heading"
          },
          {
          "type": "TextBlock",
          "text": "NSE: INFY",
          "isSubtle": True,
          "spacing": "none",
          "wrap": True
        },
        {
          "type": "TextBlock",
          "text": " \u20B9 "+ stockPrice ,
          "size": "extraLarge",
          "wrap": True
        },
        {
          "type": "TextBlock",
          "text": "▲ " + final_String if string_number > normalPrice else ("▼ " + final_String if string_number < normalPrice else "00  (0.00)%"),
          "color": "good" if string_number > normalPrice else ("attention" if string_number < normalPrice else "none"),
          "spacing": "none",
          "wrap": True
        }
        ]
      }
    }
  ]

    url = f'{WEBEX_API_URL}/messages'
    params = {'max': 100}
    print("data sending to the API, Roomtitle", room_title, "text", stockPrice, "attachments",json_body)
    data = {'roomId': room_title, 'text': "Testing the bot at 2:47", 'attachments':json_body}
    response = requests.post(url, headers=HEADERS_BOT, json=data)
   
    print("ifresponse.status_code :  ",response.status_code)

    return response.json()