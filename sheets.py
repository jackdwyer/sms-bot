"""
Jack Dwyer 2016 August 21
Thin wrapper around the new google spreadsheet api.
Offers:
  - appending to a single column
"""
import httplib2
import os
import logging
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'smsbot'

logger = logging.getLogger(__name__)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   os.environ['GENERATED_CREDENTIALS'])

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class Gsheet(object):
    def __init__(self, spreadsheet_id, sheet_config):
        self.spreadsheet_id = spreadsheet_id
        self.load_sheet_config(sheet_config)
        self.login()

    def append_value(self, value, sheet):
        data = self.get_sheet(sheet)
        data.append(value)
        return self.update_sheet(sheet, data)

    def login(self):
        creds = get_credentials()
        self.service = discovery.build('sheets',
                    'v4',
                    http=creds.authorize(httplib2.Http()),
                    discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
        print('Logged into Google Spreadsheets')

    def load_sheet_config(self, config):
        self.config = dict([pair.split(',') for pair in config.split(':')])

    def get_sheet(self, opt):
        # returns list of values
        try:
            sheet = self.config[opt]
            rows = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=sheet).execute().get('values', [])
            return rows
        except KeyError:
            logger.error("Invalid sheet choice, returning false")
            return False

    def update_sheet(self, opt, data):
        # returns True if updated
        try:
            sheet = self.config[opt]
            self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=sheet, body={'values': data}, valueInputOption='RAW').execute()
            return True
        except KeyError:
            logger.error("Invalid sheet choice, returning false")
            return False




if __name__ == '__main__':
    gclient = Gsheet(os.environ['SPREADSHEET_ID'], os.environ['SPREADSHEET_CONFIG'])

