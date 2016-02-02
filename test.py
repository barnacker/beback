from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import argparse
import json

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET = 'client_secret.json'

store = file.Storage('storage.json')
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store, flags)

SERVICE = build('drive', 'v3', http=credz.authorize(Http()))
result = []
page_token = None
while True:
    try:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = SERVICE.files().list(**param).execute()

        result.extend(files['files'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        break
result = json.dumps(result)
print result
