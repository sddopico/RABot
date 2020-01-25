from __future__ import print_function
import datetime
import pickle
import os.path
from datetime import date, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # Need i/o or front end for entering data for `yesterday` variable below.
    # Allow for selection of days, hours, or minutes
    # Allow for integer input of above selection
    now = datetime.datetime.utcnow()
    yesterday = now - timedelta(days=1)
    calendarList_result = service.calendarList().list(minAccessRole='owner').execute()

    # Get calendarId for project calendar
    pcalendarId = ''
    calendars = calendarList_result.get('items', [])
    for calendar in calendars:
        if calendar['summary'] == 'Command Center Notifications':
            pcalendarId = calendar['id']

    # Get list of events from project calendar
    events_result = service.events().list(calendarId=pcalendarId).execute()
    events = events_result.get('items', [])
    for event in events:
        if event['created'] >= yesterday.isoformat() + 'Z': # 'Z' indicates UTC time
            print(event['summary'])


if __name__ == '__main__':
    main()
