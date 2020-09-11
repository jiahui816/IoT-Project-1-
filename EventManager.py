from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class EventManager():
    
    @staticmethod
    def setUp():
        # If modifying these scopes, delete the file token.json.
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        service = build("calendar", "v3", http=creds.authorize(Http()))
        return SCOPES, store, creds, service

    @staticmethod
    def insert(bookName, userName):
        
        SCOPES, store, creds, service = EventManager.setUp()
        
        time_now = datetime.now()
        time_return = time_now + timedelta(days = 7)
        time_return_over = time_return + timedelta(days = 1)
        startString = time_return.strftime('%Y-%m-%dT%H:%M:%S+10:00')   
        endString = time_return_over.strftime('%Y-%m-%dT%H:%M:%S+10:00')
        
        bookBorrowInfo = "Book ["+bookName+"] Borrowed By "+userName
        event = {
            "summary": "Book Borrowed Out Event",
            "location": "Group 15 Smart Library",
            "description": bookBorrowInfo,
            "start": {
                "dateTime": startString,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": endString,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                { "email": "felix961213@gmail.com" }
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 30 },
                    { "method": "popup", "minutes": 10 },
                ],
            }
        }

        event = service.events().insert(calendarId = "primary", body = event).execute()
        
        return event['id']

    @staticmethod
    def deleteEvent(eId):
        SCOPES, store, creds, service = EventManager.setUp()
        service.events().delete(calendarId='primary', eventId = eId).execute()
        print("Event Deleted, thank you!")
    
    @staticmethod
    def getValidEventIds():
        eIdList = []
        SCOPES, store, creds, service = EventManager.setUp()
       
        now = datetime.utcnow().isoformat() + "Z" 
        
        events_result = service.events().list(calendarId = "primary", timeMin = now,
            maxResults = 999, singleEvents = True, orderBy = "startTime").execute()
        events = events_result.get("items", [])
        
        for event in events:
            eIdList.append(event['id'])
        
        return eIdList
