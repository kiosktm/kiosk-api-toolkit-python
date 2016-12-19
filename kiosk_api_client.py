from datetime import datetime
import json, requests, time

class KioskApiClient(object):

    def __init__(self, oauth_client_id=None, oauth_client_secret=None, host="https://api.smartrfi.kiosk.tm"):
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret
        self.host = host

        self.bearer_token = None
        self.bearer_token_expires = self.current_timestamp

    @property
    def current_timestamp(self):
        return time.mktime(datetime.now().timetuple())

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def oauth_client_id(self):
        return self._oauth_client_id

    @oauth_client_id.setter
    def oauth_client_id(self, oauth_client_id):
        self._oauth_client_id = oauth_client_id

    @property
    def oauth_client_secret(self):
        return self._oauth_client_secret

    @oauth_client_secret.setter
    def oauth_client_secret(self, oauth_client_secret):
        self._oauth_client_secret = oauth_client_secret

    def authenticate(self, refresh=False):
        if(not refresh and self.bearer_token is not None and self.current_timestamp <= self.bearer_token_expires):
            return self.bearer_token;

        url = "%s/oauth" % self.host

        http_headers = {
            'Content-Type': 'application/json', 
            'Accept':       'application/json' 
        }

        payload = {
            "grant_type":    "client_credentials", 
            "client_id":     self.oauth_client_id, 
            "client_secret": self.oauth_client_secret
        }

        result = requests.post(url, data=json.dumps(payload), headers=http_headers, verify=False)

        if result is None:
            raise StandardError("Kiosk API Authentication Error")

        result = json.loads(result.text)

        if 'access_token' in result:
            self.bearer_token = result['access_token']
            self.bearer_token_expires = self.current_timestamp + int(result['expires_in'])
        else:
            return None

        return self.bearer_token

    def submit_prospect(self, prospect_fields):
        bearer_token = self.authenticate()

        if bearer_token is None:
            raise StandardError("Authentication Failed")

        url = "%s/prospect" % self.host

        http_headers = {
            'Content-Type':  'application/json', 
            'Accept':        'application/json', 
            'Authorization': 'Bearer %s' % bearer_token
        }

        result = requests.post(url, data=json.dumps(prospect_fields), headers=http_headers, verify=False)

        if result is None:
            return None

        result = json.loads(result.text)

        if 'status' in result and result['status'] == 'ok':
            return {
                'status':      'ok', 
                'id':          result['id'], 
                'prospect_id': result['prospect_id']
            }
        else:
            return {
                'status':     'error', 
                'error':      'InvalidProspect', 
                'message':    'The Prospect you submitted had invalid field data.  Please check the "validation" element to see which fields were invalid.', 
                'validation': result['detail']['validation']
            }

