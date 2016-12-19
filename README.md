# Kiosk API Toolkit for PHP

The Kiosk API Toolkit for PHP is designed to allow Lead Vendors for Kiosk 
to be able to submit Prospect records to the Kiosk Prospect API.  The toolkit 
handles the OAuth2 authentication process, reusing the Bearer Token where 
possible, and provides a simple function that accepts a Prospect record in 
array format and submits it over the API.  

## Sample Prospect Submission

```python
from kiosk_api_client import KioskApiClient

client_id = '<CLIENT ID>'
client_secret = '<CLIENT SECRET>'

api = KioskApiClient(client_id, client_secret)

prospect = {
    'FirstName':         'John',
    'LastName':          'Test',
    'Email':             'test@kiosk.tm',
    'Phone':             '4155551234',
    'ProgramOfInterest': 'Math'
}

result = api.submit_prospect(prospect)
```

## Sample Responses

The `submit_prospect` method always returns an array with a "status" element.  
The "status" element with be either "ok" or "error".

### OK Response

Valid submissions with have a "status" of "ok" and will provide an "id" and 
"prospect_id".  It is critically important that these IDs are retained so 
that they can be used to investigate issues with missing leads.

```python
{'id': u'<CONVERSION ID>',
 'prospect_id': u'<PROSPECT ID>',
 'status': 'ok'}
```

### Invalid Response

Invalid submissions will have a "status" of "error" and will provide a 
"validation" element detailing which fields were valid (true) or invalid 
(false).

```python
{'error': 'InvalidProspect',
 'message': 'The Prospect you submitted had invalid field data.  Please check the "validation" element to see which fields were invalid.',
 'status': 'error',
 'validation': {u'Email': True,
                u'Phone': False,
                u'ProgramOfInterest': True,
                u'is_valid': False}}
```

