from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/calendar.events']

# The ID and range of a spreadsheet.
SPREADSHEET_ID = '1iBpk0sePz4MTP6Q9lGe6R3XvjUid3ynB8TWs0ka1xpA'
RANGE_NAME = 'Sheet1!A24:G24'

# The ID of a calendar event
EVENT_ID = '049ssfrp40nl7p8b14ri9j59mr'

creds = None

def getCreds():
    global creds
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
    return creds

def request(method, service, version):

    # Calls googleapi and
    # Accepts 'method, ''service', 'version'
    # Returns [request resource]

    global creds

    s = build(service, version, credentials=creds)
    sheet = s.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()

    return result

def main():

    global creds
    creds = getCreds()

    # Call the Sheets API

    result = request('get', 'sheets', 'v4')
    values = result.get('values', [])

    # Retrieve event from calendar api
    #cService = build('calendar', 'v3', credentials=creds)
    #event = cService.events()
    #eResult = event.get(calendarId='primary',
    #                    eventId=EVENT_ID).execute()

    if not values:
        agenda = 'No scheduled updates this week.'
    else:
        agenda = '%s\n' % values[0][0]
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            agenda = agenda + '%s - %s\n%s - %s\n%s - %s'  % (row[1], row[2], row[3], row[4], row[5], row[6])

        #event['description'] = agenda
        '''updated_event = event.update(calendarId='primary',
                                    eventId=event['id'],
                                    body=event).execute()'''
        print(agenda)

if __name__ == '__main__':
    main()
