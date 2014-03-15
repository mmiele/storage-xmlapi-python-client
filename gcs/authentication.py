'''
    Contains the GCS_Authentication class that generates an 
    authenticated HTTP client object. 
    The class uses the user's credentials.
    @version: 1.0
'''

__author__ = 'mielem@gmail.com'

import os

from apiclient.discovery import build as discovery_build

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as CredentialStorage
from oauth2client.tools import run as run_oauth2

from oauth2client.clientsecrets import InvalidClientSecretsError

import httplib2

# Local imports
import config


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/[your project ID]/apiui>
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# File to store authentication credentials after acquiring them.
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'stored_credentials.json')

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console
<https://code.google.com/apis/console#access>.

""" % CLIENT_SECRETS_FILE

class GCS_Authentication():
    '''
     Authenticates the application using the user's credentials via OAuth2.
     @note: It uses OAuth2.
    '''
    
    def _create_http_auth_client(self, force_auth, debug_level):
        '''
            Creates an authenticated HTTP request object. 
            @param force_auth: Flag to recreate the stored credentials [True | False].
            @param debug_level:The level of debugging message to use (0 to 4).  
            @return: 
                config.app_data['http_client'] = http_client
                config.app_data['auth_http_client'] = auth_http
            @note: In order for this function to work you need to populate the 
            client_secrets.json file.
            The credentials are stored in a local file and reused without going through 
            the OAuth2 flow again, unless you force the authentication to be executed.
            This might be required to change the authentication scope.
            
        '''
    
        # Authenticate the application.
    
        # Set up a Flow object to be used for authentication.
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=config.app_data['scope'],
                    message=MISSING_CLIENT_SECRETS_MESSAGE)
       
        
        # If the credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # credentials will get written back to the file.
        credential_storage = CredentialStorage(CREDENTIALS_FILE)
        credentials = credential_storage.get()
    
    
        if credentials is None or credentials.invalid or force_auth:
            credentials = run_oauth2(flow, credential_storage)
      
   
        # Create Google Cloud Storage authenticated client.
    
        # Create an httplib2.Http object to handle our HTTP requests 
        # and authorize it with our good Credentials.
        http_client = httplib2.Http()
        
        if debug_level != None:
            # Set debug level.
            httplib2.debuglevel=debug_level

        auth_http = credentials.authorize(http_client)
    
        # Update global application information.
        config.app_data['http_client'] = http_client
        config.app_data['auth_http_client'] = auth_http
    
